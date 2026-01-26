import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

current_dir = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(current_dir, "..", "..", ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path, 
        env_file_encoding="utf-8",
        extra="ignore" # This helps ignore extra env variables
    )
    
    # model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")

    DATABASE_URL: Optional[str] = None