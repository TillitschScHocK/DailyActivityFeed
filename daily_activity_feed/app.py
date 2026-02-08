#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Configuration
DATA_DIR = Path("/data")
DB_FILE = DATA_DIR / "events.json"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Daily Activity Feed API")


class Event(BaseModel):
    type: str
    title: str
    text: str
    image: Optional[str] = None


class StoredEvent(Event):
    timestamp: str
    date: str


def load_events() -> dict:
    """Load events from JSON file"""
    if not DB_FILE.exists():
        return {"today": [], "yesterday": []}
    
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading events: {e}")
        return {"today": [], "yesterday": []}


def save_events(data: dict) -> None:
    """Save events to JSON file"""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving events: {e}")


def cleanup_old_events() -> None:
    """Remove events older than yesterday"""
    data = load_events()
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    today_str = today.strftime("%Y-%m-%d")
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    
    # Move today to yesterday if date changed
    if data.get("today") and len(data["today"]) > 0:
        first_event_date = data["today"][0].get("date", today_str)
        if first_event_date != today_str:
            data["yesterday"] = data["today"]
            data["today"] = []
    
    # Filter yesterday's events
    if data.get("yesterday"):
        data["yesterday"] = [
            event for event in data["yesterday"]
            if event.get("date") == yesterday_str
        ]
    
    save_events(data)


@app.on_event("startup")
async def startup_event():
    """Run cleanup on startup"""
    cleanup_old_events()
    print("Daily Activity Feed API started")


@app.get("/")
async def root():
    return {"status": "ok", "service": "Daily Activity Feed API"}


@app.post("/api/event")
async def add_event(event: Event):
    """Add a new event to today's feed"""
    try:
        # Cleanup old events first
        cleanup_old_events()
        
        # Load current data
        data = load_events()
        
        # Create stored event with timestamp
        now = datetime.now()
        stored_event = StoredEvent(
            **event.dict(),
            timestamp=now.strftime("%H:%M:%S"),
            date=now.strftime("%Y-%m-%d")
        )
        
        # Add to today's events
        if "today" not in data:
            data["today"] = []
        data["today"].insert(0, stored_event.dict())  # Insert at beginning for newest first
        
        # Save
        save_events(data)
        
        return {"status": "success", "event": stored_event.dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events/today")
async def get_today_events():
    """Get all events from today"""
    cleanup_old_events()
    data = load_events()
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "count": len(data.get("today", [])),
        "events": data.get("today", [])
    }


@app.get("/api/events/yesterday")
async def get_yesterday_events():
    """Get all events from yesterday"""
    cleanup_old_events()
    data = load_events()
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    return {
        "date": yesterday,
        "count": len(data.get("yesterday", [])),
        "events": data.get("yesterday", [])
    }


@app.delete("/api/events/{day}")
async def clear_events(day: str):
    """Clear events for a specific day (today or yesterday)"""
    if day not in ["today", "yesterday"]:
        raise HTTPException(status_code=400, detail="Day must be 'today' or 'yesterday'")
    
    data = load_events()
    data[day] = []
    save_events(data)
    
    return {"status": "success", "cleared": day}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8099))
    uvicorn.run(app, host="0.0.0.0", port=port)