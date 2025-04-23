# app/api/route_events.py
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.schemas.event import EventOut
from app.services.event_service import get_filtered_events
from fastapi import HTTPException
from app.services.event_service import get_event_by_id
from sqlalchemy.orm import Session  # Импортируем Session
from app.db import get_db  # Импортируем get_db


router = APIRouter()

@router.get("/events", response_model=List[EventOut])
def read_events(
    type: Optional[str] = Query(None, description="Тип события: кино, спектакль, концерт"),
    date: Optional[str] = Query(None, description="Дата: today, tomorrow или YYYY-MM-DD"),
    genre: Optional[str] = Query(None),
    age_rating: Optional[str] = Query(None),
    time: Optional[str] = Query(None, description="Время суток: утром, днём, вечером"),
    price: Optional[str] = Query(None, description="Сортировка цены: asc или desc"),
    db: Session = Depends(get_db)  # ✅ ЭТО НУЖНО ДЛЯ ПОЛУЧЕНИЯ СЕССИИ
):
    return get_filtered_events(
        db=db,  # ПЕРЕДАЁМ СЕССИЮ В СЕРВИС
        type=type, date=date, genre=genre,
        age_rating=age_rating, time=time, price=price
    )

@router.get("/events/{event_id}", response_model=EventOut)
def read_event_by_id(event_id: int, db: Session = Depends(get_db)):  # Получаем db через Depends
    event = get_event_by_id(event_id, db=db)  # Передаём db в get_event_by_id
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    return event

