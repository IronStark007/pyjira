from typing import Sequence

from sqlmodel import Session, select

from pyjira.app import logger
from pyjira import exceptions
from pyjira.models import Task


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task_data: dict) -> Task:
        logger.info("Creating task.....")
        if self.get_task(task_title=task_data["title"]):
            raise exceptions.RecordAlreadyExistError(
                message=f"Task already exist with title: {task_data['title']}"
            )
        task = Task(
            title=task_data["title"],
            description=task_data["description"],
            completed=task_data.get("completed", False),
        )
        self.session.add(task)
        self.session.commit()
        return task

    def get_tasks(self) -> Sequence[Task]:
        statement = select(Task).order_by(Task.id)
        return self.session.exec(statement).all()

    def get_task(self, task_title: str) -> Task:
        statement = select(Task).where(Task.title == task_title)
        return self.session.exec(statement).one_or_none()

    def update_task(self, task_data: dict) -> Task:
        if not (task := self.get_task(task_title=task_data["title"])):
            raise exceptions.RecordNotFoundError(
                message=f"Task not found with title: {task_data['title']}"
            )
        if task_data.get("description"):
            task.description = task_data["description"]
        if task_data.get("completed"):
            task.completed = task_data["completed"]
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_title: str) -> None:
        if not (task := self.get_task(task_title=task_title)):
            raise exceptions.RecordNotFoundError(
                message=f"Task not found with title: {task_title}"
            )
        self.session.delete(task)
        self.session.commit()
