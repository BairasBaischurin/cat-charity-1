from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения QRKot"""

    app_title: str = 'Благотворительный фонд поддержки котов'
    app_description: str = 'Стандартное описание проекта QRKot'
    database_url: Optional[str] = 'sqlite+aiosqlite:///./fastapi.db'
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
