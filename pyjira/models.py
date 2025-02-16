from datetime import datetime

from caseconverter import snakecase
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)

    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.now)
    modify_date: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        protected_namespaces=(),
        from_attributes=True,
    )


class Task(BaseModel, table=True):
    title: str
    description: str
    completed: bool = False
