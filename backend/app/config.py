from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "CallBot Detective API"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    
    DATABASE_URL: str = "sqlite:///./callbot.db"
    
    GEMINI_API_KEY: str = ""
    CALLE_API_KEY: str = ""
    CALLE_MODE: str = "mock"  # Options: "mock", "real"
    CALLE_API_URL: str = "https://api.heycall-e.com/v1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
