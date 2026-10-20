from celery_config import celery_app
from app.tasks import *

r1 = add.delay(2, 3)
# r2 = mul.delay(4, 5)
r2 = mul.apply_async(args=(4, 5), priority=5) # Here we set the priority of this task to 5. Only works in rabbitmq.

r3 = square.delay(6)

print(r1.id)
print(r2.id)
print(r3.id)

# Note = 1. You can only set priority using the apply_async method, not with the delay method.
# 2. Argument in apply_async method:

# task.apply_async(
#     args=None,
#     kwargs=None,

#     countdown=None,  # it is used to specify the number of seconds to delay the execution of the task. For example, if you set countdown=10, the task will be executed 10 seconds after it is called.

#     eta=None,        # it is used to specify the exact date and time when the task should be executed. For example, if you set eta=datetime(2023, 1, 1, 12, 0, 0), the task will be executed on January 1, 2023, at 12:00 PM.

#     priority=None,   # it is used to specify the priority of the task. Higher priority tasks will be executed before lower priority ones. The priority can be an integer value, where a lower number indicates higher priority. For example, if you set priority=5, the task will have a priority level of 5. Only works in rabbitmq.

#     queue=None,      # it is used to specify the name of the queue to which the task should be sent. If you have multiple queues configured in your Celery application, you can use this argument to route the task to a specific queue. For example, if you set queue="math_queue", the task will be sent to the "math_queue" for processing. Only works in rabbitmq.

#     routing_key=None,

#     expires=None,   # it is used to specify the expiration time for the task. If the task is not executed before the specified time, it will be discarded and will not be executed at all. For example, if you set expires=3600, the task will expire after 1 hour (3600 seconds) if it has not been executed.

#     retry=None,
# )