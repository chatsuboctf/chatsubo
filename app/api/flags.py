import hashlib
# from pprint import pprint

from flask import request
from flask_restx import Resource

from uuid import uuid4

from sqlalchemy import desc

import app.context as ctx
from app.api import flags_api
from app.helpers.api_response import BaseApiResponse
from app.helpers.auth import require_admin
from app.helpers.flags import require_allowed_submissions
from app.helpers.users import require_user_self, import_user
from app.models.boxes import Boxes
from app.models.flags import Flags
from app.models.sessions import Sessions
from app.models.users import Users
from app.models.users_flags import UsersFlags


@flags_api.route('/generate')
class List(Resource):

    def get(self):
        return {
            "errors": [],
            "flag": hashlib.sha1(str(uuid4()).encode()).hexdigest()
        }


@flags_api.route('/delete/<string:flag_id>')
class Delete(Resource):

    @require_admin
    def delete(self, flag_id):
        res = BaseApiResponse()
        flag = Flags.query.filter_by(id=flag_id).first()
        if not flag:
            res.add_error("Flag not found")
            return res.make(), 404

        flag.deleted = True
        ctx.db.session.commit()

        return res.make()


@flags_api.route('/check/<string:box_id>')
class Check(Resource):

    @require_allowed_submissions
    def post(self, box_id):
        valid = False
        res = BaseApiResponse()
        res.data = {
            "success": False,
            "new": False
        }

        data = request.get_json()
        realm = data.get("realm")
        # if not realm:
        #     res.add_error("Missing realm")
        #     return res.make(), 400

        user_data = data.get("user")
        if not user_data:
            res.add_error("Missing user data")
            return res.make(), 400

        user = Users.query.filter_by(id=user_data["id"]).first()

        candidate = data.get("flag")
        if not candidate:
            res.add_error("Missing flag")
            return res.make(), 400

        box = Boxes.query.filter_by(id=box_id).first()
        if not box:
            res.add_error("Unknown box")
            return res.make(), 404

        if box.kind == "dynamic":
            session = Sessions.query.filter_by(
                user_id=user.id,
                box_id=box.id,
                realm=realm
            ) \
                .order_by(desc(Sessions.started_at)) \
                .first()

            flags_data = ctx.providers.get_flags_of(realm, box.template, session.id)
            flags = Flags.query.filter_by(box_id=box.id).all()

            for flag in flags:
                try:
                    current_flag = next(filter(lambda f: f["name"] == flag.name, flags_data))
                except StopIteration:
                    continue
                if not current_flag:
                    continue

                flag.value = current_flag["value"]

        else:
            flags = Flags.query.filter_by(box_id=box_id).all()
            if not flags:
                res.add_error("No flags found for this box")
                return res.make(), 404

            flags = filter(lambda f: not f.deleted, flags)

        for flag in flags:
            if flag.case_insensitive:
                candidate = candidate.lower()
                flag.value = flag.value.lower()

            if not candidate == flag.value:
                continue

            if UsersFlags.query.filter_by(user_id=user_data["id"], flag_id=flag.id, valid=True).first():
                return res.make(), 409
            else:
                valid = True
                break

        validation = UsersFlags(id=uuid4(), user_id=user_data["id"], flag_id=flag.id, value=candidate, valid=valid)
        ctx.db.session.add(validation)
        if valid:
            user.score += flag.points

        ctx.db.session.commit()

        res.data["success"] = valid
        res.data["new"] = True

        return res.make()


@flags_api.route('/restore/<string:flag_id>')
class Restore(Resource):

    @require_admin
    def post(self, flag_id):  # GET ?
        res = BaseApiResponse()
        flag = Flags.query.filter_by(id=flag_id).first()
        if not flag:
            res.add_error("Flag not found")
            return res.make(), 404

        flag.deleted = False
        ctx.db.session.commit()

        return res.make()


@flags_api.route('/submissions/all')
class AllSubmissions(Resource):

    @require_admin
    def get(self):
        res = BaseApiResponse()
        res.data = []

        submissions = ctx.db.session.query(UsersFlags, Users, Flags, Boxes) \
            .join(Users, UsersFlags.user_id == Users.id) \
            .join(Flags, UsersFlags.flag_id == Flags.id) \
            .join(Boxes, Flags.box_id == Boxes.id) \
            .order_by(UsersFlags.flagged_at.desc()) \
            .all()

        if not submissions:
            res.add_error("No submissions yet")
            return res.make()

        for sub in submissions:
            res.data.append({
                "user": sub.Users.to_json(),
                "box": sub.Boxes.to_json(),
                "submission": sub.UsersFlags.to_json()
            })

        return res.make()


@flags_api.route('/submissions/by_user/<string:user_id>')
class Submissions(Resource):

    @require_user_self
    def get(self, user_id):
        res = BaseApiResponse()
        res.data = []

        submissions = ctx.db.session.query(UsersFlags, Users, Flags, Boxes) \
            .join(Users, UsersFlags.user_id == Users.id) \
            .join(Flags, UsersFlags.flag_id == Flags.id) \
            .join(Boxes, Flags.box_id == Boxes.id) \
            .order_by(UsersFlags.flagged_at.desc()) \
            .filter(Users.id == user_id) \
            .all()

        if not submissions:
            res.add_error("No submissions yet")
            return res.make()

        for sub in submissions:
            res.data.append(sub.UsersFlags.to_json())

        return res.make()
