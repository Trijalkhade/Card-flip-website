import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Member, Achievement, Event
from auth import router as auth_router

# Create tables automatically (dev). For prod use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ClubHoloHub")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (auth endpoints now live in auth.py)
app.include_router(auth_router)

# --- Pydantic schemas
class MemberOut(BaseModel):
    id: int
    name: str
    bio: str
    achievements: List[dict] = []

    class Config:
        from_attributes = True

class EventOut(BaseModel):
    id: int
    title: str
    description: str
    start_time: datetime
    seats: int

    class Config:
        orm_mode = True

# --- Public endpoints
@app.get("/members", response_model=List[MemberOut])
def list_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

@app.get("/events", response_model=List[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.start_time).all()

@app.get("/recommend_feed/{username}")
def recommend_feed(username: str, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.start_time).limit(limit).all()
    return {
        "username": username,
        "feed": [
            {
                "type": "event",
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "start_time": e.start_time,
            }
            for e in events
        ],
    }

# --- WebSocket echo chat (demo only)
@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"echo: {data}")
    except:
        await ws.close()
