
import redis


# 1. Celery = Firstly we need to know what problem celry solves.In modern web applications, some tasks are too time-consuming to run in real time. Processes like sending email notifications, processing large datasets, or handling complex computations.
# This is where Celery comes into play. Celery is a distributed task queue system in Python, designed to handle tasks asynchronously in the background without blocking the main application. It allows you to offload time-consuming tasks to worker processes, which can run concurrently and independently of the main application.

# Key components of Celery = Celery consists of three main components i.e. task,worker and broker.These three elements work together to create a robust task-handling environment that processes and distributes tasks efficiently.
# 1. Task = In Celery, a task is nothing but a simple Python function that has been decorated to run asynchronously. 
# 2. Worker = A worker is a process that runs in the background and is responsible for executing tasks. Workers listen to the task queue and pick up tasks to execute them. You can have multiple workers running concurrently, allowing for parallel processing of tasks.
# 3. Broker = A broker is a message queue that acts as an intermediary between the main application and the workers. It is responsible for receiving tasks from the main application and distributing them to the workers as they become available. Common brokers used with Celery include RabbitMQ and Redis.

# If we summarize the flow, When a task is called, Celery sends it to the broker. The broker holds the task until a worker process retrieves it and starts processing. Once the worker completes the task, it can return the result to the main application or store it in a result backend for later retrieval.


# Commands for celery worker:
# 1. celery -A folder_name.config_file_name worker --loglevel-info = This command is used in linux or production systems.By default run --pool=prefork
# 2. celery -A folder_name.config_file_name worker --pool=solor or thread --loglevel=info = Used in the window systems.
# 3. uv run celery -A folder_name.config_file_name worker -- pool=solo or thread --loglevel=info = Used on window if you use uv.

# Note = 1. Celery internally cannot handle the tasks itself.It delegate the task to pool of execution units.These execution unit can be processes,threads,event loop.Now the --pool commands control that think only which execution unit to use.
# 2. the --pool= solo means one task at a time, --pool=thread means multiple tasks run parallel at a time.
# 3. If you getting erro while running the celry worker then run it as a python module like "uv run python -m rest_of_the_command".


# More important configuration realted to workers and the autoscaling:

# 1. uv run celery -A folder_name.config_file_name worker --loglevel=info -c 4 = This command is used to specify the number of worker processes to run concurrently. In this example, it will run 4 worker processes.It only works on the linux or production system where the by default pool is prefork.In pool=solo case by deafult -c = 1.

# 2. uv run celery -A folder_name.config_file_name worker --pool=thread --loglevel=info -c 4 = It will work on widows as well as linux system and it will run 4 worker threads concurrently.Usefull for I/O bound tasks.

# 3. uv run celery -A folder_name.config_file_name worker --loglevel=info --autoscale=10,3 = Celery will automatically adjust the number of worker processes based on the workload, scaling up when there are more tasks to process and scaling down when there are fewer tasks.But only works on linux or production system where the by default pool is prefork.We can also customize with pool=thread.

# 4. celery -A project worker -l info -c 4 --prefetch-multiplier=1 = It is used to handle the number of tasks a worker can grabs.

# 5. uv run celery -A project worker -n worker1@<%h> = This command is used to give a specific name to a worker.This command is used to run worker on multiple machine or horizonal scaling.where %h = replaced with the hostname of that machine.

# 6. celery -A your_project_name inspect active = This command is used to check the active tasks that are currently being processed by the workers. It provides information about the tasks that are currently running, including their IDs, names, and the worker that is processing them.

# 7. celery -A celery_config.celery_app worker -Q cpu_queue -l info = This command is used to specify a particular queue for the worker to listen to. In this example, the worker will only process tasks that are sent to the "cpu_queue". This is useful for organizing tasks into different queues based on their type or priority, allowing for more efficient task management and processing.

# 8. uv run python -m celery -A celery_config.celery_app flower --port=5555 = Firslty install the flower usign uv or pip.This command is used to start the Flower monitoring tool for Celery. Flower provides a web-based interface to monitor and manage Celery workers and tasks. By running this command, you can access the Flower dashboard at http://localhost:5555 to see real-time information about your Celery workers, tasks, and their statuses. It allows you to track task progress, view task results, and manage worker processes effectively.

# Note = 1. In real production environment, we keep think simple so we only run this command "celery -A project worker -l info -c 4 --prefetch-multiplier=1" and it will work fine for most of the use cases.
# 2. They achieve scaling with container or pods via horizontal scaling.


def main():
    print("Hello from celery-tutorial!")
    r = redis.Redis(host="localhost", port=6379)
    print(r.ping())   # True


if __name__ == "__main__":
    main()
