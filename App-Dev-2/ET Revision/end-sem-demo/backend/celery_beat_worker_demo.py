# Topic 11 – Celery Worker + Beat (Short Demo)
# Prerequisites:
#   pip install celery redis
#   redis-server
# Run worker:
#   celery -A celery_beat_worker_demo.celery_app worker --loglevel=info
# Run beat:
#   celery -A celery_beat_worker_demo.celery_app beat --loglevel=info

from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/1",
    backend="redis://localhost:6379/2",
)

celery_app.conf.timezone = "Asia/Kolkata"
celery_app.conf.beat_schedule = {
    "print-reminder-every-morning": {
        "task": "send_daily_reminder",
        "schedule": crontab(hour=8, minute=0),
    }
}


@celery_app.task(name="send_daily_reminder")
def send_daily_reminder():
    print("Reminder task executed by worker.")
    return "done"
