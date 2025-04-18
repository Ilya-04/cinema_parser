from pydantic import BaseModel

class EventBase(BaseModel):
    title: str
    type: str
    genre: str
    age_rating: str
    duration: int
    description: str
    poster_url: str

class EventCreate(EventBase):
    pass

class EventOut(EventBase):
    id: int

    class Config:
        orm_mode = True
