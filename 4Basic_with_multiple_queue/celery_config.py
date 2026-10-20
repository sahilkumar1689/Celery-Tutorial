from celery import Celery
from kombu import Queue,Exchange

celery_app = Celery(
    "worker",
    broker="amqp://admin:admin@localhost:5672//",
    backend="redis://localhost:6379/0",
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_extended=True,

    # Declare queues here:
    task_queues=(
        Queue("math_queue",
            Exchange("math_queue"),
            routing_key="math_queue",
            queue_arguments={"x-max-priority": 10}  # Here we set the maximum priority for the math_queue to 0-10.Only works in rabbitmq.Rabbitmq queues are immutable.
        ),
        Queue("cpu_queue"),
    ),

    # Also set task_routes to route tasks to the appropriate queues:
    # task_routes = {
    # "app.tasks.math_tasks.add": {"queue": "math_queue"},
    # "app.tasks.math_tasks.mul": {"queue": "math_queue"},
    # "app.tasks.math_tasks.square": {"queue": "cpu_queue"},
    # }

    # Also we can set rate limits for specific tasks using task_annotations:
    # task_annotations = {
    # "app.tasks.email.send_email": {"rate_limit": "10/s"},
    # }
)

celery_app.autodiscover_tasks(["app"])