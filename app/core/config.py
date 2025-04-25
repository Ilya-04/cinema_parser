# app/core/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Загружаем .env файл
load_dotenv()

class Config:
    DB_URL = os.getenv("DB_URL", "postgresql://postgres:000@localhost/cinema_parser")  # Строка подключения
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Пример секрета
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")  # Алгоритм для JWT
    
    # Добавляем строку подключения для SQLAlchemy
    SQLALCHEMY_DATABASE_URL = DB_URL

# Экземпляр конфигурации
settings = Config()


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
