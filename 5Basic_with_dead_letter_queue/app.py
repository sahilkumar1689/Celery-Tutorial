from celery_config import celery_app
from app.tasks import *


# task1 = fail_task.apply_async(queue="math_queue")

r1 = add.delay(2, 3)
r2 = square.delay(6)

print(r1.id)
print(r2.id)
