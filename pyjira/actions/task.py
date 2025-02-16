from sqlmodel import Session

from pyjira.app import logger
from pyjira import exceptions
from pyjira.services import TaskService


def add_task(data: dict, session: Session):
    task_service = TaskService(session=session)
    try:
        task = task_service.create_task(task_data=data)
        logger.info(f"Task added: {task.title}")
        return task
    except exceptions.RecordAlreadyExistError as e:
        logger.error(str(e))


# List all tasks
def list_tasks(session: Session):
    task_service = TaskService(session=session)
    tasks = task_service.get_tasks()

    if not tasks:
        logger.warning("No tasks found")
        return None

    print("\nTasks:")
    for task in tasks:
        status = "✔" if task.completed else "✖"
        print(
            f"\nTitle: {task.title}\nDescription: {task.description}\nStatus: {status}"
        )
    print("\n")
    return tasks


# Mark a task as complete
def mark_complete(data: dict, session: Session):
    task_service = TaskService(session=session)
    try:
        task = task_service.update_task(task_data=data)
        logger.info(f"Task {task.title} marked as complete.")
        return task
    except exceptions.RecordNotFoundError as e:
        logger.error(str(e))


# Delete a task
def delete_task(task_title: str, session: Session):
    task_service = TaskService(session=session)
    try:
        task_service.delete_task(task_title=task_title)
        logger.info(f"Task {task_title} deleted")
    except exceptions.RecordNotFoundError as e:
        logger.error(str(e))
