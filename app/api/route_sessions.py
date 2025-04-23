# app/api/route_sessions.py
from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from app.schemas.session import SessionOut
from app.services.session_service import get_sessions_filtered
from sqlalchemy.orm import Session  # Импортируем Session
from app.db import get_db  # Импортируем get_db

router = APIRouter()

@router.get("/sessions")
def read_sessions(
    event_id: Optional[int] = None,
    venue_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_sessions_filtered(event_id=event_id, venue_id=venue_id, db=db)
