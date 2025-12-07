from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    NEON_DATABASE_URL: str
    QDRANT_URL: str
    QDRANT_API_KEY: str
    PORT: int = 8000

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()
