from sqlmodel import Session

from pyjira.app import logger
from pyjira.exceptions import RecordNotFoundError
from pyjira.services import TaskService


def add_task(data: dict, session: Session):
    task_service = TaskService(session=session)
    task = task_service.create_task(task_data=data)
    logger.info(f"Task added: {task.title}")


# List all tasks
def list_tasks(session: Session):
    task_service = TaskService(session=session)
    tasks = task_service.get_tasks()

    if not tasks:
        logger.warning("No tasks found.")
        return

    print("\nTasks:")
    for task in tasks:
        status = "✔" if task.completed else "✖"
        print(
            f"\nTitle: {task.title}\nDescription: {task.description}\nStatus: {status}"
        )
    print("\n")


# Mark a task as complete
def mark_complete(data: dict, session: Session):
    task_service = TaskService(session=session)
    try:
        task = task_service.update_task(task_data=data)
        logger.info(f"Task {task.title} marked as complete.")
    except RecordNotFoundError:
        pass


# Delete a task
def delete_task(task_title: str, session: Session):
    task_service = TaskService(session=session)
    try:
        task_service.delete_task(task_title=task_title)
        logger.info(f"Task {task_title} deleted.")
    except RecordNotFoundError:
        pass
