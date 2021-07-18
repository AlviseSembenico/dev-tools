from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):

    MONGO_DB_USER: str
    MONGO_DB_PASSWORD: str
    MONGO_DB_NAME: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
