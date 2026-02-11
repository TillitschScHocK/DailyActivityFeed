# Daily Activity Feed Add-on Documentation

## 📋 Table of Contents

- [Configuration Options](#configuration-options)
- [REST API Reference](#rest-api-reference)
- [Event Fields](#event-fields)
- [Data Storage](#data-storage)
- [Automatic Cleanup](#automatic-cleanup)
- [Logs](#logs)
- [Troubleshooting](#troubleshooting)

---

## ⚙️ Configuration Options

### `port`
- **Type:** Integer
- **Default:** `8099`
- **Range:** `8000-9000`
- **Description:** Port where the API listens for requests. Change if 8099 is already in use.

### `max_events_per_day`
- **Type:** Integer
- **Default:** `100`
- **Range:** `1-1000`
- **Description:** Maximum number of events stored per day. Older events are removed when the limit is reached.

**Example Configuration:**
```json
{
  "port": 8099,
  "max_events_per_day": 100
}
```

---

## 📡 REST API Reference

### Add Event

**Endpoint:** `POST /api/event`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
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

### Get Today's Events

**Endpoint:** `GET /api/events/today`

**Response:**
```json
[
  {
    "type": "doorbell",
    "title": "Doorbell",
    "text": "Someone rang the doorbell",
    "timestamp": "14:32:15",
    "date": "2026-02-08",
    "image": "/local/snapshot.jpg"
  }
]
```

### Get Yesterday's Events

**Endpoint:** `GET /api/events/yesterday`

Returns an array of yesterday's events in the same format.

### Clear Events

**Endpoint:** `DELETE /api/events/{day}`

**Parameters:**
- `day`: Either `today` or `yesterday`

**Response:**
```json
{
  "status": "success",
  "message": "Events cleared"
}
```

### Health Check

**Endpoint:** `GET /`

**Response:**
```json
{
  "status": "running",
  "version": "1.0.0",
  "events_today": 6,
  "events_yesterday": 0
}
```

---

## 📝 Event Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ Yes | Event category (e.g., `doorbell`, `door`, `energy`, `security`) |
| `title` | string | ✅ Yes | Short event title |
| `text` | string | ✅ Yes | Detailed event description |
| `image` | string | ⬜ No | Image path (e.g., `/local/snapshot.jpg`) |
| `timestamp` | string | 🔄 Auto | Time in `HH:MM:SS` format (automatically added) |
| `date` | string | 🔄 Auto | Date in `YYYY-MM-DD` format (automatically added) |

---

## 💾 Data Storage

Events are stored in `/data/events.json` inside the add-on container:

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
    },
    {
      "type": "door",
      "title": "Front Door",
      "text": "Door opened",
      "timestamp": "15:20:42",
      "date": "2026-02-08"
    }
  ],
  "yesterday": []
}
```

**Storage Details:**
- Persistent across add-on restarts
- Automatically backed up by Home Assistant
- Located in `/addon_configs/[addon-slug]/`


---

## 📊 Logs

The add-on provides clean, minimal logging:

### Startup Log
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

### Event Logs
```
✓ Event: [doorbell] Doorbell
✓ Event: [door] Front Door
✓ Event: [energy] High Consumption
```

### Error Logs
```
✗ Error: Invalid JSON format
✗ Error: Missing required field 'title'
```

---

## 🐛 Troubleshooting

### Add-on Won't Start

**Symptoms:** Add-on shows as stopped, won't start

**Solutions:**
1. Check if port 8099 is already in use
2. Review add-on logs for errors
3. Try changing the port to 8100 or 8101
4. Restart Home Assistant

### Cannot Connect to API

**Symptoms:** Integration can't reach add-on, timeout errors

**Solutions:**
1. Verify add-on is running (green status)
2. Test connection: `http://homeassistant.local:8099/`
3. Check firewall settings
4. Ensure port matches integration configuration

### Events Not Saving

**Symptoms:** API accepts events but they don't appear

**Solutions:**
1. Check add-on logs for errors
2. Verify JSON format is correct
3. Ensure `/data` directory is writable
4. Check if `max_events_per_day` limit is reached
5. Restart the add-on

### Events Disappearing

**Symptoms:** Events vanish unexpectedly

**Solutions:**
1. Check if events are older than yesterday (auto-cleanup)
2. Verify `max_events_per_day` setting isn't too low
3. Check for multiple automations clearing events
4. Review add-on logs for cleanup messages

### Image Not Displaying

**Symptoms:** Events save but images don't show

**Solutions:**
1. Verify image path is correct (e.g., `/local/snapshot.jpg`)
2. Ensure image exists in `/config/www/` directory
3. Check file permissions
4. Use full URL if accessing externally

### High Memory Usage

**Symptoms:** Add-on using excessive RAM

**Solutions:**
1. Lower `max_events_per_day` setting
2. Check for very large image files
3. Restart add-on to clear cache
4. Review event cleanup settings

---

## 🔗 Related Resources

- [GitHub Repository](https://github.com/TillitschScHocK/DailyActivityFeed)
- [Integration Documentation](https://github.com/TillitschScHocK/DailyActivityFeed)
- [Report Issues](https://github.com/TillitschScHocK/DailyActivityFeed/issues)
- [Feature Requests](https://github.com/TillitschScHocK/DailyActivityFeed/issues)

---

**Made with ❤️ for Home Assistant**