from celery_config import celery_app
from celery.result import AsyncResult

def get_task_result(task_id):
    res = AsyncResult(task_id, app=celery_app)
    if res.status == "PENDING":
        print("Task is still pending...")
    else:
        print(f"Task status: {res.status}")
        print(f"Task result: {res.result}")


if __name__ == "__main__":

    task_id = "30f484bd-561a-4adc-b1e0-8b4169d7f678"

    get_task_result(task_id)

