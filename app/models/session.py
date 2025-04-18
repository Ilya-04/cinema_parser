from sqlalchemy import Column, Integer, ForeignKey, String
from .base import Base
from sqlalchemy.orm import relationship

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    venue_id = Column(Integer, ForeignKey("venues.id"))
    date = Column(String)
    time = Column(String)
    price = Column(String)

    event = relationship("Event", back_populates="sessions")
    venue = relationship("Venue", back_populates="sessions")
