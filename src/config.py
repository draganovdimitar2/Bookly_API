from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # inherit from .env file
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    SENDGRID_API_KEY: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    DOMAIN: str
    model_config = SettingsConfigDict(  # to read our .env file
        env_file='.env',
        extra='ignore'  # ignore any extra attributes
    )


Config = Settings()
