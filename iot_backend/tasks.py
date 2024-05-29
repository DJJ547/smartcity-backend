# myapp/tasks.py
from celery import shared_task
from .mongodb import MongoDBProcessor
from datetime import datetime, timedelta
import pytz

# this celery task emulate a real api that fetches data from a .txt file every five minutes
@shared_task
def update_flow_speed_congestion_every_5min():
    current_time = pytz.utc.localize(datetime.now())
    mongodb = MongoDBProcessor()
    mongodb.update_all_flow_speed_congestion_in_5min(current_time)
    print("This task runs every five minutes!")