
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STORAGE_DIR: str = "data/uploads"
    MAX_FILE_MB: int = 5
    ALLOWED_EXTS: List[str] = [".png", ".jpg", ".jpeg"]
    ALLOWED_CONTENT_TYPES: List[str] = ["image/png", "image/jpeg"]
    API_KEY: str | None = None
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
