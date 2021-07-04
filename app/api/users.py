# from pprint import pprint
import os
from pathlib import Path
from time import sleep
from uuid import uuid4

from flask import request, current_app
from flask_restx import Resource, abort
from sqlalchemy import func
from werkzeug.utils import secure_filename

from app.api import users_api, BaseApiResponse
from app.helpers.api_response import UserApiResponse, ListUsersApiResponse
import app.context as ctx
from app.helpers.auth import require_admin, check_user_session, morph_admin
from app.helpers.upload import allowed_file, ALLOWED_IMG_EXTENSIONS
from app.helpers.users import require_user_self, import_user
from app.models.boxes import Boxes
from app.models.flags import Flags
from app.models.users import Users
from app.models.users_flags import UsersFlags


@users_api.route('/<string:username>')
class Get(Resource):

    def get(self, username):
        res = UserApiResponse()

        user = ctx.db.session.query(Users).filter_by(username=username).first()
        if not user:
            res.add_error("Username not found")
            return res.make(), 404

        res.set_user(user, with_flags=True)

        return res.make()


@users_api.route('/top/<int:limit>')
class Get(Resource):

    def get(self, limit):
        res = ListUsersApiResponse()
        limit = limit if limit <= 500 else 500
        users = ctx.db.session.query(Users).filter_by(admin=False).order_by(Users.score.desc()).limit(limit).all()

        category_id = request.args.get('cat')
        if category_id:
            rows = (ctx.db.session.query(Users)
                  .filter_by(admin=False)) \
                  .filter(Boxes.category_id == category_id and category_id) \
                  .filter(UsersFlags.flag_id == Flags.id) \
                  .join(UsersFlags, UsersFlags.user_id == Users.id and UsersFlags.valid) \
                  .join(Flags, Flags.id == UsersFlags.flag_id) \
                  .join(Boxes, Boxes.id == Flags.box_id) \
                  .values(Users.id, Flags.points, UsersFlags.flagged_at, UsersFlags.valid)
        else:
            rows = (ctx.db.session.query(Users)
                  .filter_by(admin=False)) \
                  .filter(UsersFlags.flag_id == Flags.id) \
                  .join(UsersFlags, UsersFlags.user_id == Users.id and UsersFlags.valid) \
                  .join(Flags, Flags.id == UsersFlags.flag_id) \
                  .join(Boxes, Boxes.id == Flags.box_id) \
                  .values(Users.id, Flags.points, UsersFlags.flagged_at, UsersFlags.valid)

        results = list(rows)

        for user in users:
            user.score = 0
            # x[3] : UsersFlags.valid
            user.score = sum([flag_value for _, flag_value, _, _ in filter(lambda r: r[0] == user.id and r[3], results)])

        if not users:
            res.add_error("No users found")
            return res.make(), 404

        res.set_users(users, with_flags=False)
        res.users = sorted(res.users, key=lambda u: u["score"], reverse=True)

        for user in res.users:
            # r[3] : UsersFlags.valid
            user["flagged"] = len(list(filter(lambda r: r[0] == user["id"] and r[3], results)))

        return res.make()


@users_api.route('/all')
class List(Resource):

    @morph_admin
    def get(self, is_admin=False):
        res = ListUsersApiResponse()

        if is_admin:
            users = ctx.db.session.query(Users).order_by(Users.score.desc()).all()
        else:
            users = ctx.db.session.query(Users).filter_by(admin=False).order_by(Users.score.desc()).all()

        res.set_users(users)

        return res.make()


@users_api.route('/edit')
class Edit(Resource):

    @require_user_self
    @import_user
    def post(self, user=None):
        res = BaseApiResponse()
        new_user = request.get_json()

        try:
            if len(new_user["password"]) > 0:
                if not new_user["newPassword"] == new_user["newPasswordConfirmation"]:
                    res.add_error("Password does not match")
                    return res.make()
                elif not user.check_password(new_user["password"]):
                    res.add_error("Bad password")
                    return res.make()
                else:
                    user.set_password(new_user["newPassword"])
        except KeyError:
            res.add_error("Missing fields")
            return res.make(), 400

        user.avatar = new_user["background"]
        ctx.db.session.commit()

        return res.make()


@users_api.route('/edit/<string:user_id>')
class EditUser(Resource):

    @require_admin
    def post(self, user_id):
        res = BaseApiResponse()
        new_user = request.get_json()

        user = ctx.db.session.query(Users).filter_by(id=user_id).first()
        if not user:
            res.add_error("User not found")
            return res.make(), 404

        try:
            if len(new_user["password"]) > 0:
                if not new_user["password"] == new_user["passwordConfirmation"]:
                    res.add_error("Password does not match")
                    return res.make()
                elif not user.check_password(new_user["password"]):
                    res.add_error("Bad password")
                    return res.make()
        except KeyError:
            res.add_error("Missing fields")
            return res.make(), 400

        user.set_password(new_user["newPassword"])
        ctx.db.session.commit()

        return res.make()


@users_api.route('/reset/<string:user_id>')
class ResetPass(Resource):

    @require_admin
    def post(self, user_id):
        res = BaseApiResponse()
        data = request.get_json()
        new_pass = data.get("newPass")
        if not new_pass:
            res.add_error("Missing arg 'newPass'")
            return res.make(), 400

        user = ctx.db.session.query(Users).filter_by(id=user_id).first()
        if not user:
            res.add_error("User not found")
            return res.make(), 404

        user.set_password(new_pass)
        ctx.db.session.commit()

        return res.make()


@users_api.route('/set_admin')
class ResetPass(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        data = request.get_json()
        user_id = data.get("userID")
        if not user_id:
            res.add_error("Missing arg 'userID'")
            return res.make(), 400

        print(data)

        state = data.get("state")
        if state is None:
            res.add_error("Missing arg 'state'")
            return res.make(), 400

        if type(state) is not bool:
            res.add_error("Invalid state value")
            return res.make(), 400

        user = ctx.db.session.query(Users).filter_by(id=user_id).first()
        if not user:
            res.add_error("User not found")
            return res.make(), 404

        user.admin = state
        ctx.db.session.commit()

        return res.make()


@users_api.route('/avatar/<string:user_id>')
class UploadAvatar(Resource):

    @import_user
    def post(self, user_id, user=None):
        res = BaseApiResponse()
        target_user_id = user_id
        session = request.cookies.get('CHATSUBO-SESSION')
        if not check_user_session(target_user_id, session):
            abort(401)
            return

        avatar = request.files["avatar"]
        if not avatar or not allowed_file(avatar.filename, ALLOWED_IMG_EXTENSIONS):
            abort(400)

        unique_filename = f"{uuid4()}.{avatar.filename.rsplit('.', 1)[1].lower()}"
        users_avatar_dir = os.path.abspath(os.path.join(current_app.config['AVATARS_FOLDER'], user.id))
        Path(users_avatar_dir).mkdir(parents=True, exist_ok=True)

        avatar_path = os.path.join(users_avatar_dir, unique_filename)
        avatar.save(avatar_path)

        backend_path = avatar_path.replace(current_app.config["DIST_DIR"], "")

        user.avatar = backend_path
        ctx.db.session.commit()

        res.data = {
            "path": backend_path
        }

        return res.make()
