from celery import Celery

celery_app = Celery(
    "worker",

    # RabbitMQ (broker)
    broker="amqp://admin:admin@localhost:5672//",

    # PostgreSQL (result backend)
    backend="db+postgresql://celery:celery@localhost:5432/celerydb",
    include=["celery_tasks"]   # it is used to create a app instance level tasks registry, so we can import the task directly from the app instance instead of importing the task function directly from the tasks module.Not recommended for the production environment but it is good for the development and testing purpose.
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_extended=True,
)

# Production grade and recommneded task configuration:
celery_app.autodiscover_tasks(["app"])
# Note = 1. It is used to create the shared task which does not bound to any celery app instance.
# 2. You need to create a app folder which contains the files with "tasks.py" name strictly.And you simply create your task with the help of the shared_task decorator and it will automatically register the task in the app instance level registry and you can import the task directly from the app instance instead of importing the task function directly from the tasks module.