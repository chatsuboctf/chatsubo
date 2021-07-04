# from app.queue.celery_app import celery_app
from abc import ABC

import celery
from datetime import datetime

import app.context as ctx
from app.models.boxes import Boxes
from app.models.sessions import Sessions


class CallbackTask(celery.Task, ABC):
    def on_success(self, retval, task_id, args, kwargs):
        ctx.db.session.commit()
        session = ctx.db.session.query(Sessions).filter_by(task_id=task_id).first()
        if not session:
            return

        session.state = "running"
        session.started_at = datetime.now()
        ctx.db.session.commit()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        ctx.db.session.commit()
        session = ctx.db.session.query(Sessions).filter_by(task_id=task_id).first()
        if not session:
            return

        session.state = "failure"
        ctx.db.session.commit()


@ctx.celery_app.task(base=CallbackTask, track_started=True, max_retries=0)
def start_box(realm: str, template: str, session_id: str, duration: int):
    err = ctx.providers.start_dynamic_instance(realm, template, session_id)
    if err is not None:
        session = Sessions.query.filter_by(id=session_id).first()
        if not session:
            return None

        ctx.db.session.delete(session)
        ctx.db.session.commit()
        return err

    duration_seconds = duration * 60
    stop_box.apply_async(kwargs={"realm": realm, "session_id": session_id}, countdown=duration_seconds)

    return None


@ctx.celery_app.task(base=CallbackTask, max_retries=0)
def stop_box(realm: str, session_id: str):
    session = Sessions.query.filter_by(id=session_id).first()
    if not session:
        # Already stopped, we pass
        return None

    ctx.db.session.delete(session)
    ctx.db.session.commit()

    return ctx.providers.stop_dynamic_instance(realm, session_id)
