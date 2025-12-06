from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    QDRANT_API_KEY: str
    QDRANT_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
