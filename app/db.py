from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаём подключение к базе данных
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

# Создаём сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для создания моделей
Base = declarative_base()

# Функция для получения сессии
def get_db():
    db = SessionLocal()  # Создаем новую сессию
    try:
        yield db  # Возвращаем сессию для использования в запросах
    finally:
        db.close()  # Закрываем сессию после использования