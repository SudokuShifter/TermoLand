import os

from pydantic import BaseModel, Field

from src.common.const import DEFAULT_URL, DEFAULT_PATH


class ExternalApiConfig(BaseModel):
    URL: str = Field(default=DEFAULT_URL)
    PATH: str = Field(default=DEFAULT_PATH)


class AppConfig(BaseModel):
    external_api: ExternalApiConfig

    @classmethod
    def create(cls) -> "AppConfig":
        envs = os.environ

        external_api = ExternalApiConfig(**envs)

        return AppConfig(external_api=external_api)
