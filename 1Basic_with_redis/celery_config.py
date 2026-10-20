from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["celery_tasks"]
)

celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]

# These configuration can set the job_id expiration time by default celery set it to 1 day.It means you can access one day old jobs result only.You can set it to accordingly.

# celery_app.conf.result_expires = 60 * 60 * 24 * 7   # 7 days
# # or
# celery_app.conf.result_expires = None             # Never delete


# Note = 1. It is very important to keep that in mind, if you change any thing in celery_config file or even celery tasks file you need to restart the celery workers.
