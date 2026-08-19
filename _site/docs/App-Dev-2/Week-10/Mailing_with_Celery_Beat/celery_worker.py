from celery import Celery, Task
from app import app
from celery.schedules import crontab

celery_app = Celery('tasks', broker='redis://localhost:6379/1', backend='redis://localhost:6379/2', include=['tasks'])


class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
        

celery_app.Task = FlaskTask        

celery_app.conf.timezone = 'Asia/Kolkata'

celery_app.conf.beat_schedule = {
    'monthly-report': {
        'task': 'tasks.generate_monthly_report',
        'schedule': crontab(hour=22, minute=10, day_of_month=14),
        # 'schedule': 10,
    },
    'daily-reminder': {
        'task': 'tasks.send_daily_reminder',
        'schedule': crontab(hour=22, minute=10),
        # 'schedule': 10,
    }
}