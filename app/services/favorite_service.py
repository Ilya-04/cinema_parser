from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from app.models.user import User
from app.models.event import Event

def add_favorite(db: Session, user_id: int, event_id: int):
    favorite = Favorite(user_id=user_id, event_id=event_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

def remove_favorite(db: Session, user_id: int, event_id: int):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.event_id == event_id).first()
    if favorite:
        db.delete(favorite)
        db.commit()
    return favorite

def get_user_favorites(db: Session, user_id: int):
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()
