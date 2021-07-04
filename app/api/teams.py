# from pprint import pprint
import os
from uuid import uuid4

from flask import request, current_app
from flask_restx import Resource, abort
from sqlalchemy import exc
from sqlalchemy.sql import func
from werkzeug.utils import redirect

from app.api import teams_api
from app.helpers.api_response import TeamApiResponse, ListTeamsApiResponse, BaseApiResponse
from app.helpers.auth import check_user_session
from app.helpers.teams import upgrade_team_with_stats, require_team_owner, require_teams_enabled
from app.helpers.upload import allowed_file, ALLOWED_IMG_EXTENSIONS
from app.helpers.users import import_user, require_user_self
from app.models.teams import Teams

import app.context as ctx
from app.models.users import Users


@teams_api.route('/<string:team_id>')
class Get(Resource):

    @require_teams_enabled
    @import_user
    def get(self, team_id, user=None):
        res = TeamApiResponse()
        if team_id == "join":
            if not user.team:
                return res.make(), 204

            res = BaseApiResponse()
            res.data = {
                "team_id": user.team.id
            }
            return res.make(), 301

        team = ctx.db.session.query(Teams).filter_by(id=team_id).first()
        if not team:
            res.add_error("Team not found")
            return res.make(), 404

        res.set_team(team, with_users=True, with_flags=True)
        res.team = upgrade_team_with_stats(res.team, user)
        # res.team["is_owner"] = user.team.id == team.id

        # ranking = ctx.db.session.query(func.count(team.id)).filter(team.score > Teams.score).as_scalar()
        # print(ranking)
        # res.team["ranking"] = ranking + 1
        # pprint(res.make())

        return res.make()


@teams_api.route('/all')
class List(Resource):

    @require_teams_enabled
    def get(self):
        res = ListTeamsApiResponse()

        teams = ctx.db.session.query(Teams).all()
        if not teams:
            res.add_error("No teams found")
            return res.make()

        res.set_teams(teams, with_users=True)

        for team in res.teams:
            team["score"] = sum([user["score"] for user in team["users"]])

        res.teams = list(sorted(res.teams, key=lambda x: x["score"], reverse=True))

        return res.make()


@teams_api.route('/join/<string:team_name>')
class join(Resource):

    @require_teams_enabled
    def post(self, team_name):
        res = BaseApiResponse()
        data = request.get_json()
        user_data = data.get("user")
        team_data = data.get("team")

        if not user_data:
            res.add_error("Missing user data")
            return res.make(), 400

        if not team_data:
            res.add_error("Missing team data")
            return res.make(), 400

        team = ctx.db.session.query(Teams).filter_by(name=team_name).first()
        if not team:
            res.add_error("Team not found")
            return res.make(), 404

        user = ctx.db.session.query(Users).filter_by(id=user_data["id"]).first()
        if not user:
            res.add_error("User not found")
            return res.make(), 404

        if not team.check_password(team_data["password"]):
            res.add_error("Invalid password")
            return res.make()

        user.team_id = team.id
        ctx.db.session.commit()

        res.data = {
            "team_id": team.id
        }

        return res.make()


@teams_api.route('/new')
class Create(Resource):

    @require_teams_enabled
    def post(self):
        res = BaseApiResponse()
        data = request.get_json()

        team_data = data.get("team")
        if not team_data:
            res.add_error("Missing team data")
            return res.make(), 500

        user_data = data.get("user")
        if not user_data:
            res.add_error("Missing user data")
            return res.make(), 500

        user = ctx.db.session.query(Users).filter_by(id=user_data["id"]).first()
        if not user:
            res.add_error("Unknown user")
            return res.make(), 404

        new_team = Teams(id=uuid4(), name=team_data["name"], avatar=team_data.get("avatar", ""), owner=user.id)
        new_team.set_password(team_data["password"])

        try:
            ctx.db.session.add(new_team)
            ctx.db.session.flush()
        except exc.IntegrityError:
            ctx.db.session.rollback()
            existing_team = ctx.db.session.query(Teams).filter_by(name=team_data["name"]).first()

            if existing_team and existing_team.deleted:
                res.add_error("An existing team with this name already exist")
                return res.make(), 409
            elif existing_team:
                res.add_error("An existing team with this name already exist")
                return res.make(), 409

        user.team_id = new_team.id
        ctx.db.session.commit()

        res.data = {
            "team_id": new_team.id
        }

        return res.make(), 201


@teams_api.route('/edit/<string:team_id>')
class Edit(Resource):

    @require_teams_enabled
    @require_team_owner
    def post(self, team_id):
        res = BaseApiResponse()
        new_team = request.get_json()

        old_team = Teams.query.filter_by(id=team_id).first()
        if not old_team:
            res.add_error("Team not found")
            return res.make(), 404

        old_team.name = new_team["name"]
        old_team.avatar = new_team["avatar"]
        old_team.owner = new_team["owner"]

        ctx.db.session.commit()

        return res.make()


@teams_api.route('/disband/<string:team_id>')
class Disband(Resource):

    @require_teams_enabled
    @require_team_owner
    def post(self, team_id):
        res = BaseApiResponse()

        team = Teams.query.filter_by(id=team_id).first()
        if not team:
            res.add_error("Team not found")
            return res.make(), 404

        for user in team.users:
            user.team_id = None

        Teams.query.filter_by(id=team.id).delete()
        ctx.db.session.commit()

        return res.make()


@teams_api.route('/leave')
class Leave(Resource):

    @require_teams_enabled
    @import_user
    def post(self, user=None):
        res = BaseApiResponse()
        session = request.cookies.get('CHATSUBO-SESSION')
        if not check_user_session(user.id, session):
            abort(401)
            return

        user.team_id = None
        ctx.db.session.commit()

        return res.make()


@teams_api.route('/avatar/<string:team_id>')
class UploadAvatar(Resource):

    @require_teams_enabled
    @import_user
    def post(self, team_id, user=None):
        res = BaseApiResponse()

        avatar = request.files["avatar"]
        if not avatar or not allowed_file(avatar.filename, ALLOWED_IMG_EXTENSIONS):
            abort(400)

        unique_filename = f"{uuid4()}.{avatar.filename.rsplit('.', 1)[1].lower()}"
        avatar_path = os.path.join(current_app.config['TEAMS_AVATARS_FOLDER'], unique_filename)
        avatar.save(avatar_path)

        backend_path = avatar_path.replace(current_app.config["DIST_DIR"], "")
        if team_id != "temp":
            team = Teams.query.filter_by(id=team_id).first()
            if user.team_id != team.id:
                abort(401)

            team.avatar = backend_path
            ctx.db.session.commit()

        res.data = {
            "path": backend_path
        }

        return res.make()
