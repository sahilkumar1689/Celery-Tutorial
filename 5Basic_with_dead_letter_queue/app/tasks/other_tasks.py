from celery.exceptions import Reject
from celery import shared_task

@shared_task(queue="math_queue",rate_limit="5/m")
def add(x, y):
    return x + y

@shared_task(queue="math_queue",rate_limit="5/m")
def mul(x, y):
    return x * y

@shared_task(queue="cpu_queue",rate_limit="5/m")
def square(x):
    return x * x

@shared_task(bind=True, acks_late=True)
def fail_task(self):
    raise Reject("Force DLQ", requeue=False)