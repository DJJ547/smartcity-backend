from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# celery -A smartcity_backend worker -l info --pool=solo
# celery -A smartcity_backend beat -l info

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity_backend.settings')

app = Celery('smartcity_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-every-5-minutes': {
        'task': 'iot_backend.tasks.get_speed_every_5min',
        'schedule': crontab(minute='*/5'),
    },
}

