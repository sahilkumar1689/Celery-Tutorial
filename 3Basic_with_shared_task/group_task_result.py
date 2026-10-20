from celery_config import celery_app
from celery.result import GroupResult

def get_group_result(group_id):
    group_result = GroupResult.restore(group_id, app=celery_app)

    if not group_result:
        print("Group not found in backend")
        return

    # print("Group Status:", group_result.status)
    print("Completed:", group_result.completed_count())
    print("Total:", len(group_result.results))

    if group_result.ready():
        print("Final Results:", group_result.get())

if __name__ == "__main__":
    group_id = "43897993-a6c3-4a99-b6af-af065773a63a"  # Replace with your actual group ID
    get_group_result(group_id)