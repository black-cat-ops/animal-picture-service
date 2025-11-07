import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://user:password@db:5432/animals"
    )
    app_name: str = "Animal Picture Service"
    app_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"

settings = Settings()
