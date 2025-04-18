from sqlalchemy import Column, Integer, String
from .base import Base

class Venue(Base):
    __tablename__ = "venues"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    type = Column(String)
