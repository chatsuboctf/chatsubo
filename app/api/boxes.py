# import threading
import os
from multiprocessing import Process

from eventlet import greenthread
from datetime import timedelta, datetime
# from pprint import pprint
from uuid import uuid4

from flask import current_app, request
from flask_restx import Resource, abort
from sqlalchemy import exc, desc

from app.api import boxes_api
from app.helpers.api_response import ListBoxesTemplatesApiResponse, ListBoxesApiResponse, BaseApiResponse
from app.helpers.auth import require_admin, morph_admin
from app.helpers.boxes import is_box_completed_by, upgrade_box_with_stats
from app.helpers.upload import allowed_file, ALLOWED_IMG_EXTENSIONS
from app.models.boxes import Boxes
from app.models.categories import Categories
from app.models.flags import Flags
from app.models.sessions import Sessions
from app.models.users import Users
from app.models.users_boxes import UsersBoxes
import app.context as ctx
from app.providers.exc import BackendConnectionException
from app.queue.boxes import start_box


@boxes_api.route('/templates/list')
class List(Resource):

    @require_admin
    def get(self):
        res = ListBoxesTemplatesApiResponse()

        try:
            res.templates = ctx.providers.list_templates()
        except Exception as e:
            res.add_error(str(e))
            return res.make(), 500

        for tpl in res.templates:
            if tpl["data"]["provider"].get("vpns"):
                del tpl["data"]["provider"]["vpns"]

        return res.make()


@boxes_api.route('/list')
class List(Resource):

    @require_admin
    def get(self):
        res = ListBoxesApiResponse()

        boxes = ctx.db.session.query(Boxes).all()
        res.set_boxes(boxes, public=False, with_flags=True)

        return res.make()


@boxes_api.route('/list_by_category/<string:category_slug>')
class List(Resource):

    @morph_admin
    def get(self, category_slug, is_admin=False):
        res = ListBoxesApiResponse()
        category = ctx.db.session.query(Categories).filter_by(slug=category_slug).first()
        if not category:
            res.add_error("Unknown category")
            return res.make(), 404

        boxes = ctx.db.session.query(Boxes).filter_by(category_id=category.id).all()

        if not boxes:
            res.boxes = []
            return res.make()

        if is_admin:
            res.set_boxes(boxes, public=False, with_flags=True)
        else:
            # Remove not released boxes
            boxes = list(filter(lambda b: b.released, boxes))
            res.set_boxes(boxes, public=True, with_flags=True)

        for box in res.boxes:
            box = upgrade_box_with_stats(box)

        return res.make()


@boxes_api.route('/get/<string:box_id>')
class List(Resource):

    @morph_admin
    def get(self, box_id, is_admin=False):
        res = ListBoxesApiResponse()
        box = ctx.db.session.query(Boxes).outerjoin(Categories).filter(Boxes.id == box_id).first()

        if not box:
            res.add_error("Unknown box")
            return res.make(), 404

        if is_admin:
            res.set_boxes([box], public=False, with_flags=True, with_deleted_flags=True)
        else:
            if not box.released:
                res.add_error("Unknown box")
                return res.make(), 404

            res.set_boxes([box], public=True, with_flags=True)

        for box in res.boxes:
            box = upgrade_box_with_stats(box)

        return res.make()


@boxes_api.route('/access/<string:realm>/<string:box_id>')
class List(Resource):

    @morph_admin
    def get(self, realm, box_id, is_admin=False):
        res = BaseApiResponse()
        box = ctx.db.session.query(Boxes).filter(Boxes.id == box_id).first()

        if not box:
            res.add_error("Unknown box")
            return res.make(), 404

        if not is_admin and not box.released:
            res.add_error("Unknown box")
            return res.make(), 404

        try:
            address = {"address": ctx.providers.get_address_of(realm, box.template)}
            creds = ctx.providers.get_creds_of(realm, box.template)
        except Exception as e:
            # import traceback
            # print(traceback.format_exc())

            res.add_error(str(e))
            return res.make(), 500

        if not address:
            res.add_error("No instance running in this realm")
            return res.make(), 404

        res.data = {
            "address": address,
            "creds": creds
        }

        return res.make()


