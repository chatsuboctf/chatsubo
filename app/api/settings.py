import dateutil.parser
from dateutil.tz import tzlocal, UTC
from flask import request, current_app
from flask_restx import Resource, abort

from app.api import settings_api
from app.helpers.api_response import BaseApiResponse

from app import context as ctx
from app.helpers.auth import require_admin
from app.helpers.upload import allowed_file, ALLOWED_IMG_EXTENSIONS
from app.models.settings import Settings


@settings_api.route('/all')
class All(Resource):

    def get(self):
        res = BaseApiResponse()

        settings = ctx.db.session.query(Settings).first()
        if not settings:
            res.add_error("Settings not found")
            return res.make(), 404

        res.data = {
            "settings": settings.to_json()
        }

        res.data["settings"]["state"] = settings.get_ctf_state()

        return res.make()


@settings_api.route('/access')
class Access(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        new_settings = request.get_json()
        required = ["not_before", "not_after", "enforce_access_restriction"]

        settings = ctx.db.session.query(Settings).first()
        if not settings:
            res.add_error("Settings not found")
            return res.make(), 404

        if not all(req in settings.to_json().keys() for req in required):
            res.add_error(f"Missing one of the following value : {required}")
            return res.make(), 400

        try:
            settings.not_before = dateutil.parser.isoparse(new_settings["not_before"]).astimezone(UTC)
        except ValueError:
            return res.make(), 400
        try:
            settings.not_after = dateutil.parser.isoparse(new_settings["not_after"]).astimezone(UTC)
        except ValueError:
            return res.make(), 400

        settings.enforce_access_restriction = new_settings["enforce_access_restriction"]

        ctx.db.session.commit()

        return res.make()


@settings_api.route('/game')
class Game(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        new_settings = request.get_json()
        required = ["enable_teams", "freeze_scoreboard"]

        settings = ctx.db.session.query(Settings).first()
        if not settings:
            res.add_error("Settings not found")
            return res.make(), 404

        if not all(req in settings.to_json().keys() for req in required):
            res.add_error(f"Missing one of the following value : {required}")
            return res.make(), 400

        settings.enable_teams = new_settings["enable_teams"]
        settings.freeze_scoreboard = new_settings["freeze_scoreboard"]
        settings.allow_registration = new_settings["allow_registration"]

        ctx.db.session.commit()

        return res.make()


@settings_api.route('/logo/picture')
class UploadAvatar(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        logo = request.files["logo"]
        if not logo or not allowed_file(logo.filename, ALLOWED_IMG_EXTENSIONS):
            abort(400)

        settings = ctx.db.session.query(Settings).first()
        if not settings:
            res.add_error("Settings not found")
            return res.make(), 404

        logo_path = current_app.config['LOGO_IMG_PATH']
        logo.save(logo_path)
        settings.logo = logo_path.replace(current_app.config["DIST_DIR"], "")
        ctx.db.session.commit()

        return res.make()


@settings_api.route('/logo/sizing')
class AvatarSizing(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        data = request.get_json()
        required = ["height", "width"]

        if not all(req in data.keys() for req in required):
            abort(400)

        height = data.get("height")
        width = data.get("width")

        if type(height) is not int or type(width) is not int:
            abort(400)

        settings = ctx.db.session.query(Settings).first()
        if not settings:
            res.add_error("Settings not found")
            return res.make(), 404

        settings.logo_height = height
        settings.logo_width = width
        ctx.db.session.commit()

        return res.make()


@settings_api.route('/homepage')
class HomePage(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        data = request.get_json()

        if "content" not in data.keys():
            abort(400)

        content = data.get("content")

        if not content:
            abort(400)

        settings = ctx.db.session.query(Settings).first()
        if not settings:
            res.add_error("Settings not found")
            return res.make(), 404

        settings.homepage = content
        ctx.db.session.commit()

        return res.make()
