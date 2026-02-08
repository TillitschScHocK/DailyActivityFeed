<div align="center">

# Daily Activity Feed

**Persistent event storage for Home Assistant with beautiful dashboard integration**

[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=for-the-badge&logo=homeassistant)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/TillitschScHocK/DAF---DailyActivityFeed?style=for-the-badge)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue?style=for-the-badge&logo=paypal)](https://paypal.me/Schock07)

[Installation](#-installation) • [Configuration](#%EF%B8%8F-configuration) • [Usage](#-usage) • [API](#-api)

</div>

---

## 🎯 What is this?

Daily Activity Feed turns your Home Assistant into a timeline machine. Store and display events like doorbell rings, door openings, or energy alerts with optional camera snapshots - all in a beautiful, persistent feed.

### Why you'll love it

✅ **Zero data loss** - Events survive restarts  
✅ **Smart cleanup** - Auto-removes events older than yesterday  
✅ **Image support** - Attach camera snapshots to events  
✅ **HACS ready** - Install via GUI, no YAML hassle  
✅ **REST API** - Dead simple integration with automations  
✅ **Lightweight** - FastAPI backend, JSON storage  

---

## 🚀 Installation

### Step 1: Add-on

1. **Settings** → **Add-ons** → **Add-on Store** → **⋮** (menu) → **Repositories**
2. Add: `https://github.com/TillitschScHocK/DAF---DailyActivityFeed`
3. Install **Daily Activity Feed** from the store
4. Start the add-on

### Step 2: Integration

1. Open **HACS** → **Integrations** → **⋮** → **Custom repositories**
2. Add:
   - Repository: `https://github.com/TillitschScHocK/DAF---DailyActivityFeed`
   - Category: **Integration**
3. Download **Daily Activity Feed**
4. Restart Home Assistant
5. **Settings** → **Devices & Services** → **Add Integration**
6. Search for **Daily Activity Feed** and configure

### Step 3: REST Command

Add to `configuration.yaml` (only YAML needed):

```yaml
rest_command:
  daily_activity_event:
    url: "http://[HA-IP]/api/event"
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

Restart Home Assistant. Done! ✅

---

## ⚙️ Configuration

### Add-on Options

```json
{
  "port": 8099,
  "max_events_per_day": 100
}
```

### Integration

Configure via GUI after adding the integration:
- **Add-on URL**: `http://[HA-IP]:8099` (default)
- **Scan interval**: 30 seconds (10-300 range)

---

## 💻 Usage

### Sensors

Two sensors are created automatically:
- `sensor.daily_activity_today` - Today's event count
- `sensor.daily_activity_yesterday` - Yesterday's event count

All events are stored in the `entries` attribute:

```yaml
state: 3
attributes:
  entries:
    - type: doorbell
      title: Doorbell
      text: Someone rang the doorbell
      timestamp: "14:32:15"
      date: "2026-02-08"
      image: /local/doorbell_snapshot.jpg
```

### Example Automation

```yaml
alias: Doorbell with Snapshot
trigger:
  - platform: state
    entity_id: binary_sensor.doorbell
    to: "on"
action:
  # Take snapshot
  - service: camera.snapshot
    target:
      entity_id: camera.front_door
    data:
      filename: /config/www/doorbell_{{ now().strftime('%Y%m%d_%H%M%S') }}.jpg
  
  # Send to feed
  - service: rest_command.daily_activity_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang the doorbell at {{ now().strftime('%H:%M') }}"
      image: "/local/doorbell_{{ now().strftime('%Y%m%d_%H%M%S') }}.jpg"
```

### Dashboard Card

```yaml
type: markdown
content: |
  ## 📋 Activity Feed
  
  {% set events = state_attr('sensor.daily_activity_today', 'entries') %}
  {% if events and events|length > 0 %}
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

## 🔧 API

### POST `/api/event`
Create a new event

```json
{
  "type": "doorbell",
  "title": "Doorbell",
  "text": "Someone rang the doorbell",
  "image": "/local/snapshot.jpg"
}
```

### GET `/api/events/today`
Retrieve today's events

### GET `/api/events/yesterday`
Retrieve yesterday's events

### DELETE `/api/events/{day}`
Clear events (`day` = `today` or `yesterday`)

---

## 📝 Event Types

Use any type you want, or stick to these conventions:

| Type | Description |
|------|-------------|
| `doorbell` | Doorbell pressed |
| `door` | Door opened/closed |
| `energy` | Energy alerts |
| `security` | Security events |
| `device` | Device events |
| `custom` | Anything else |

---

## 🐛 Troubleshooting

**Add-on won't start**  
→ Check logs in add-on tab, ensure port 8099 is free

**Integration not found**  
→ Verify add-on is running, test `http://[HA-IP]]:8099/`

**No events showing**  
→ Check REST command in `configuration.yaml`, test in Developer Tools → Services

**HACS integration missing**  
→ Ensure category is "Integration", wait 2 minutes, restart HA

---

## ❤️ Support

Like this project? Consider supporting development:

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue?style=for-the-badge&logo=paypal)](https://paypal.me/Schock07)

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**Made with ❤️ for Home Assistant**

[Report Bug](https://github.com/TillitschScHocK/DAF---DailyActivityFeed/issues) • [Request Feature](https://github.com/TillitschScHocK/DAF---DailyActivityFeed/issues)

</div>
