from sqlmodel import create_engine, SQLModel, Session

from pyjira import app_settings

engine = create_engine(app_settings.database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        return session
