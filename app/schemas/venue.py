from pydantic import BaseModel

class VenueBase(BaseModel):
    address: str

class VenueCreate(VenueBase):
    pass

class VenueOut(VenueBase):
    id: int

    model_config = {
    "from_attributes": True
}
