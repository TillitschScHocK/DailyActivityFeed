# Daily Activity Feed Add-on

## About

The Daily Activity Feed add-on provides a persistent storage and API for Home Assistant events. It stores events from today and yesterday, automatically cleaning up older entries.

## Features

- REST API for event submission
- Persistent JSON-based storage
- Automatic cleanup of old events
- Support for text and image attachments
- Integration with Home Assistant sensors

## Configuration

### Options

- **port** (integer): API port (default: 8099)
- **max_events_per_day** (integer): Maximum events to store per day (default: 100)

## API Endpoints

### POST /api/event
Add a new event

```json
{
  "type": "doorbell",
  "title": "Doorbell",
  "text": "Someone rang the doorbell",
  "image": "/local/snapshot.jpg"
}
```

### GET /api/events/today
Retrieve today's events

### GET /api/events/yesterday
Retrieve yesterday's events

### DELETE /api/events/{day}
Clear events for today or yesterday

## Usage

Configure the REST command in your `configuration.yaml`:

```yaml
rest_command:
  daily_activity_event:
    url: "http://addon-daily-activity-feed:8099/api/event"
    method: POST
    content_type: "application/json"
    payload: >
      {
        "type": "{{ type }}",
        "title": "{{ title }}",
        "text": "{{ text }}",
        "image": "{{ image | default('') }}"
      }
```

Then use it in your automations:

```yaml
action:
  - service: rest_command.daily_activity_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang the doorbell"
```

## Support

For issues and feature requests, please visit:
https://github.com/TillitschScHocK/DAF---DailyActivityFeed/issues
