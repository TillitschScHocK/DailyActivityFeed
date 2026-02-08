# Daily Activity Feed Add-on

![Logo](logo.png)

## About

The Daily Activity Feed add-on provides a lightweight REST API for storing Home Assistant events with automatic cleanup and persistent storage.

### Features

✨ **REST API** - Simple HTTP endpoints for event management  
📋 **Persistent Storage** - JSON-based event database  
🧹 **Auto Cleanup** - Automatically removes events older than yesterday  
📸 **Image Support** - Store camera snapshots with events  
⚡ **FastAPI** - Modern, fast Python backend  

---

## Installation

1. Add this repository to your Home Assistant:
   ```
   https://github.com/TillitschScHocK/DAF---DailyActivityFeed
   ```

2. Install the **Daily Activity Feed** add-on

3. Configure options (see below)

4. Start the add-on

---

## Configuration

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `port` | 8099 | API port |
| `max_events_per_day` | 100 | Maximum events to store per day |

### Example Configuration

```json
{
  "port": 8099,
  "max_events_per_day": 100
}
```

---

## API Reference

### Health Check
```
GET /
```
Returns service status and version information.

### Add Event
```
POST /api/event
Content-Type: application/json

{
  "type": "doorbell",
  "title": "Doorbell",
  "text": "Someone rang the doorbell",
  "image": "/local/snapshot.jpg"
}
```

### Get Today's Events
```
GET /api/events/today
```

### Get Yesterday's Events
```
GET /api/events/yesterday
```

### Clear Events
```
DELETE /api/events/{day}
```
Where `day` is either `today` or `yesterday`.

---

## Logs

The add-on provides clean, minimal logging:

**Startup:**
```
=========================================
Daily Activity Feed API
=========================================
Port: 8099
Max events/day: 100
Data: /data/events.json
Loaded: 6 today, 0 yesterday
Ready to accept events
=========================================
```

**Event received:**
```
✓ Event: [doorbell] Doorbell
```

---

## Data Storage

Events are stored in `/data/events.json`:

```json
{
  "today": [
    {
      "type": "doorbell",
      "title": "Doorbell",
      "text": "Someone rang the doorbell",
      "timestamp": "14:32:15",
      "date": "2026-02-08",
      "image": "/local/snapshot.jpg"
    }
  ],
  "yesterday": []
}
```

Data is automatically cleaned:
- Events older than yesterday are removed
- Cleanup runs on startup and with each new event
- Date rollover happens automatically at midnight

---

## Troubleshooting

### Add-on won't start
- Check if port 8099 is already in use
- Review add-on logs for errors
- Ensure Home Assistant has sufficient resources

### API not responding
- Verify add-on is running
- Check network connectivity
- Test with: `http://addon-daily-activity-feed:8099/`

---

## Support

For issues and feature requests:
[GitHub Issues](https://github.com/TillitschScHocK/DAF---DailyActivityFeed/issues)

---

**Made with ❤️ for Home Assistant**
