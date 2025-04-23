from pydantic import BaseModel
from datetime import datetime

class FavoriteBase(BaseModel):
    user_id: int
    movie_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteOut(FavoriteBase):
    id: int
    added_at: datetime

    model_config = {
    "from_attributes": True
}