from app.core.database import SessionLocal, Base
from app.models import events, users, venues, sessions, favorites

# Создаём сессию и создаём таблицы
def create_tables():
    # Создаём все таблицы, которые были описаны в моделях
    Base.metadata.create_all(bind=SessionLocal())

if __name__ == "__main__":
    create_tables()
    print("Таблицы успешно созданы.")
