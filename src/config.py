from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # inherit from .env file
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    model_config = SettingsConfigDict(  # to read our .env file
        env_file='.env',
        extra='ignore'  # ignore any extra attributes
    )
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = False # set to True for Gmail | False for ABV
    MAIL_SSL_TLS: bool = True  # set to False for Gmail | True for ABV
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'  # ignore any extra attributes
    )

Config = Settings()
