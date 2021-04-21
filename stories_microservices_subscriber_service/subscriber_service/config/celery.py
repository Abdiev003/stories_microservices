from celery import Celery
from celery.schedules import crontab
from ..app import app as flask_app

# Add periodic tasks
celery_beat_schedule = {
    "time_scheduler": {
        "task": "send_mail_to_subscribers",
        # Run every second
        "schedule": 10.0,
        # "schedule": crontab(hour=11, minute=24),
    }
}

celery = Celery(flask_app.name, include=['subscriber_service.tasks',])
celery.conf.update(
    broker_url=flask_app.config["CELERY_BROKER_URL"],
    timezone="Asia/Baku",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    beat_schedule=celery_beat_schedule,
)

celery.conf.update(flask_app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask

'''
RUN command:
celery -A subscriber_service.config.celery worker --loglevel=INFO -B
'''