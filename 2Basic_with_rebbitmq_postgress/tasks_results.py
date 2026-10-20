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
    # task_id = "3909089b-796a-4a98-8e3b-633ead201287"
    task_id = "a52c70bf-d5ca-4a63-952f-20b05d0fc8ea"
    # task_id = "adc8c656-7f69-4a8a-a806-8f21ef8035e9"
    get_task_result(task_id)

