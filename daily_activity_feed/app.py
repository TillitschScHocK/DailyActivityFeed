#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Configuration
DATA_DIR = Path("/data")
DB_FILE = DATA_DIR / "events.json"
PORT = int(os.getenv("PORT", 8099))
MAX_EVENTS = int(os.getenv("MAX_EVENTS", 100))

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)
logger.info(f"Data directory: {DATA_DIR}")
logger.info(f"Database file: {DB_FILE}")

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
        logger.info("No existing events file found, creating new one")
        return {"today": [], "yesterday": []}
    
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.debug(f"Loaded {len(data.get('today', []))} events for today, {len(data.get('yesterday', []))} for yesterday")
            return data
    except Exception as e:
        logger.error(f"Error loading events: {e}")
        return {"today": [], "yesterday": []}


def save_events(data: dict) -> None:
    """Save events to JSON file"""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.debug("Events saved successfully")
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
            logger.info(f"Date changed, moving {len(data['today'])} events from today to yesterday")
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
            logger.info(f"Cleaned up {old_count - len(data['yesterday'])} old events")
    
    save_events(data)


@app.on_event("startup")
async def startup_event():
    """Run cleanup on startup"""
    logger.info("===========================================")
    logger.info("Daily Activity Feed API starting up")
    logger.info("===========================================")
    logger.info(f"Port: {PORT}")
    logger.info(f"Max events per day: {MAX_EVENTS}")
    logger.info("Running initial cleanup...")
    cleanup_old_events()
    logger.info("Startup complete - Ready to accept events")
    logger.info("===========================================")


@app.get("/")
async def root():
    """Health check endpoint"""
    logger.info("Health check requested")
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
        
        # Check max events limit
        if len(data["today"]) >= MAX_EVENTS:
            logger.warning(f"Max events limit reached ({MAX_EVENTS}), removing oldest")
            data["today"] = data["today"][:MAX_EVENTS-1]
        
        data["today"].insert(0, stored_event.dict())  # Insert at beginning for newest first
        
        # Save
        save_events(data)
        
        logger.info(f"Event received: [{event.type}] {event.title}")
        
        return {"status": "success", "event": stored_event.dict()}
    
    except Exception as e:
        logger.error(f"Error adding event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events/today")
async def get_today_events():
    """Get all events from today"""
    logger.info("Fetching today's events")
    cleanup_old_events()
    data = load_events()
    count = len(data.get("today", []))
    logger.info(f"Returning {count} events for today")
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "count": count,
        "events": data.get("today", [])
    }


@app.get("/api/events/yesterday")
async def get_yesterday_events():
    """Get all events from yesterday"""
    logger.info("Fetching yesterday's events")
    cleanup_old_events()
    data = load_events()
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    count = len(data.get("yesterday", []))
    logger.info(f"Returning {count} events for yesterday")
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
    
    logger.info(f"Cleared {count} events for {day}")
    
    return {"status": "success", "cleared": day, "count": count}


if __name__ == "__main__":
    logger.info("Starting uvicorn server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
        access_log=True
    )
