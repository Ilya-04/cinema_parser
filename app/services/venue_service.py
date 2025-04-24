# app/services/venue_service.py
from sqlalchemy.orm import Session
from app.models.venue import Venue
from app.schemas.venue import VenueOut

def get_venue_by_id(db: Session, venue_id: int) -> VenueOut:
    # Получаем площадку по ID
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if venue is None:
        return None  # Можно добавить обработку ошибки, если не найдено
    return VenueOut.from_orm(venue)
