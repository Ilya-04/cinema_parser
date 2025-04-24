# app/api/route_venues.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.venue_service import get_venue_by_id
from app.schemas.venue import VenueOut
from app.db import get_db  # Получаем подключение к базе данных

router = APIRouter()

@router.get("/venues/{venue_id}", response_model=VenueOut)
def read_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = get_venue_by_id(db, venue_id)
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue
