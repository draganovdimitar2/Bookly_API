from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    model_config = SettingsConfigDict(  # to read our .env file
        env_file = '.env',
        extra='ignore'  # ignore any extra attributes
    )

Config = Settings()
