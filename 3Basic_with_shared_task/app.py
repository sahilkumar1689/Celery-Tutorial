from celery_config import celery_app 
from celery import chain,group,chord
from app.tasks import *


# job = sub.delay(7, 3)
# job = mul.delay(6, 3)


# 1. Chain = A chain is a powerful feature in Celery that allows you to link multiple tasks together in a sequence, where the output of one task is passed as the input to the next task automatically. This is useful for creating complex workflows and ensuring that tasks are executed in a specific order.Here we use the s() instead of delay() because delay() method directly submit the task to the worker and return the AsyncResult object while s() method creates a signature of the task that can be used to build a chain or group of tasks. When you call apply_async() on the chain, it will execute the tasks in the defined order, passing the results from one task to the next as needed.
# It is generally used when you have a series of tasks that need to be executed in a specific order, and the output of one task is required as input for the next task.

# workflow = chain(
#     add.s(2, 3),      # 5
#     multi.s(10),      # 5 * 10 = 50
#     square.s()        # 50² = 2500
# )


# result = workflow.apply_async()


# 2. Group = A group is a feature in Celery that allows you to execute multiple tasks in parallel. It is used when you have a collection of tasks that can be executed independently of each other, and you want to run them concurrently to improve performance. When you create a group of tasks, Celery will distribute the tasks across available worker processes, allowing them to run simultaneously. Once all tasks in the group are completed, you can collect their results together.
# It is generally used when you have a set of tasks that can be executed independently and you want to run them concurrently to improve performance.

# g = group(
#     add.s(2, 3),
#     multi.s(4, 5),
#     square.s(6)
# )

# result = g.apply_async()
# result.save()  # Save the group result to the backend for later retrieval

# # print(result.__dir__())
# print(result.id)
# # print(result.status)
# print(result.results)  # This will give you a list of AsyncResult objects for each task in the group.
# # Note = The group returns a GroupResult so it need to access by using the group_result = GroupResult.restore(group_id, app=celery_app) and then we can access the result by using group_result.results.


# 3. chord = It is a powerful feature in Celery that allows you to execute a group of tasks in parallel and then execute a callback task once all the tasks in the group have completed. A chord is essentially a combination of a group and a callback. The tasks in the group are executed concurrently, and once they are all finished, the results are collected and passed to the callback task for further processing. This is particularly useful when you have a set of tasks that can be executed independently, but you need to perform some final processing once all those tasks are done.

workflow = chord(
    [add.s(2,3), mul.s(4,5)],
    total.s()
)

result = workflow.apply_async()

print("Task started:", result.id)

# 4. Combined = We can also combine the chain,group and chord together to create more complex workflows. For example, we can have a chain of tasks that includes a group of tasks, and then a callback task that runs after the group is completed.

# ((2 + 3), (4 * 5), (6²)) → total → square

workflow = chain(
    chord(
        [
            add.s(2, 3),
            mul.s(4, 5),
            square.s(6)
        ],
        total.s()
    ),
    square.s()
)

result = workflow.apply_async()

# Note = When every you want to combine the result at end always use the chord and if you want to execute the task in sequence then use the chain and if you want to execute the task in parallel then use the group. You can also combine them together to create more complex workflows as per your requirement.
