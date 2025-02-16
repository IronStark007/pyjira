from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: str


class PyJiraException(Exception):
    def __init__(self, message: str | None = None):
        self.message = message
        self.error_response = ErrorModel(detail=message)
        super().__init__(self.message)


class RecordNotFoundError(PyJiraException): ...


class RecordAlreadyExistError(PyJiraException): ...
