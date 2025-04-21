from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type_event = Column(String, nullable=False)
    genre = Column(String)
    age_rating = Column(String)
    duration = Column(String)
    description = Column(Text)
    poster_url = Column(String)
    url = Column(String)
    favorites = relationship("Favorite", back_populates="movie")
