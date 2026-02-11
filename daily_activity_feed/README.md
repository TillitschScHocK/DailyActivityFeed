<div align="center">

# Daily Activity Feed Add-on

**Lightweight REST API for persistent Home Assistant event storage**

[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=for-the-badge&logo=homeassistant)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/TillitschScHocK/DAF---DailyActivityFeed?style=for-the-badge)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue?style=for-the-badge&logo=paypal)](https://paypal.me/Schock07)

</div>

---

## 🎯 About

This add-on provides the backend API for the Daily Activity Feed integration. It stores events in a persistent JSON database with automatic cleanup.

**Features:**
- ⚡ FastAPI REST backend
- 📦 Persistent JSON storage
- 🧹 Auto-cleanup (removes events older than yesterday)
- 📸 Image/snapshot support
- 🔄 Automatic date rollover

---

## 🚀 Quick Start

1. Start this add-on
2. Install the [Daily Activity Feed integration](https://github.com/TillitschScHocK/DailyActivityFeed) via HACS
3. Configure the integration to connect to this add-on
4. Use `daily_activity_feed.add_event` in your automations

See the **Documentation** tab for detailed API reference and examples.

---

## ⚙️ Configuration

```json
{
  "port": 8099,
  "max_events_per_day": 100
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `port` | 8099 | API port (change if already in use) |
| `max_events_per_day` | 100 | Maximum events stored per day |

**Note:** If you change the port, update the integration settings accordingly.

---

## 📊 Logs

The add-on provides clean logging:

**Startup:**
```
=========================================
Daily Activity Feed API
=========================================
Port: 8099
Max events/day: 100
Loaded: 6 today, 0 yesterday
Ready to accept events
=========================================
```

**Event received:**
```
✓ Event: [doorbell] Doorbell
```

---

<div align="center">

**Made with ❤️ for Home Assistant**

[Report Bug](https://github.com/TillitschScHocK/DailyActivityFeed/issues) • [Request Feature](https://github.com/TillitschScHocK/DailyActivityFeed/issues) • [Full Documentation](https://github.com/TillitschScHocK/DailyActivityFeed)

</div>