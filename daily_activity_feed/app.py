#!/usr/bin/env python3
import json
import os
import sys
import warnings
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import logging

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Configure logging - reduce verbosity
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Silence uvicorn access logs
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.setLevel(logging.WARNING)

# Configuration
DATA_DIR = Path("/data")
DB_FILE = DATA_DIR / "events.json"
PORT = int(os.getenv("PORT", 8099))
MAX_EVENTS = int(os.getenv("MAX_EVENTS", 100))

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
        logger.error(f"Error loading events: {e}")
        return {"today": [], "yesterday": []}


def save_events(data: dict) -> None:
    """Save events to JSON file"""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving events: {e}")


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
            logger.info(f"Date changed - moved {len(data['today'])} events to yesterday")
            data["yesterday"] = data["today"]
            data["today"] = []
    
    # Filter yesterday's events
    if data.get("yesterday"):
        old_count = len(data["yesterday"])
        data["yesterday"] = [
            event for event in data["yesterday"]
            if event.get("date") == yesterday_str
        ]
        if old_count != len(data["yesterday"]):
            removed = old_count - len(data["yesterday"])
            logger.info(f"Cleaned up {removed} old event(s)")
    
    save_events(data)


@app.on_event("startup")
async def startup_event():
    """Run cleanup on startup"""
    logger.info("=========================================")
    logger.info("Daily Activity Feed API")
    logger.info("=========================================")
    logger.info(f"Port: {PORT}")
    logger.info(f"Max events/day: {MAX_EVENTS}")
    logger.info(f"Data: {DB_FILE}")
    cleanup_old_events()
    data = load_events()
    logger.info(f"Loaded: {len(data.get('today', []))} today, {len(data.get('yesterday', []))} yesterday")
    logger.info("Ready to accept events")
    logger.info("=========================================")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Daily Activity Feed API",
        "version": "1.0.0",
        "port": PORT
    }


@app.post("/api/event")
async def add_event(event: Event):
    """Add a new event to today's feed"""
    try:
        cleanup_old_events()
        data = load_events()
        
        now = datetime.now()
        stored_event = StoredEvent(
            **event.model_dump(),
            timestamp=now.strftime("%H:%M:%S"),
            date=now.strftime("%Y-%m-%d")
        )
        
        if "today" not in data:
            data["today"] = []
        
        # Check max events limit
        if len(data["today"]) >= MAX_EVENTS:
            data["today"] = data["today"][:MAX_EVENTS-1]
        
        data["today"].insert(0, stored_event.model_dump())
        save_events(data)
        
        # Only log event creation, not regular fetches
        logger.info(f"\u2713 Event: [{event.type}] {event.title}")
        
        return {"status": "success", "event": stored_event.model_dump()}
    
    except Exception as e:
        logger.error(f"Error adding event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events/today")
async def get_today_events():
    """Get all events from today"""
    cleanup_old_events()
    data = load_events()
    count = len(data.get("today", []))
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "count": count,
        "events": data.get("today", [])
    }


@app.get("/api/events/yesterday")
async def get_yesterday_events():
    """Get all events from yesterday"""
    cleanup_old_events()
    data = load_events()
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    count = len(data.get("yesterday", []))
    return {
        "date": yesterday,
        "count": count,
        "events": data.get("yesterday", [])
    }


@app.delete("/api/events/{day}")
async def clear_events(day: str):
    """Clear events for a specific day (today or yesterday)"""
    if day not in ["today", "yesterday"]:
        raise HTTPException(status_code=400, detail="Day must be 'today' or 'yesterday'")
    
    data = load_events()
    count = len(data.get(day, []))
    data[day] = []
    save_events(data)
    
    logger.info(f"Cleared {count} event(s) for {day}")
    
    return {"status": "success", "cleared": day, "count": count}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="warning",  # Only show warnings and errors
        access_log=False  # Disable access logging
    )
