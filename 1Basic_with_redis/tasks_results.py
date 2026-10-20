from celery_config import celery_app
from celery.result import AsyncResult

def get_task_result(task_id):
    res = AsyncResult(task_id, app=celery_app)
    if res.status == "PENDING":
        print("Task is still pending...")
    else:
        print(f"Task status: {res.status}")
        print(f"Task result: {res.result}")

# Note = All the attributes and methods of the job object are also available in the AsyncResult object, so you can use them to check the status, get the result, or handle retries for a task using its ID.

if __name__ == "__main__":
    task_id = "d014d758-c4b0-4552-b0a0-9602d374e171"
    get_task_result(task_id)

