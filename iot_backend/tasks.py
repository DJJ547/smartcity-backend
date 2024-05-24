# myapp/tasks.py
from celery import shared_task

# this celery task emulate a real api that fetches data from a .txt file every five minutes
@shared_task
def my_task():
    # Your task code here
    print("This task runs every five minutes!")