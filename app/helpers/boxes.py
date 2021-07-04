from flask import request
from sqlalchemy import or_
from sqlalchemy.testing import in_

import app.context as ctx
from app.models.users import Users
from app.models.users_flags import UsersFlags


def is_box_completed_by(box, user=None):
    if not user:
        session_cookie = request.cookies.get('CHATSUBO-SESSION')
        if not session_cookie:
            return

        user = ctx.db.session.query(Users).filter_by(session=session_cookie).first()
        if not user:
            return

    box_flags_id = [f["id"] for f in box["flags"]]
    submissions = ctx.db.session.query(UsersFlags).filter_by(user_id=user.id).filter(UsersFlags.flag_id.in_(box_flags_id)).all()

    valid_submissions = [sub for sub in filter(lambda sub: sub.valid, submissions)]
    if len(valid_submissions) != len([f for f in box["flags"] if not f["deleted"]]):
        return False

    for flag in box["flags"]:
        if flag["id"] not in [sub.flag_id for sub in valid_submissions]:
            return False

    return True


def get_validated_flags(box, user=None):
    if not user:
        session_cookie = request.cookies.get('CHATSUBO-SESSION')
        if not session_cookie:
            return

        user = ctx.db.session.query(Users).filter_by(session=session_cookie).first()
        if not user:
            return

    box_flags_id = [f["id"] for f in box["flags"]]
    submissions = ctx.db.session.query(UsersFlags).filter_by(user_id=user.id).filter(UsersFlags.flag_id.in_(box_flags_id)).all()

    valid_flags = []
    valid_submissions_flags_id = [sub.flag_id for sub in filter(lambda sub: sub.valid, submissions)]
    for f in box["flags"]:
        if f["id"] in valid_submissions_flags_id:
            f["category"] = box["category"]["name"]
            valid_flags.append(f)

    return valid_flags


def upgrade_box_with_stats(box, user=None):
    if not user:
        session_cookie = request.cookies.get('CHATSUBO-SESSION')
        if not session_cookie:
            return

        user = ctx.db.session.query(Users).filter_by(session=session_cookie).first()
        if not user:
            return

    box["completed"] = is_box_completed_by(box, user=user)
    box["validated_flags"] = []
    if user.flags:
        # box["validated_flags"] = [flag.to_json() for flag in filter(lambda f: False if f.deleted else f.box_id == box["id"], user.flags)]
        box["validated_flags"] = get_validated_flags(box, user=user)
