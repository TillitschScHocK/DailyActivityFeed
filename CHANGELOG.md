# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-02-09

### 🎉 New Features

#### Native Action Integration
- **No YAML configuration needed!** The `rest_command` entry in `configuration.yaml` is no longer required
- New native action: `daily_activity_feed.add_event`
- Automatic action registration on integration setup
- Full integration with Home Assistant action browser
- Autocomplete and validation for all parameters
- **Modern syntax:** Uses `action:` instead of deprecated `service:`

#### GUI Support
- 🖥️ **Full UI integration** via `services.yaml`
- Text input for custom event types (not restricted to predefined values)
- Entity selector for camera selection
- Multi-line text fields for descriptions
- Dropdown for priority levels
- No YAML knowledge required
- Convenient configuration directly in the automation editor

#### Camera Integration
- Automatic snapshots via `camera_entity` parameter
- No manual `camera.snapshot` action needed
- Automatic filename generation with timestamp
- Storage in `/config/www/` with `/local/` URL
- Fallback on snapshot error (event is still created)

#### New Action Parameters
- `type`: Custom event type (free text input)
- `title`: Short title for the event
- `text`: Detailed description
- `image`: Optional image URL
- `camera_entity`: Automatic snapshot from camera entity
- `priority`: Event priority (`low`, `normal`, `high`)
- `timestamp`: Optional custom timestamp (HH:MM:SS)
- Full template support for all text parameters

### 🔧 Technical Improvements

- Modern async/await action handler
- Better error handling with meaningful messages
- Timeout handling for API calls (10 seconds)
- Action is only registered once (protection against double registration)
- Automatic action cleanup when removing the integration
- Optimized dependencies (`aiohttp>=3.9.0`)
- `services.yaml` for UI field definitions
- English translations throughout the integration

### 📚 Documentation

- Fully updated README in English
- Modern example automations with `action:` syntax
- GUI usage guide
- Migration guide from v1.0.x to v1.1.0
- Updated troubleshooting section
- Action parameter table with all options

### ⚡ Breaking Changes

**Migration required:**
1. Remove `rest_command.daily_activity_event` from `configuration.yaml`
2. Replace `rest_command.daily_activity_event` with `daily_activity_feed.add_event` in all automations
3. Change `service:` to `action:` (modern Home Assistant syntax)
4. Restart Home Assistant after integration update

**Old Syntax (v1.0.x):**
```yaml
action:
  - service: rest_command.daily_activity_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang"
      image: "/local/snapshot.jpg"
```

**New Syntax (v1.1.0):**
```yaml
action:
  - action: daily_activity_feed.add_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang"
      camera_entity: camera.front_door  # Automatic snapshot!
      priority: "high"
```

### 🐛 Bug Fixes

- Improved error handling for connection issues
- Better logging for debugging
- Correct cleanup logic when removing the integration
- Added missing `asyncio` import

---

## [1.0.0] - 2026-02-08

### Added

- Initial release of Daily Activity Feed add-on
- FastAPI-based REST API for event management
- Persistent storage in JSON format
- Automatic cleanup of old events (>1 day)
- Custom Home Assistant integration with two sensors:
  - `sensor.daily_activity_today`
  - `sensor.daily_activity_yesterday`
- Event types: doorbell, door, energy, security, notification, device, custom
- Support for images/snapshots
- Example automations for:
  - Doorbell with snapshot
  - Front door opened
  - High energy consumption
- Example Lovelace cards:
  - Simple Markdown card
  - Custom Button Card integration
- Full documentation
- API Endpoints:
  - `POST /api/event` - Add event
  - `GET /api/events/today` - Retrieve today's events
  - `GET /api/events/yesterday` - Retrieve yesterday's events
  - `DELETE /api/events/{day}` - Delete events
- Docker-based add-on for Home Assistant
- Configurable options:
  - Maximum events per day
  - API port
  - Scan interval

### Technical Details

- Python 3.11 Alpine-based Docker image
- FastAPI for REST API
- Uvicorn as ASGI server
- Pydantic for data validation
- JSON-based data storage
- Automatic cleanup on startup and with each event
- Support for all common architectures (aarch64, amd64, armhf, armv7, i386)

### Documentation

- Comprehensive README with installation instructions
- API documentation
- Example configurations
- Troubleshooting guide
- Architecture diagram

---

## [Unreleased]

### Planned

- Web UI for event management
- Advanced filtering options
- Export function (CSV, JSON)
- Event categories and tags
- Notification rules
- SQLite as alternative database
- Event statistics
- Multi-language support
- Custom event icons
- Event search and filter in dashboard
