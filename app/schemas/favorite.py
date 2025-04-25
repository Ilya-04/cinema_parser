from pydantic import BaseModel

class FavoriteOut(BaseModel):
    id: int
    event_id: int

    model_config = {
    "from_attributes": True
}