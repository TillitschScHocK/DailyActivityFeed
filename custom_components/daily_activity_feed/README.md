# Daily Activity Feed Integration

<img src="brand/icon.png" width="128" height="128" alt="Icon">

## Overview

Home Assistant integration that connects to the Daily Activity Feed add-on. Track events in a beautiful timeline with camera snapshots.

**Key Features:**
- 📊 Two sensors: `sensor.daily_activity_today` and `sensor.daily_activity_yesterday`
- 🎬 Native action: `daily_activity_feed.add_event` for automations
- 📷 Automatic camera snapshots
- ⚙️ Full GUI configuration
- 📋 All events stored in sensor attributes

---

## Installation

### Via HACS (Recommended)

1. **HACS** → **Integrations** → **⋮** → **Custom repositories**
2. Add repository: `https://github.com/TillitschScHocK/DailyActivityFeed` (Category: Integration)
3. Download **Daily Activity Feed**
4. Restart Home Assistant

### Setup

1. **Settings** → **Devices & Services** → **Add Integration**
2. Search for **Daily Activity Feed**
3. Configure:
   - **Add-on URL**: `http://[HA-IP]]:8099`
   - **Scan Interval**: 30 seconds (10-300 range)

---

## Usage

### Add Events in Automations

Use the `daily_activity_feed.add_event` action:

```yaml
action:
  - action: daily_activity_feed.add_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang at {{ now().strftime('%H:%M') }}"
      camera_entity: camera.front_door
      priority: "high"
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | ✅ | Event type (any text: `doorbell`, `door`, `security`, etc.) |
| `title` | ✅ | Short headline |
| `text` | ✅ | Event description |
| `camera_entity` | ⬜ | Camera for auto-snapshot |
| `priority` | ⬜ | `low`, `normal`, or `high` |
| `image` | ⬜ | Custom image path |
| `timestamp` | ⬜ | Custom time (HH:MM:SS) |

### Example: Door Monitor

```yaml
alias: Front Door
trigger:
  - platform: state
    entity_id: binary_sensor.front_door
    to: "on"
action:
  - action: daily_activity_feed.add_event
    data:
      type: "door"
      title: "Front Door"
      text: "Door opened at {{ now().strftime('%H:%M:%S') }}"
```

---

## Dashboard Card

Display your activity feed with a Markdown card:

```yaml
type: markdown
content: |
  ## 📋 Today's Activity
  
  {% set events = state_attr('sensor.daily_activity_today', 'entries') %}
  {% if events and events|length > 0%}
    {% for event in events %}
  ---
  **{{ event.timestamp }}** - {{ event.title }}
  {{ event.text }}
      {% if event.image %}
  <img src="{{ event.image }}" style="width: 100%; max-width: 400px; border-radius: 8px; margin-top: 8px;">
      {% endif %}
    {% endfor %}
  {% else %}
  *No events today*
  {% endif %}
```

---

## Sensors

### `sensor.daily_activity_today`

**State:** Number of today's events

**Attributes:**
```yaml
entries:
  - type: doorbell
    title: Doorbell
    text: Someone rang the doorbell
    timestamp: "14:32:15"
    date: "2026-02-08"
    image: /local/snapshot.jpg
```

### `sensor.daily_activity_yesterday`

Same structure for yesterday's events.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Integration not found | Ensure add-on is running at configured URL |
| Sensors unavailable | Check add-on URL in integration settings |
| Action missing | Restart Home Assistant, check Developer Tools → Actions |
| Camera snapshot fails | Verify camera entity and `/config/www/` permissions |

---

## Support

[Report Issues](https://github.com/TillitschScHocK/DailyActivityFeed/issues) • [GitHub](https://github.com/TillitschScHocK/DailyActivityFeed)

---

**Part of the Daily Activity Feed ecosystem**