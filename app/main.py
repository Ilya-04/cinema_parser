# app/main.py
from fastapi import FastAPI
from app.api import route_events, route_sessions

app = FastAPI()

app.include_router(route_events.router)
app.include_router(route_sessions.router)
