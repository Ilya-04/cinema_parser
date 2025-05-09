from sqlalchemy import Column, Integer, String
from .base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # ЭТО ХЭШ, хотя называется "password"
    
    favorites = relationship("Favorite", back_populates="user")
