from functools import wraps

from flask import request
from flask_restx import abort

import app.context as ctx
from app.models.categories import Categories
from app.models.settings import Settings
from app.models.users import Users


def require_teams_enabled(fn):
    @wraps(fn)
    def check_teams_enable(*args, **kwargs):
        settings = ctx.db.session.query(Settings).first()
        if not settings:
            abort(500)
            return

        if settings.enable_teams:
            return fn(*args, **kwargs)
        else:
            abort(403)

    return check_teams_enable


def require_team_owner(fn):
    @wraps(fn)
    def check_owner_session(*args, **kwargs):
        session = request.cookies.get('CHATSUBO-SESSION')
        if not session:
            abort(401)
            return

        user = ctx.db.session.query(Users).filter_by(session=session).first()
        if not user:
            abort(401)
            return

        if not user.team.id != user.team.owner:
            abort(401)
        else:
            return fn(*args, **kwargs)

    return check_owner_session


def upgrade_team_with_stats(team, user):
    # real_users = ctx.db.session.query(Users).filter_by(team_id=team["id"]).all()
    categories = ctx.db.session.query(Categories).all()

    team_flags = {}
    for team_user in team["users"]:
        for flag in team_user["flags"]:
            team_flags[flag["id"]] = flag

    team["flags"] = list(team_flags.keys())
    team["categories"] = [cat.to_json(with_unreleased=user.admin, with_boxes=True, with_flags=True) for cat in categories]

    for cat in team["categories"]:
        for box in cat["boxes"]:
            try:
                for flag in box["flags"]:
                    if flag["id"] not in team_flags:
                        raise NextBox

                box["completed"] = True
            except NextBox:
                pass

    team["is_owner"] = user.id == team["owner"]

    team["score"] = sum([flag["points"] for flag in team_flags.values()])

    return team


class NextBox(Exception):
    pass