@boxes_api.route('/session/<string:realm>/<string:box_id>/<string:user_id>')
class List(Resource):

    def get(self, realm, box_id, user_id):
        res = BaseApiResponse()
        res.data = {"session": None}
        box = ctx.db.session.query(Boxes).filter(Boxes.id == box_id).first()

        if not box:
            res.add_error("Unknown box")
            return res.make(), 404

        session = ctx.db.session.query(Sessions) \
            .filter(Sessions.realm == realm,
                    Sessions.box_id == box_id,
                    Sessions.user_id == user_id
                    ) \
            .order_by(desc(Sessions.started_at)) \
            .first()

        if not session:
            return res.make()

        res.data["session"] = session.to_json()
        res.data["session"]["address"] = ctx.providers.get_address_of(realm, box.template, session.id)
        res.data["session"]["creds"] = ctx.providers.get_creds_of(realm, box.template, session.id)

        return res.make()


@boxes_api.route('/new')
class Create(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        box = request.get_json()
        flags = []
        authors = []

        available_os = ['Linux', 'Windows', 'FreeBSD', 'Other']

        if box["os"] not in available_os:
            res.add_error(f"Unknown OS : {box['os']}. Available OSes : {', '.join(available_os)}")

        new_box = Boxes(
            id=uuid4(),
            name=box["name"],
            description=box["description"],
            os=box["os"],
            kind=box["kind"],
            background=box["background"],
            duration=box["duration"],
            difficulty=box["difficulty"],
            template=box["template"]["name"],
            category_id=box["category"]["id"]
        )

        try:
            ctx.db.session.add(new_box)
            ctx.db.session.flush()
        except exc.IntegrityError:
            ctx.db.session.rollback()
            existing_box = Boxes.query.filter_by(name=box["name"]).first()

            if existing_box and existing_box.deleted:
                res.add_error("A box with this name already exist but is deleted")
                return res.make(), 409
            elif existing_box:
                res.add_error("A box with this name already exist")
                return res.make(), 409

        # Add flags
        for flag in box.get("flags", []):
            flags.append(
                Flags(
                    id=uuid4(),
                    name=flag["name"],
                    value=flag["value"],
                    points=flag["points"],
                    icon=flag["icon"],
                    user=flag["user"],
                    root=flag["root"],
                    case_insensitive=flag["case_insensitive"],
                    dynamic=flag["dynamic"],
                    box_id=new_box.id
                )
            )

        ctx.db.session.bulk_save_objects(flags)
        ctx.db.session.flush()

        # Add authors
        for author_id in box.get("authors", []):
            authors.append(
                UsersBoxes(
                    user_id=author_id,
                    box_id=new_box.id
                )
            )

        ctx.db.session.bulk_save_objects(authors)
        ctx.db.session.commit()

        return res.make(), 201


@boxes_api.route('/delete/<string:box_id>')
class Delete(Resource):

    @require_admin
    def delete(self, box_id):
        res = BaseApiResponse()

        box = Boxes.query.filter_by(id=box_id).first()
        if not box:
            return res.add_error("Box not found"), 404

        box.deleted = True
        ctx.db.session.commit()

        return res.make()


@boxes_api.route('/bulk_delete')
class BulkDelete(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        boxes = request.json

        to_update = []
        for box in boxes:
            to_update.append({"id": box["id"], "deleted": True})

        try:
            ctx.db.session.bulk_update_mappings(Boxes, to_update)
            ctx.db.session.commit()
            return res.make()

        except Exception as e:
            res.add_error(f"failed to delete boxes in bulk : {str(e)}")
            return res.make(), 500


@boxes_api.route('/restore')
class RestoreDeleted(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        box = request.get_json()

        box = Boxes.query.filter_by(id=box["id"]).first()
        if not box:
            res.add_error("Box not found")
            return res.make(), 404

        box.deleted = False
        ctx.db.session.commit()

        return res.make()


@boxes_api.route('/reset/<string:realm>/<string:box_id>')
class RestoreDeleted(Resource):

    def do_reset(self, realm, box, session=None):
        try:
            if not ctx.providers.reset_box(realm, box.template, session=session):
                ctx.io.emit("notify", {
                    "message": f"{box.name} failed to reset",
                    "type": "warning"
                })
                return

        except BackendConnectionException:
            ctx.io.emit("notify", {
                "message": f"{box.name} failed to reset",
                "type": "warning"
            })
            return

        ctx.io.emit("notify", {
            "message": f"<b>{box.name}</b> has been reset",
            "type": "success"
        })

    def post(self, realm, box_id):
        session = None
        res = BaseApiResponse()
        data = request.get_json()
        user_data = data.get("user")
        if not user_data:
            res.add_error("Missing user data")
            return res.make(), 400

        session_id = data.get("session")

        box = Boxes.query.filter_by(id=box_id).first()
        if not box:
            res.add_error("Box not found")
            return res.make(), 404

        user = Users.query.filter_by(id=user_data["id"]).first()
        if not user:
            res.add_error("User not found")
            return res.make(), 404

        if not user.can_reset():
            next_reset = user.last_reset + timedelta(minutes=current_app.config.get("RESET_DELAY", 30))

            res.add_error(f"Next reset will be available at {str(next_reset)}")
            return res.make()

        if session_id:
            session = Sessions.query.filter_by(id=session_id).first()

        params = {
            "realm": realm,
            "template": box.template,
            "session": session,
        }

        # Ask provider of instance to schedule a reset
        # Signal to all users the reset
        if not user.admin:
            greenthread.spawn_after(5 * 60, self.do_reset, **params)

            user.update_last_reset()
            ctx.db.session.commit()

            ctx.io.emit("notify", {
                "message": f"{box.name} will be reset in 5 minutes",
                "type": "info"
            })
        else:
            greenthread.spawn_after(0, self.do_reset, **params)

        return res.make()


@boxes_api.route('/start/<string:realm>/<string:box_id>')
class Start(Resource):

    # def instance_timeout(self, session_id):
    #     session = Sessions.query.filter_by(id=session_id).first()
    #     if not session:
    #         return
    #
    #     try:
    #         ctx.providers.stop_dynamic_instance(session)
    #     except Exception:
    #         pass
    #
    #     try:
    #         Sessions.query.filter_by(id=session.id).delete()
    #         ctx.db.session.commit()
    #     except Exception:
    #         pass

    def post(self, realm, box_id):
        res = BaseApiResponse()
        user_data = request.get_json()

        box = Boxes.query.filter_by(id=box_id).first()
        if not box:
            res.add_error("Box not found")
            return res.make(), 404

        user = Users.query.filter_by(id=user_data["id"]).first()
        if not user:
            res.add_error("User not found")
            return res.make(), 404

        existing_session = Sessions.query.filter_by(realm=realm, box_id=box.id, user_id=user.id).first()
        if existing_session:
            res.add_error(f"An instance is already running for {realm}/{box.name}")
            return res.make(), 409

        session_id = str(uuid4())
        now = datetime.now().timestamp()
        box_expiration = now + (box.duration * 60)
        session = Sessions(id=session_id, realm=realm, state="pending", box_id=box.id, user_id=user.id, started_at=None, expires_at=datetime.fromtimestamp(box_expiration))

        ctx.db.session.add(session)
        ctx.db.session.commit()

        task = start_box.delay(realm, box.template, session_id, box.duration)

        session.task_id = task.id
        ctx.db.session.commit()

        res.data = {
            "session": session_id,
            "taskID": task.id
        }

        return res.make()


@boxes_api.route('/stop/<string:session_id>')
class Stop(Resource):

    def post(self, session_id):
        res = BaseApiResponse()
        session = ctx.db.session.query(Sessions) \
            .filter(Sessions.id == session_id) \
            .first()

        if not session:
            res.add_error("Session not found")
            res.make(), 404
            return

        # check if session belong to calling user (from cookie)
        session_cookie = request.cookies.get('CHATSUBO-SESSION')
        if not session_cookie:
            abort(401)
            return

        user = ctx.db.session.query(Users).filter_by(session=session_cookie).first()
        if not user:
            abort(401)
            return

        if session.owner.id != user.id:
            abort(401)
            return

        try:
            ctx.providers.stop_dynamic_instance(session.realm, session.id)
        except Exception as e:
            res.add_error(str(e))
            return res.make(), 500

        Sessions.query.filter_by(id=session.id).delete()
        ctx.db.session.commit()

        return res.make()


@boxes_api.route('/release/<string:box_id>')
class RestoreDeleted(Resource):

    @require_admin
    def post(self, box_id):
        res = BaseApiResponse()
        box = Boxes.query.filter_by(id=box_id).first()
        if not box:
            res.add_error("Box not found")
            return res.make(), 404

        box.released = True
        ctx.db.session.commit()

        return res.make()


@boxes_api.route('/retire/<string:box_id>')
class RestoreDeleted(Resource):

    @require_admin
    def post(self, box_id):
        res = BaseApiResponse()
        box = Boxes.query.filter_by(id=box_id).first()
        if not box:
            res.add_error("Box not found")
            return res.make(), 404

        box.released = False
        ctx.db.session.commit()

        return res.make()


@boxes_api.route('/edit/<string:box_id>')
class Edit(Resource):

    @require_admin
    def post(self, box_id):
        res = BaseApiResponse()
        new_box = request.get_json()

        old_box = Boxes.query.filter_by(id=box_id).first()
        if not old_box:
            res.add_error("Box not found")
            return res.make(), 404

        old_box.description = new_box["description"]
        old_box.template = new_box["template"]
        old_box.background = new_box["background"]
        old_box.duration = new_box["duration"]
        old_box.kind = new_box["kind"]
        old_box.difficulty = new_box["difficulty"]
        old_box.category_id = new_box["category_id"]
        old_box.name = new_box["name"]

        ctx.db.session.flush()

        # Add flags
        for new_flag in new_box.get("flags", []):
            # pprint(new_flag)
            flag = Flags.query.filter_by(id=new_flag.get("id")).first()
            if not flag:
                ctx.db.session.add(
                    Flags(
                        id=uuid4(),
                        name=new_flag["name"],
                        value=new_flag["value"],
                        points=new_flag["points"],
                        dynamic=new_flag["dynamic"],
                        icon=new_flag["icon"],
                        user=new_flag["user"],
                        root=new_flag["root"],
                        case_insensitive=new_flag["case_insensitive"],
                        box_id=box_id
                    )
                )
            else:
                flag.value = new_flag["value"]
                flag.points = new_flag["points"]
                flag.dynamic = new_flag["dynamic"]
                flag.user = new_flag["user"]
                flag.root = new_flag["root"]
                flag.case_insensitive = new_flag["case_insensitive"]

        ctx.db.session.flush()

        # Add new authors present in new_box but not in old_box
        for author_id in new_box.get("authors", []):
            if author_id not in [author.id for author in old_box.authors]:
                assoc = UsersBoxes.query.filter_by(user_id=author_id, box_id=old_box.id).first()
                if not assoc:
                    ctx.db.session.add(
                        UsersBoxes(
                            user_id=author_id,
                            box_id=old_box.id
                        )
                    )

        ctx.db.session.flush()

        # Remove new authors present in old_box but not in new_box
        for author in old_box.authors:
            if author.id not in [author_id for author_id in new_box.get("authors", [])]:
                UsersBoxes.query.filter_by(user_id=author.id, box_id=old_box.id).delete()

        ctx.db.session.commit()

        return res.make()


@boxes_api.route('/background/<string:box_id>')
class UploadAvatar(Resource):

    @require_admin
    def post(self, box_id):
        res = BaseApiResponse()

        background = request.files["background"]
        if not background or not allowed_file(background.filename, ALLOWED_IMG_EXTENSIONS):
            abort(400)

        unique_filename = f"{uuid4()}.{background.filename.rsplit('.', 1)[1].lower()}"
        background_path = os.path.join(current_app.config['BOXES_AVATARS_FOLDER'], unique_filename)
        background.save(background_path)

        backend_path = background_path.replace(current_app.config["DIST_DIR"], "")
        # if box_id != "temp":
        #     box = Boxes.query.filter_by(id=box_id).first()
        #     box.avatar = backend_path
        #     ctx.db.session.commit()

        res.data = {
            "path": backend_path
        }

        return res.make()
