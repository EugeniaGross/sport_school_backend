from pathlib import Path
import os

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

    @property
    def DB_URL(self):
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:"
            f"{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )

    @property
    def BASE_DIR(self):
        return str(Path(__file__).resolve().parent) + os.sep


settings = Settings()
