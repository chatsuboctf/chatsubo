from functools import wraps

from flask import request
from flask_restx import abort

import app.context as ctx
from app.helpers.auth import check_user_session
from app.models.users import Users


def require_user_self(fn):
    @wraps(fn)
    def check_self_session(*args, **kwargs):
        try:
            target_user_id = request.get_json().get("id")
        except AttributeError:
            target_user_id = kwargs.get("user_id")
        session = request.cookies.get('CHATSUBO-SESSION')
        if not check_user_session(target_user_id, session):
            abort(401)
            return
        # if not session:
        #     abort(401)
        #     return
        #
        # user = ctx.db.session.query(Users).filter_by(session=session).first()
        # if not user:
        #     abort(401)
        #     return
        #
        # if not user.id == target_user_id:
        #     abort(401)
        # else:
        #     return fn(*args, **kwargs)
        return fn(*args, **kwargs)

    return check_self_session


def import_user(fn):
    @wraps(fn)
    def fetch(*args, **kwargs):
        user = fetch_user()
        if not user:
            abort(401)

        return fn(user=user, *args, **kwargs)

    return fetch


def fetch_user():
    session = request.cookies.get('CHATSUBO-SESSION')
    if not session:
        return None

    user = ctx.db.session.query(Users).filter_by(session=session).first()
    if not user:
        return None

    return user
