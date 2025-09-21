# config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # 业务相关
    OPENAI_API_KEY: str | None = Field(default=None)
    DASH_SCOPE_KEY: str | None = Field(default=None)

    # 路径/IO
    WORK_DIR: str = Field(default="data")
    TMP_DIR: str = Field(default="data/tmp")
    OUTPUT_DIR: str = Field(default="data/output")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
