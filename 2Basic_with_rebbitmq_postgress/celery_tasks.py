from celery_config import celery_app
from celery.exceptions import SoftTimeLimitExceeded
import random
import time


# 1. Creating a simple task.
@celery_app.task
def add(x, y):
    time.sleep(12)   # simulate heavy work
    return x + y

# 2. Create a production ready task with retry and error handling.

# (i) Here we set the manual configuration,best for the db related or custom retry strategy.
@celery_app.task(
    bind=True,                # It is the most important attribute in the task decorator. It allows the task to access its own state and retry mechanism through the self parameter. When bind=True is set, the first argument of the task function will be the task instance itself, which can be used to call self.retry() for retrying the task in case of failure.In simple words in order to access all the metadata and methods of the task object we need to set bind=True in the task decorator.
    max_retries=3,
    # default_retry_delay=5,  # it used to specify the delay between mulitple retires.
    acks_late=True,           # It ensures that the task is acknowledged only after it has been successfully executed. If a worker crashes or fails to complete the task, it will be re-queued and retried by another worker, preventing task loss.
    soft_time_limit=10,       # It sets a soft time limit for the task execution. If the task exceeds this time limit, a SoftTimeLimitExceeded exception will be raised, allowing you to handle it gracefully within the task code. This is useful for preventing tasks from running indefinitely and consuming resources unnecessarily.
    time_limit=15             # It sets a hard time limit for the task execution. If the task exceeds this time limit, it will be forcefully terminated by the worker, and a TimeLimitExceeded exception will be raised. This is a more aggressive way to ensure that tasks do not run for too long, but it may lead to incomplete or inconsistent results if the task is terminated before it finishes its work.
)
def add(self, x, y):
    try:
        time.sleep(2)

        if random.choice([True, False]):
            raise Exception("Random failure!")

        return x + y

    except SoftTimeLimitExceeded:
        print("Task took too long!")
        raise

    except Exception as exc:
        # Here,we are implementing an exponential backoff strategy for retries.
        countdown = 2 ** self.request.retries
        raise self.retry(exc=exc, countdown=countdown)

# (ii) Automatic retry, best for the task which depend on the external API or service and we want to retry on specific exception.

# Rough example:
from celery import shared_task

def do_something(payload):
    pass;

@shared_task(
    bind=True,                              # Access task instance (self)
    autoretry_for=(Exception,),             # Auto-retry for specified exceptions
    retry_backoff=True,                     # Enable exponential backoff
    retry_backoff_max=600,                  # Max backoff delay (10 minutes)
    retry_jitter=True,                      # Add randomness to avoid retry storms
    max_retries=5,                          # Stop after 5 attempts
    acks_late=True,                         # Acknowledge only after successful completion
    reject_on_worker_lost=True,             # Requeue if worker crashes
    soft_time_limit=60,                     # Graceful timeout
    time_limit=90                           # Hard kill timeout
)
def production_task(self, payload):
    # idempotent logic here
    return do_something(payload)