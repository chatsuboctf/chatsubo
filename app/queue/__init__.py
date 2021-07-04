from os import environ

from celery import Celery


def make_celery(app=None):
    broker = environ.get("BROKER_URL", "pyamqp://guest@localhost//")
    backend = environ.get("BACKEND", "rpc://")

    celery_app = Celery('celery_app', backend=backend, broker=broker)

    celery_app.conf.update(
        result_expires=3600
    )

    if app:
        celery_app.conf.update(app.config)

    celery_app.autodiscover_tasks()

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery_app = make_celery()
