import logging
from pathlib import Path
import os

from litestar.logging import LoggingConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{str(Path(__file__).resolve().parent.parent) + os.sep}.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    CLIENT_URL: str
    ALLOWED_HOSTS: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    ADMIN_TOKEN_EXPIRE_DAYS: int
    LITESTAR_WARN_IMPLICIT_SYNC_TO_THREAD: int
    PRODUCTION_URL: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_HOST: str
    EMAIL_PORT: str
    EMAIL_HOST_USER: str
    ADMIN_EMAIL: str

    @property
    def DB_URL(self):
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )

    @property
    def BASE_DIR(self):
        return str(Path(__file__).resolve().parent) + os.sep


settings = Settings()

logging_config = LoggingConfig(
    root={"level": "INFO", "handlers": ["queue_listener"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    log_exceptions="always",
)

logging_config.configure()("passlib").setLevel(logging.ERROR)
logger = logging_config.configure()()
