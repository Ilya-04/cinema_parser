from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Pydantic-схемы для моделей

class EventBase(BaseModel):
    title: str
    type: str
    genre: str
    age_rating: str
    duration: int
    description: Optional[str] = None
    poster_url: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    class Config:
        orm_mode = True

class VenueBase(BaseModel):
    name: str
    address: str
    type: str

class VenueCreate(VenueBase):
    pass

class Venue(VenueBase):
    id: int

    class Config:
        orm_mode = True

class SessionBase(BaseModel):
    date: datetime
    time: str
    price: float

class SessionCreate(SessionBase):
    event_id: int
    venue_id: int

class Session(SessionBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class FavoriteBase(BaseModel):
    user_id: int
    movie_id: int
    added_at: datetime

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int

    class Config:
        orm_mode = True
