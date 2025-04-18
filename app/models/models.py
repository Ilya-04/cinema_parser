from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    type = Column(String)
    genre = Column(String)
    age_rating = Column(String)
    duration = Column(Integer)
    description = Column(Text)
    poster_url = Column(String)
    
    sessions = relationship("Session", back_populates="event")

class Venue(Base):
    __tablename__ = 'venues'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    type = Column(String)
    
    sessions = relationship("Session", back_populates="venue")

class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    date = Column(DateTime)
    time = Column(String)
    price = Column(Float)
    
    event = relationship("Event", back_populates="sessions")
    venue = relationship("Venue", back_populates="sessions")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    favorites = relationship("Favorite", back_populates="user")

class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('events.id'))
    added_at = Column(DateTime)
    
    user = relationship("User", back_populates="favorites")
    movie = relationship("Event")
