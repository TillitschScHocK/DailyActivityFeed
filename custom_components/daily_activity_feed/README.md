# Daily Activity Feed Integration

<img src="icon.png" width="128" height="128" alt="Icon">

## Overview

Home Assistant integration for the Daily Activity Feed add-on. Provides sensors to display event feeds in your dashboard **and a native action to add events from automations**.

### What it does

📊 **Creates Sensors** - `sensor.daily_activity_today` and `sensor.daily_activity_yesterday`  
🎬 **Native Action** - `daily_activity_feed.add_event` for automations (no YAML config needed!)  
📷 **Camera Integration** - Automatic snapshots via `camera_entity` parameter  
🔄 **Auto Updates** - Polls the add-on API at configurable intervals  
⚙️ **GUI Config** - No YAML configuration needed  
📋 **Rich Attributes** - All events stored in sensor attributes  

---

## Installation

### Via HACS (Recommended)

1. Open **HACS** → **Integrations**
2. Click **⋮** (menu) → **Custom repositories**
3. Add:
   - Repository: `https://github.com/TillitschScHocK/DAF---DailyActivityFeed`
   - Category: **Integration**
4. Download **Daily Activity Feed**
5. Restart Home Assistant

### Manual Installation

1. Copy `custom_components/daily_activity_feed` to your Home Assistant `custom_components` folder
2. Restart Home Assistant

---

## Configuration

1. **Settings** → **Devices & Services** → **Add Integration**
2. Search for **Daily Activity Feed**
3. Enter configuration:
   - **Add-on URL**: `http://addon-daily-activity-feed:8099` (default)
   - **Scan Interval**: 30 seconds (range: 10-300)

### Reconfigure

Change settings anytime:
1. **Settings** → **Devices & Services**
2. Click on **Daily Activity Feed**
3. Click **Configure**

---

## Actions

### `daily_activity_feed.add_event`

**NEW in v1.1.0** - Add events directly from automations without any YAML configuration!

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | ✅ | Event type (free text - any value you want) |
| `title` | ✅ | Short title |
| `text` | ✅ | Event description |
| `image` | ⬜ | Image URL (e.g. `/local/snapshot.jpg`) |
| `camera_entity` | ⬜ | Camera entity for automatic snapshot |
| `timestamp` | ⬜ | Custom timestamp (HH:MM:SS) |
| `priority` | ⬜ | Priority level (`low`, `normal`, `high`) |

**Example:**

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

---

## Sensors

### `sensor.daily_activity_today`

**State**: Number of events today  
**Attributes**:
```yaml
entries:
  - type: doorbell
    title: Doorbell
    text: Someone rang the doorbell
    timestamp: "14:32:15"
    date: "2026-02-08"
    image: /local/snapshot.jpg
date: "2026-02-08"
last_updated: "2026-02-08T14:32:15+01:00"
```

### `sensor.daily_activity_yesterday`

Same structure, but for yesterday's events.

---

## Usage in Dashboards

### Markdown Card Example

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
  <img src="{{ event.image }}" style="width: 100%; max-width: 400px; border-radius: 8px;">
      {% endif %}
    {% endfor %}
  {% else %}
  *No events today*
  {% endif %}
```

### Template Sensor Example

```yaml
template:
  - sensor:
      - name: "Latest Activity"
        state: >
          {% set events = state_attr('sensor.daily_activity_today', 'entries') %}
          {% if events and events|length > 0 %}
            {{ events[0].title }}
          {% else %}
            No events
          {% endif %}
        attributes:
          time: >
            {% set events = state_attr('sensor.daily_activity_today', 'entries') %}
            {% if events and events|length > 0 %}
              {{ events[0].timestamp }}
            {% endif %}
```

---

## Troubleshooting

### Integration not available
→ Ensure the add-on is running and accessible

### Sensors show unavailable
→ Check add-on URL in integration settings  
→ Test add-on API: `http://[HA-IP]:8099/`

### Action not available
→ Check Developer Tools → Actions  
→ Search for `daily_activity_feed.add_event`  
→ Restart Home Assistant if just installed

### Camera snapshot fails
→ Ensure camera entity exists  
→ Check `/config/www/` directory permissions

### Old events not clearing
→ The add-on handles cleanup automatically  
→ Check add-on logs for errors

---

## Technical Details

- **Platform**: sensor + action
- **Update Method**: Polling (configurable interval)
- **Data Source**: Daily Activity Feed add-on REST API
- **Storage**: Add-on handles all data persistence
- **Version**: 1.1.0

---

## What's New in v1.1.0

✨ Native `daily_activity_feed.add_event` action  
✨ No `rest_command` configuration needed  
✨ GUI support with text inputs and entity selectors  
✨ Automatic camera snapshots  
✨ Free text input for custom event types  
✨ Priority levels support  
✨ Full English interface  

---

## Support

[Report Issues](https://github.com/TillitschScHocK/DAF---DailyActivityFeed/issues) • [Documentation](https://github.com/TillitschScHocK/DAF---DailyActivityFeed)

---

**Part of the Daily Activity Feed ecosystem**
