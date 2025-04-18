from sqlalchemy import Column, Integer, ForeignKey, DateTime
from .base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("events.id"))
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    movie = relationship("Event", back_populates="favorites")
