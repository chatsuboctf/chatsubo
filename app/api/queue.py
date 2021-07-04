import celery.result
from flask_restx import Resource

from app.api import queue_api
from app.context import celery_app
from app.helpers.api_response import BaseApiResponse

from app import context as ctx
from app.models.sessions import Sessions


@queue_api.route('/<string:task_id>')
class All(Resource):

    def get(self, task_id):
        res = BaseApiResponse()
        session = Sessions.query.filter_by(task_id=task_id).first()
        if not session:
            return res.make(), 404

        res.data = {
            "state": session.state,
            "position": 1,
            "queueLen": 1
        }

        if session.state == "pending" or session.state == "success":
            queue = []
            active = []
            insp = ctx.celery_app.control.inspect()

            # Flatten each node's data
            if full_queue := insp.scheduled():
                queue = [el for l in full_queue.values() for el in l]

            if full_active := insp.active():
                active = [el for l in full_active.values() for el in l]

            current_state = celery_app.AsyncResult(task_id).state
            print("HEY", current_state)
            if celery_app.AsyncResult(task_id).state != session.state:
                session.state = current_state.lower()
                ctx.db.session.commit()

            try:
                res.data["position"] = [task["id"] for task in queue].index(task_id)
            except ValueError:
                pass
            except KeyError:
                res.data["position"] = -1
            res.data["queueLen"] = len(queue) + len(active)

        return res.make()
