from pydantic import BaseModel

class EventBase(BaseModel):
    title: str
    type_event: str
    genre: str
    age_rating: str
    duration: str
    description: str
    poster_url: str
    url: str
    

class EventCreate(EventBase):
    pass

class EventOut(EventBase):
    id: int

    model_config = {
    "from_attributes": True
}
