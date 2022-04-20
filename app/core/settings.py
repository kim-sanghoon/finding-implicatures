from pydantic import BaseSettings


class Settings(BaseSettings):
    base_model: str

    class Config:
        env_file = ".env"

settings = Settings()
