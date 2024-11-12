from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

class Settings(BaseSettings):  # inherit from .env file
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str
    REDIS_PORT: int
    model_config = SettingsConfigDict(  # to read our .env file
        env_file='.env',
        extra='ignore'  # ignore any extra attributes
    )


Config = Settings()
