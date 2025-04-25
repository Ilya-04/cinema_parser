# app/main.py
from fastapi import FastAPI
from app.api import route_events, route_sessions, favorites
from fastapi.middleware.cors import CORSMiddleware
from app.api.route_venues import router as venue_router
from app.api import auth, protected

app = FastAPI()

app.include_router(route_events.router)
app.include_router(route_sessions.router)
app.include_router(venue_router)
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(favorites.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или ["http://localhost:5173"] — адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# .\venv\Scripts\Activate
# uvicorn app.main:app --reload