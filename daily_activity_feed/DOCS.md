# Daily Activity Feed Add-on Documentation

## Quick Start

1. Install the add-on from the add-on store
2. Configure port and event limits (optional)
3. Start the add-on
4. Add REST command to `configuration.yaml`
5. Create automations to send events

## Configuration Options

### `port` (integer)
**Default:** 8099  
**Range:** 8000-9000  
Port where the API will listen for requests.

### `max_events_per_day` (integer)
**Default:** 100  
**Range:** 1-1000  
Maximum number of events to store per day. Older events are automatically removed when limit is reached.

## REST API

### Add Event
```http
POST /api/event
Content-Type: application/json

{
  "type": "doorbell",
  "title": "Doorbell",
  "text": "Someone rang the doorbell",
  "image": "/local/snapshot.jpg"
}
```

**Response:**
```json
{
  "status": "success",
  "event": {
    "type": "doorbell",
    "title": "Doorbell",
    "text": "Someone rang the doorbell",
    "image": "/local/snapshot.jpg",
    "timestamp": "14:32:15",
    "date": "2026-02-08"
  }
}
```

### Get Events
```http
GET /api/events/today
GET /api/events/yesterday
```

### Clear Events
```http
DELETE /api/events/today
DELETE /api/events/yesterday
```

## Event Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Event category (e.g., doorbell, door, energy) |
| `title` | string | Yes | Short event title |
| `text` | string | Yes | Event description |
| `image` | string | No | Path to image (e.g., /local/snapshot.jpg) |

Server automatically adds:
- `timestamp` - Time in HH:MM:SS format
- `date` - Date in YYYY-MM-DD format

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

## Automatic Cleanup

The add-on automatically:
- Moves today's events to yesterday at midnight
- Deletes events older than yesterday
- Runs cleanup on startup and with each new event
- Enforces max_events_per_day limit

## Logs

Minimal, clean logging for easy monitoring:

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

✓ Event: [doorbell] Doorbell
✓ Event: [door] Front Door
```

## Troubleshooting

### Port Already in Use
Change the `port` option to a different value (e.g., 8100).

### Cannot Connect to Add-on
1. Verify add-on is running
2. Check logs for errors
3. Test with: `http://addon-daily-activity-feed:8099/`

### Events Not Saving
1. Check add-on logs
2. Verify JSON format in REST command
3. Ensure /data directory is writable

## Support

For help and issues:
https://github.com/TillitschScHocK/DAF---DailyActivityFeed/issues
