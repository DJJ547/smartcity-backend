# myapp/tasks.py
from celery import shared_task
from datetime import datetime, timedelta
from .mysql import MysqlProcessor
import pytz

# this celery task emulate a real api that fetches data from a .txt file every five minutes
@shared_task
def update_incident_every_1min():
    current_time = pytz.utc.localize(datetime.now())
    print(current_time)
    mysql = MysqlProcessor()
    mysql.update_all_chp_incidents_in_1minute(current_time)
    print("This task runs every one minute!")
    