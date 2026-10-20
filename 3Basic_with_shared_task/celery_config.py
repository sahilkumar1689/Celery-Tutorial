from celery import Celery

celery_app = Celery(
    "worker",
    broker="amqp://admin:admin@localhost:5672//",
    backend="db+postgresql://celery:celery@localhost:5432/celerydb",
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_extended=True,
)

celery_app.autodiscover_tasks(["app"])