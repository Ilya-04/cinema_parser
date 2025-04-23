# app/services/event_service.py
from fastapi import Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Event, Session as DBSession
from app.db import get_db
from datetime import datetime, timedelta
from sqlalchemy import cast, Date


def get_filtered_events(
    type: Optional[str],
    date: Optional[str],
    genre: Optional[str],
    age_rating: Optional[str],
    time: Optional[str],
    price: Optional[str],
    db: Session = Depends(get_db)
) -> List[Event]:
    query = db.query(Event)

    if type:
        query = query.filter(Event.type_event == type)

    if genre:
        query = query.filter(Event.genre == genre)

    if age_rating:
        query = query.filter(Event.age_rating == age_rating)

    if date == "today":
        today = datetime.today().date()
        query = query.join(Event.sessions).filter(cast(DBSession.date, Date) == today)
    elif date == "tomorrow":
        tomorrow = datetime.today().date() + timedelta(days=1)
        query = query.join(Event.sessions).filter(cast(DBSession.date, Date) == tomorrow)
    elif date:
        try:
            specific_date = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.join(Event.sessions).filter(cast(DBSession.date, Date) == specific_date)
        except ValueError:
            pass  # Неправильный формат даты


    # Сортировка по времени суток
    if time:
        if time == "утром":
            query = query.join(Event.sessions).filter(DBSession.time < "12:00")
        elif time == "днём":
            query = query.join(Event.sessions).filter(DBSession.time >= "12:00", DBSession.time < "18:00")
        elif time == "вечером":
            query = query.join(Event.sessions).filter(DBSession.time >= "18:00")

    # Сортировка по цене
    if price == "asc":
        query = query.join(Event.sessions).order_by(DBSession.price.asc())
    elif price == "desc":
        query = query.join(Event.sessions).order_by(DBSession.price.desc())

    return query.all()


def get_event_by_id(event_id: int, db: Session = Depends(get_db)) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()

