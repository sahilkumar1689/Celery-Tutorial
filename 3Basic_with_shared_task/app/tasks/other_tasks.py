from celery import shared_task

@shared_task
def add(x, y):
    return x + y

@shared_task
def multi(x, y):
    return x * y

@shared_task
def square(x):
    return x * x

@shared_task
def total(numbers):
    return sum(numbers)