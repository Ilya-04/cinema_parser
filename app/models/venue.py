from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
