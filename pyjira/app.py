import logging
from logging.config import dictConfig

from pyjira import app_settings
from pyjira.actions import task
from pyjira.databases import init_db, get_session
from pyjira.logger_conf import log_config

dictConfig(log_config)
logger = logging.getLogger(app_settings.logger_name)


if __name__ == "__main__":
    init_db()
    while True:
        print("\nPyJira - Task Manager")
        print("1. Add Task\n2. List Task\n3. Mark Complete\n4. Delete Task\n5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            task.add_task(
                data={"title": title, "description": description}, session=get_session()
            )
        elif choice == "2":
            task.list_tasks(session=get_session())
        elif choice == "3":
            task_title = input("Enter task title to mark complete: ")
            completed = input("Mark complete? (y/n): ")
            is_completed = True if completed == "y" else False
            task.mark_complete(
                data={"title": task_title, "completed": is_completed},
                session=get_session(),
            )
        elif choice == "4":
            task_title = input("Enter task title to delete: ")
            task.delete_task(task_title=task_title, session=get_session())
        elif choice == "5":
            logger.info("Exiting...\nThank you for using PyJira")
            break
        else:
            logger.warning("Invalid choice. Please try again.")
