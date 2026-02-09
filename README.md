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
✅ **Native action** - Use `daily_activity_feed.add_event` in automations  
✅ **GUI friendly** - Configure via UI with dropdowns and entity selectors  
✅ **Camera integration** - Automatic snapshots with `camera_entity`  
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

### ✨ That's it! No YAML configuration needed!

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
- **Add-on URL**: `http://addon-daily-activity-feed:8099` (default)
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

### 🎬 Actions

#### `daily_activity_feed.add_event`

Add events to your feed using the native Home Assistant action.

**Parameters:**

| Parameter | Required | Description | Example |
|-----------|----------|-------------|----------|
| `type` | ✅ | Event type | `doorbell`, `door`, `energy`, `security` |
| `title` | ✅ | Short title | `"Doorbell"` |
| `text` | ✅ | Event description | `"Someone rang the doorbell"` |
| `image` | ⬜ | Image URL | `"/local/snapshot.jpg"` |
| `camera_entity` | ⬜ | Camera for auto-snapshot | `"camera.front_door"` |
| `timestamp` | ⬜ | Custom timestamp (HH:MM:SS) | `"14:32:15"` |
| `priority` | ⬜ | Event priority | `low`, `normal`, `high` |

**🖥️ GUI Usage:**
1. In your automation, click **Add Action**
2. Search for `daily_activity_feed.add_event`
3. Fill in the fields using dropdowns and entity selectors:
   - **Type**: Dropdown with predefined options
   - **Title**: Text input
   - **Text**: Multi-line text input
   - **Camera Entity**: Entity selector (shows all cameras)
   - **Priority**: Dropdown (low/normal/high)

---

### 📝 Example Automations

#### Doorbell with Auto-Snapshot

```yaml
alias: Doorbell with Camera
trigger:
  - platform: state
    entity_id: binary_sensor.doorbell
    to: "on"
action:
  - action: daily_activity_feed.add_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang at {{ now().strftime('%H:%M') }}"
      camera_entity: camera.front_door
      priority: "high"
```

#### Door Opening with Context

```yaml
alias: Front Door Monitor
trigger:
  - platform: state
    entity_id: binary_sensor.front_door
    to: "on"
action:
  - action: daily_activity_feed.add_event
    data:
      type: "door"
      title: "Front Door Opened"
      text: >
        {% if is_state('alarm_control_panel.home', 'armed_away') %}
          ⚠️ Door opened while alarm is active!
        {% else %}
          Door opened at {{ now().strftime('%H:%M:%S') }}
        {% endif %}
      priority: >
        {% if is_state('alarm_control_panel.home', 'armed_away') %}
          high
        {% else %}
          normal
        {% endif %}
```

#### Energy Alert

```yaml
alias: High Power Consumption
trigger:
  - platform: numeric_state
    entity_id: sensor.power_consumption
    above: 3000
action:
  - action: daily_activity_feed.add_event
    data:
      type: "energy"
      title: "High Power Usage"
      text: "Consumption at {{ states('sensor.power_consumption') }} W"
      priority: "high"
```

#### Using Pre-existing Image

```yaml
alias: Motion with Snapshot
trigger:
  - platform: state
    entity_id: binary_sensor.motion_detected
    to: "on"
action:
  # Take snapshot first
  - action: camera.snapshot
    target:
      entity_id: camera.garden
    data:
      filename: /config/www/motion_{{ now().strftime('%Y%m%d_%H%M%S') }}.jpg
  
  # Add to feed
  - action: daily_activity_feed.add_event
    data:
      type: "security"
      title: "Motion Detected"
      text: "Motion in garden at {{ now().strftime('%H:%M') }}"
      image: "/local/motion_{{ now().strftime('%Y%m%d_%H%M%S') }}.jpg"
```

---

### 🎨 Dashboard Card

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
  "image": "/local/snapshot.jpg",
  "priority": "normal"
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

| Type | Description | Icon Suggestion |
|------|-------------|----------------|
| `doorbell` | Doorbell pressed | 🔔 |
| `door` | Door opened/closed | 🚪 |
| `energy` | Energy alerts | ⚡ |
| `security` | Security events | 🔒 |
| `device` | Device events | 📱 |
| `custom` | Anything else | ✨ |

---

## 🆕 What's New in v2.0.0

✨ **Native Action Support** - No more `rest_command` in `configuration.yaml`  
✨ **GUI Support** - Full UI integration with dropdowns and entity selectors  
✨ **Auto Camera Snapshots** - Use `camera_entity` parameter for automatic snapshots  
✨ **Priority Levels** - Mark events as `low`, `normal`, or `high` priority  
✨ **Better Error Handling** - Clear error messages in logs  
✨ **Template Support** - Full Jinja2 template support in all text fields  

### Migration from v1.x

If you're upgrading from v1.x:
1. Update the integration via HACS
2. **Remove** the `rest_command` from your `configuration.yaml`
3. Replace `rest_command.daily_activity_event` with `daily_activity_feed.add_event`
4. Change `service:` to `action:` in your automations
5. Restart Home Assistant

**Old (v1.x):**
```yaml
action:
  - service: rest_command.daily_activity_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang"
```

**New (v2.0):**
```yaml
action:
  - action: daily_activity_feed.add_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang"
      camera_entity: camera.front_door  # Optional auto-snapshot
```

---

## 🐛 Troubleshooting

**Add-on won't start**  
→ Check logs in add-on tab, ensure port 8099 is free

**Integration not found**  
→ Verify add-on is running, test `http://[HA-IP]:8099/`

**Action not available**  
→ Check Developer Tools → Actions, search for `daily_activity_feed.add_event`

**Camera snapshot fails**  
→ Ensure camera entity exists and `/config/www/` directory is writable

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
