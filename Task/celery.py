import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Task.settings')

app = Celery('Task')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'board.tasks.weekly_news',
        #'schedule': crontab(),  # каждую минуту
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),  # Каждый понедельник в 8:00
        'args': (),
    },
}