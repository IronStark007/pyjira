import pytest

from sqlmodel import create_engine, SQLModel, Session

from pyjira.models import Task


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session  # Provide the session to the test

    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def add_task_data():
    title = "Watch tut"
    description = "I have to watch python tutorials at 8pm today."
    return {
        "payload": {"title": title, "description": description, "completed": False},
        "expected_response": Task(
            title=title, description=description, completed=False
        ),
        "error_response": "Task already exist with title: Watch tut",
    }


@pytest.fixture(scope="function")
def update_task_data(add_task_data):
    return {
        "add_payload": add_task_data.get("payload"),
        "update_payload": add_task_data.get("payload") | {"completed": True},
        "expected_response": Task(
            title=add_task_data.get("expected_response").title,
            description=add_task_data.get("expected_response").description,
            completed=True,
        ),
        "error_response": "Task not found with title: Watch tut",
    }


@pytest.fixture(scope="function")
def delete_task_data(update_task_data):
    return {
        **update_task_data,
        "expected_response": f"Task {update_task_data.get('add_payload').get('title')} deleted",
    }


@pytest.fixture(scope="function")
def list_task_data():
    return {
        "payload": [
            {
                "title": "task 1",
                "description": "description for task 1",
                "completed": False,
            },
            {
                "title": "task 2",
                "description": "description for task 2",
                "completed": True,
            },
        ],
        "expected_response": [
            Task(title="task 1", description="description for task 1", completed=False),
            Task(title="task 2", description="description for task 2", completed=True),
        ],
        "error_response": "No tasks found",
    }
