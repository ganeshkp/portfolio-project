

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio2.settings")
app = Celery("portfolio2")  # portfolio is project name
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-minute-contrab': {
        'task': 'send_blog_mail',
        'schedule': crontab(minute='*/5'),  # every 5 minutes
        'args': (16, 16),
    },
    # 'add-every-5-seconds': {
    #     'task': 'multiply_two_numbers',
    #     'schedule': 5.0,  # in seconds
    #     'args': (16, 16)
    # },
    # 'add-every-30-seconds': {
    #     'task': 'tasks.add',
    #     'schedule': 30.0,
    #     'args': (16, 16)
    # },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
