from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity_backend.settings')

app = Celery('smartcity_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-every-5-minutes': {
        'task': 'iot_backend.tasks.my_task',
        'schedule': crontab(minute='*/5'),
    },
}

