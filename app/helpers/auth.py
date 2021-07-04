from functools import wraps

from flask import request, abort

from app.models.users import Users

import app.context as ctx


def check_user_session(target_user_id, session):
    user = ctx.db.session.query(Users).filter_by(session=session).first()
    if not user:
        return False

    return user.id == target_user_id


def email_exists(email, ctx):
    return ctx.db.session.query(Users).filter_by(email=email).first() is not None


def username_exists(username, ctx):
    return ctx.db.session.query(Users).filter_by(username=username).first() is not None


def require_admin(fn):
    @wraps(fn)
    def check_admin_session(*args, **kwargs):
        session = request.cookies.get('CHATSUBO-SESSION')
        if not session:
            abort(401)
            return

        user = ctx.db.session.query(Users).filter_by(session=session).first()
        if not user:
            abort(401)
            return

        if not user.admin:
            abort(401)
        else:
            return fn(*args, **kwargs)

    return check_admin_session


def morph_admin(fn):
    @wraps(fn)
    def check_admin_session(*args, **kwargs):
        is_admin = False
        session = request.cookies.get('CHATSUBO-SESSION')
        user = ctx.db.session.query(Users).filter_by(session=session).first()

        if user and user.admin:
            is_admin = True

        return fn(is_admin=is_admin, *args, **kwargs)

    return check_admin_session
