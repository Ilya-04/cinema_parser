from fastapi import Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.models.user import User  # Импортируем модель User
from app.utils.user_utils import get_user_by_email
from app.core import security  # Импортируем декодирование токена
from fastapi.security import OAuth2PasswordBearer
from app.db import get_db
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import status

# OAuth2 схема для получения токена из заголовков запроса
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Функция для извлечения текущего пользователя из токена
def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)  # Декодируем токен
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = get_user_by_email(db, email)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Хеширование пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Создание токена
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Определение функции decode_token
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Функция для получения данных из токена для Swagger
def get_current_user(token: str = Security(oauth2_scheme)) -> dict:
    # Извлекаем сам токен из объекта
    if isinstance(token, str):  # Проверяем, что это строка
        return decode_token(token)
    else:
        raise HTTPException(status_code=401, detail="Invalid token format")
