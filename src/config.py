from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_DB_NAME: str
    SECRET_KEY_JWT: str

    class Config:
        env_file = ".env"

settings = Settings()

