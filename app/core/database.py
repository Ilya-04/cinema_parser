from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Config

# Настройка подключения к базе данных
DATABASE_URL = Config.DB_URL

# Создаём engine
engine = create_engine(DATABASE_URL)

# Создаём базовый класс для моделей
Base = declarative_base()

# Создаём SessionLocal для работы с сессиями
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для создания всех таблиц в базе
def create_db():
    Base.metadata.create_all(bind=engine)
