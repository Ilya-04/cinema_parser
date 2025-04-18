from pydantic import BaseModel

class SessionBase(BaseModel):
    event_id: int
    venue_id: int
    date: str
    time: str
    price: str

class SessionCreate(SessionBase):
    pass

class SessionOut(SessionBase):
    id: int

    class Config:
        orm_mode = True
