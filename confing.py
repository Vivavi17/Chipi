from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseModel):
    API_KEY: str
    AI_URL: str


class LLMSettings(BaseModel):
    PROMPT: str
    AI_MODEL: str


class ServerSettings(BaseModel):
    ADMIN_ID: int
    BOT_TOKEN: str


class DBSettings(BaseModel):
    DB_PATH: str


class Settings(BaseSettings):
    LLM: LLMSettings
    OPENAI: OpenAISettings
    SERVER: ServerSettings
    DB: DBSettings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        nested_model_default_partial_update=False,
    )
