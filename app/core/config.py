import os

class Settings:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:000@localhost/cinema_parser")

settings = Settings()
