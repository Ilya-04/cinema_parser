# app/core/config.py
import os
from dotenv import load_dotenv

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
