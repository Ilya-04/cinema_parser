from pydantic import BaseModel

class VenueBase(BaseModel):
    name: str
    address: str
    type: str

class VenueCreate(VenueBase):
    pass

class VenueOut(VenueBase):
    id: int

    class Config:
        orm_mode = True
