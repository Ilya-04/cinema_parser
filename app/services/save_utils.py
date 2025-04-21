from app.db import get_db
from app.models import Event, Venue, Session
from sqlalchemy.orm import Session as SQLAlchemySession

def save_event_and_session(db: SQLAlchemySession, title: str, genre: str, age_rating: str, duration: str,
                            description: str, url: str, type_event: str, poster_url: str, date: str,
                            venue_address: str, time_: str, price: str):
    # Проверяем, существует ли уже такое событие в базе
    event = db.query(Event).filter(Event.title == title).first()
    if not event:
        # Если события нет, создаём новое
        event = Event(
            title=title,
            genre=genre,
            age_rating=age_rating,
            duration=duration,
            description=description,
            url=url,
            type_event=type_event,
            poster_url=poster_url
        )
        db.add(event)
        db.commit()
        db.refresh(event)

    # Проверяем, существует ли уже такое место проведения
    venue = db.query(Venue).filter(Venue.address == venue_address).first()
    if not venue:
        # Если места нет, создаём новое
        venue = Venue(address=venue_address)
        db.add(venue)
        db.commit()
        db.refresh(venue)

    # Создаём сеанс
    session = Session(
        event_id=event.id,
        venue_id=venue.id,
        date=date,
        time=time_,
        price=price
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return event, venue, session
