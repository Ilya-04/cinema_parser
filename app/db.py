from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .core.config import settings

# Создаём подключение к базе данных
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

# Создаём сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для создания моделей
Base = declarative_base()
