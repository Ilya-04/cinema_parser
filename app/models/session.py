from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    venue_id = Column(Integer, ForeignKey("venues.id", ondelete="CASCADE"))
    date = Column(String)
    time = Column(String)
    price = Column(String)