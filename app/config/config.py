from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    MYSQL_URL: str
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_PORT: str
    MYSQL_DBNAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings():
    return Settings()
