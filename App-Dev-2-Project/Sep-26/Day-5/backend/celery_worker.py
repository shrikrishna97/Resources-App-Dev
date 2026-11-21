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
    'monthly-user-report': {
        'task': 'tasks.monthly_user_report',
        # 'schedule': 30.0,
        'schedule' : crontab(hour=0, minute=0, day_of_month='1'),  # Run on the first day of every month at midnight
    },
    'daily-reminder': {
        'task': 'tasks.send_daily_reminder',
        'schedule': crontab(hour=19, minute=13), 
        # 'schedule': 20.0,  # Run every day at 9:00 AM
    }
}

