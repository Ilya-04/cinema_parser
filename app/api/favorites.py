from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.favorite import FavoriteOut
from app.services.favorite_service import add_favorite, remove_favorite, get_user_favorites
from app.core.security import get_current_user
from app.db import get_db
from app.models.user import User

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.post("/{event_id}", response_model=FavoriteOut)
def add_to_favorites(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Добавить в избранное
    return add_favorite(db, current_user.id, event_id)

@router.delete("/{event_id}", response_model=FavoriteOut)
def remove_from_favorites(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Удалить из избранного
    favorite = remove_favorite(db, current_user.id, event_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return favorite

@router.get("/", response_model=list[FavoriteOut])
def get_favorites(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Получить все избранные события
    return get_user_favorites(db, current_user.id)
