from celery_tasks import add

job = add.delay(3, 3)

# Methods and the attributes of the job object:

# 1. job.id = It is the unique identifier for the task.
print(job.id)

# 2. job.status = It gives the current status of the task. It can be PENDING, STARTED, SUCCESS, FAILURE, etc.
print(job.status)

# 3. job.result = It holds the result of the task once it is completed.
print(job.result)

# 4. job.get(timeout=10) = This method is used to wait for the task to complete and retrieve the result. The timeout parameter specifies how long to wait for the result before raising an exception.
print(dir(job))
# print(job.get(timeout=10))  # It is only used when you want to wait and get the result.

# 5. job.ready() = This method returns True if the task has finished processing (either successfully or with an error), and False otherwise.
print(job.ready())

# 6. job.successful() = This method returns True if the task completed successfully, and False if it failed or is still pending.
print(job.successful())

# 7. job.failed() = This method returns True if the task failed, and False if it completed successfully or is still pending.
print(job.failed())

# 8. job.traceback = If the task failed, this attribute contains the traceback of the error that occurred during task execution.
print(job.traceback)

# 9. job.date_done = This attribute holds the timestamp of when the task was completed.
print(job.date_done)

# 10. job.revoke() = This method is used to revoke a task, preventing it from being executed if it has not already started. You can also specify terminate=True to kill the task if it is currently running.
# job.revoke(terminate=True)  # Use this with caution, as it can lead to data corruption if the task is in the middle of processing.

# 11 job.info = This attribute contains additional information about the task, such as the arguments passed to it and any custom metadata you may have set when defining the task.Also tell how many times the task has been retried if you have configured retries for the task.It can also tell how much task is currently running and how much is pending like a progress bar.
print(job.info)

# 12. job.retry() = This method is used to retry a task that has failed. You can specify the number of retries and the delay between retries.
# job.retry(countdown=5)  # This will retry the task after a delay of 5 seconds.

# 13. job.forget() = This method is used to remove the task result from the backend, which can be useful for cleaning up after a task has completed and you no longer need the result.
# job.forget()  # Use this to clean up the result after you have retrieved it

# 14. job.on_success(callback) = This method allows you to specify a callback function that will be called when the task completes successfully. The callback function will receive the result of the task as an argument.Very useful when you want to perform some action after the task has completed, such as updating a database record or sending a notification via webhooks. You can also use job.on_failure(callback) to specify a callback function that will be called if the task fails, allowing you to handle errors gracefully.

def success_callback(result):
    print(f"Task completed successfully with result: {result}")
job.on_success(success_callback)

def failure_callback(exc):
    print(f"Task failed with exception: {exc}")
job.on_failure(failure_callback)

# 15. job.on_retry(callback) = This method allows you to specify a callback function that will be called when the task is retried. The callback function will receive the exception that caused the retry as an argument. This can be useful for logging retry attempts or performing specific actions when a retry occurs.
def retry_callback(exc):
    print(f"Task is being retried due to exception: {exc}")
job.on_retry(retry_callback)

# 16. job.on_timeout(callback) = This method allows you to specify a callback function that will be called if the task times out while waiting for a result. The callback function will receive the exception that caused the timeout as an argument. This can be useful for handling cases where a task takes too long to complete and you want to perform specific actions when a timeout occurs.
def timeout_callback(exc):
    print(f"Task timed out with exception: {exc}")
job.on_timeout(timeout_callback)

# 17. job.on_revoke(callback) = This method allows you to specify a callback function that will be called when the task is revoked. The callback function will receive the reason for revocation as an argument. This can be useful for logging revocation events or performing specific actions when a task is revoked.
def revoke_callback(reason):
    print(f"Task was revoked for reason: {reason}")
job.on_revoke(revoke_callback)

# 18. job.backend = This attribute gives you access to the result backend associated with the task, allowing you to interact with the backend directly if needed. You can use this to store additional information or retrieve results in a custom way.
print(job.backend)




