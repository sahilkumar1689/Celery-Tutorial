from celery import Celery
from kombu import Queue,Exchange

celery_app = Celery(
    "worker",
    broker="amqp://admin:admin@localhost:5672//",
    backend="redis://localhost:6379/0",
)

main_exchange = Exchange("main_exchange", type="direct")
dlx_exchange = Exchange("dlx_exchange", type="direct")

celery_app.conf.task_default_exchange = "main_exchange"
celery_app.conf.task_default_routing_key = "math_queue"

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_extended=True,

    # Declare a dead letter queues = It is nothing but a simple queue that is used to store the failed tasks. When a task fails, it is automatically moved to the dead letter queue for later analysis and debugging. This allows you to keep track of failed tasks and take appropriate actions to fix them without losing any important information.
    task_queues=(
        # Main Queue
        Queue(
            "math_queue",
            main_exchange,
            routing_key="math_queue",
            queue_arguments={
                "x-dead-letter-exchange": "dlx_exchange",
                "x-dead-letter-routing-key": "dead_math_queue",
            },
        ),

        # Dead Letter Queue
        Queue(
            "dead_math_queue",
            dlx_exchange,
            routing_key="dead_math_queue",
        ),
        
        Queue(
            "cpu_queue",
            main_exchange,
            routing_key="cpu_queue",
        ),
    ),

    # Beat Schedule = It is a built-in scheduler in Celery that allows you to schedule tasks to run at specific intervals or times. It is based on the concept of periodic tasks, which are tasks that are executed repeatedly according to a defined schedule. The beat scheduler runs in the background and checks for scheduled tasks at regular intervals, executing them when their scheduled time arrives.
    beat_schedule={
        "run-every-minute": {
            "task": "app.tasks.other_tasks.add",
            "schedule": 2.0,    
            "args": (2, 3),
        },
    }
)

celery_app.autodiscover_tasks(["app"])