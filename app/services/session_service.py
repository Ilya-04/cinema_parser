from app.models import Session as DBSession
from app.db import get_db
from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List


def get_sessions_filtered(
    event_id: Optional[int],
    venue_id: Optional[int],
    db: Session
) -> List[DBSession]:
    query = db.query(DBSession)
    if event_id:
        query = query.filter(DBSession.event_id == event_id)
    if venue_id:
        query = query.filter(DBSession.venue_id == venue_id)
    return query.all()
