from celery_tasks import add

job = add.delay(3, 3)

print(job.id)
print(job.status)
print(job.result)
