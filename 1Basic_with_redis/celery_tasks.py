from celery_config import celery_app
import time

@celery_app.task
def add(x, y):
    time.sleep(12)   # simulate heavy work
    return x + y
