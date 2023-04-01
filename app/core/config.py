from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    parse_obj_as,
    validator,
)
from typing import Any, Optional, Union
import secrets

# from dotenv import dotenv_values, find_dotenv


# class Config:
#     config = dotenv_values(find_dotenv())
#     config["SECRET_KEY"] = secrets.token_urlsafe()


# config = Config().config


class Settings(BaseSettings):
    API_STR: str = "/jfarms"
    SECRET_KEY: str
    AUTHJWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2  # 60 * 24 * 8  # 8 days
    SERVER_NAME: str = "localhost"
    SERVER_HOST: AnyHttpUrl = parse_obj_as(AnyHttpUrl, "http://127.0.0.1:8000")
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ["http://localhost:3000"]  # type: ignore

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "JFarms"

    # SENTRY_DSN: Optional[HttpUrl]

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    DATABASE_PORT: int
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///healthy_cup.db"
    # SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = "sqlite:///healthy_cup.db"

    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_HOST"),  # type: ignore
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_FULL_NAME: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()  # type: ignore
