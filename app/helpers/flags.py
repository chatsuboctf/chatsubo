from functools import wraps

import app.context as ctx
from flask_restx import abort

from app.models.settings import Settings


def require_allowed_submissions(fn):
    @wraps(fn)
    def check_allowed_submissions(*args, **kwargs):
        settings = ctx.db.session.query(Settings).first()
        if not settings:
            abort(500)
            return

        if settings.freeze_scoreboard:
            abort(403)
        else:
            return fn(*args, **kwargs)

    return check_allowed_submissions

