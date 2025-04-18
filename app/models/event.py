from sqlalchemy import Column, Integer, String, Text
from .base import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    type = Column(String)
    genre = Column(String)
    age_rating = Column(String)
    duration = Column(Integer)
    description = Column(Text)
    poster_url = Column(String)
