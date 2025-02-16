from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///pyjira.db"
    debug_mode: bool = True
    log_level: str = "info"
    logger_name: str = "pyjira"
    log_format: str = "[%(asctime)s] [%(process)s] [%(name)s:%(module)s:%(funcName)s] [%(levelname)s]  %(message)s"
    disable_existing_loggers: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


app_settings = get_settings()
