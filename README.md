<div align="center">

# Daily Activity Feed

**Turn Home Assistant into a timeline - track events with camera snapshots**

[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=for-the-badge&logo=homeassistant)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/TillitschScHocK/DAF---DailyActivityFeed?style=for-the-badge)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue?style=for-the-badge&logo=paypal)](https://paypal.me/Schock07)

[Installation](#-installation) • [Usage](#-usage) • [Dashboard](#-dashboard) • [Support](#-support)

</div>

---

## 🎯 What is this?

Store and display Home Assistant events in a persistent timeline. Track doorbell rings, door openings, energy alerts, or anything else with optional camera snapshots.

**Key Features:**
- 📦 Events survive restarts
- 📸 Automatic camera snapshots
- 🎨 Beautiful dashboard cards
- ⚙️ Full GUI configuration
- 🧹 Auto-cleanup after 24h

---

## 🚀 Installation

### 1. Install Add-on

1. **Settings** → **Add-ons** → **Add-on Store** → **⋮** → **Repositories**
2. Add: `https://github.com/TillitschScHocK/DailyActivityFeed`
3. Install and start **Daily Activity Feed**

### 2. Install Integration

1. **HACS** → **Integrations** → **⋮** → **Custom repositories**
2. Add repository: `https://github.com/TillitschScHocK/DailyActivityFeed` (Category: Integration)
3. Download **Daily Activity Feed**
4. Restart Home Assistant
5. **Settings** → **Devices & Services** → **Add Integration** → Search "Daily Activity Feed"

Done! No YAML needed.

---

## 💻 Usage

### Add Events in Automations

Use the `daily_activity_feed.add_event` action in your automations:

**Required fields:**
- **Type**: Any text (e.g., `doorbell`, `security`, `package`)
- **Title**: Short headline
- **Text**: Event description

**Optional fields:**
- **Camera Entity**: Auto-capture snapshot
- **Priority**: `low`, `normal`, or `high`
- **Image URL**: Custom image path
- **Timestamp**: Custom time (HH:MM:SS)

### Example: Doorbell with Camera

```yaml
alias: Doorbell Alert
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

### Example: Door Monitoring

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
      title: "Front Door Opened"
      text: "Door opened at {{ now().strftime('%H:%M:%S') }}"
      priority: "normal"
```

---

## 🎨 Dashboard

Add this Markdown card to display your activity feed:

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

**Available sensors:**
- `sensor.daily_activity_today` (today's event count)
- `sensor.daily_activity_yesterday` (yesterday's event count)

All events are stored in the `entries` attribute.

---

## 🔧 Configuration

### Add-on Settings

```json
{
  "port": 8099,
  "max_events_per_day": 100
}
```

### Integration Settings

Configure after adding the integration:
- **Add-on URL**: `http://[HA-IP]:8099`
- **Scan interval**: 30 seconds (adjustable 10-300s)

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Add-on won't start | Check logs, ensure port 8099 is available |
| Integration not found | Verify add-on is running at `http://[HA-IP]:8099` |
| Action missing | Check Developer Tools → Actions |
| Camera snapshot fails | Verify camera entity and `/config/www/` permissions |

---

## ❤️ Support

Like this project? 

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue?style=for-the-badge&logo=paypal)](https://paypal.me/Schock07)

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**Made with ❤️ for Home Assistant**

[Report Bug](https://github.com/TillitschScHocK/DailyActivityFeed/issues) • [Request Feature](https://github.com/TillitschScHocK/DailyActivityFeed/issues)

</div>