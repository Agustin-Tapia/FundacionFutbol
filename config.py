import os
from typing import List

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Futbol Compartir"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    db_user: str | None = None
    db_password: str | None = None
    db_host: str | None = None
    db_name: str
    secret_key: str = os.environ.get("SECRET_KEY", default="secret_key")
    access_token_expired_minutes: int = 30
    database_url: str | None = None

    @field_validator("database_url", mode="before")
    def assemble_db_connection(cls, v: str | None, values: FieldValidationInfo) -> str:
        if values.data.get("db_user") and values.data.get("db_host"):
            return PostgresDsn.build(
                scheme="postgresql",
                username=values.data.get("db_user"),
                password=values.data.get("db_password"),
                host=values.data.get("db_host"),
                path=f"{values.data.get('db_name') or ''}",
            ).unicode_string()
        return f"sqlite+aiosqlite:///{values.data.get('db_name')}.sqlite3"

    class Config:
        env_file = ".env"


settings = Settings()
