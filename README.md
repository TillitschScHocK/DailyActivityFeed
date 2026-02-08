# Daily Activity Feed (DAF) für Home Assistant

[![GitHub Release](https://img.shields.io/github/v/release/TillitschScHocK/DAF---DailyActivityFeed)](https://github.com/TillitschScHocK/DAF---DailyActivityFeed/releases)
[![License](https://img.shields.io/github/license/TillitschScHocK/DAF---DailyActivityFeed)](LICENSE)

Ein persistentes Activity Feed System für Home Assistant, das Smart Home Ereignisse speichert und übersichtlich im Dashboard darstellt.

## ✨ Features

- **Persistente Speicherung** aller Ereignisse (heute und gestern)
- **Automatische Bereinigung** alter Daten
- **REST API** zum einfachen Hinzufügen von Events
- **Custom Integration** mit Sensoren für Home Assistant
- **Dashboard-Integration** mit flexiblen Lovelace Cards
- **Bild-Support** für Snapshots (z.B. von Kameras)
- **Typisierte Events** (doorbell, door, energy, custom)

## 🏗️ Architektur

```
┌────────────────────────┐
│   Home Assistant       │
│   Automations          │
└────────┬──────────────┘
         │
         │ HTTP POST
         │
         ▼
┌────────────────────────┐
│  DAF Addon (FastAPI)  │
│  - REST API           │
│  - SQLite/JSON Store  │
│  - Auto Cleanup       │
└────────┬──────────────┘
         │
         │ HTTP GET
         │
         ▼
┌────────────────────────┐
│  Custom Integration   │
│  - sensor.today       │
│  - sensor.yesterday   │
└────────┬──────────────┘
         │
         ▼
┌────────────────────────┐
│  Lovelace Dashboard   │
│  - Activity Feed      │
└────────────────────────┘
```

## 📦 Installation

### 1. Addon Installation

#### Option A: Manuell

1. Kopiere den Ordner `daily_activity_feed` nach `/addons/`
2. Gehe zu **Einstellungen** → **Add-ons** → **Add-on Store**
3. Klicke oben rechts auf die drei Punkte → **Repositories**
4. Füge hinzu: `https://github.com/TillitschScHocK/DAF---DailyActivityFeed`
5. Installiere das **Daily Activity Feed** Addon
6. Starte das Addon

#### Option B: Repository hinzufügen

1. **Einstellungen** → **Add-ons** → **Add-on Store** (drei Punkte oben rechts)
2. **Repositories** auswählen
3. URL hinzufügen: `https://github.com/TillitschScHocK/DAF---DailyActivityFeed`
4. Das Addon erscheint nun im Store

### 2. Custom Integration Installation

1. Kopiere den Ordner `custom_components/daily_activity_feed` nach `/config/custom_components/`
2. Starte Home Assistant neu
3. Füge zur `configuration.yaml` hinzu:

```yaml
daily_activity_feed:
  addon_url: "http://addon-daily-activity-feed:8099"
  scan_interval: 30
```

4. Starte Home Assistant erneut neu

### 3. REST Command einrichten

Füge zur `configuration.yaml` hinzu:

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

## 🚀 Verwendung

### Sensoren

Nach der Installation stehen dir zwei Sensoren zur Verfügung:

- `sensor.daily_activity_today` (Anzahl der Events heute)
- `sensor.daily_activity_yesterday` (Anzahl der Events gestern)

Jeder Sensor hat ein Attribut `entries`, das alle Events enthält:

```yaml
state: 5
attributes:
  entries:
    - type: doorbell
      title: Türklingel
      text: Es wurde an der Haustür geklingelt
      timestamp: "14:32:15"
      date: "2026-02-08"
      image: /local/doorbell_latest.jpg
    - type: door
      title: Haustür
      text: Die Haustür wurde geöffnet
      timestamp: "12:15:43"
      date: "2026-02-08"
```

### Automationen

#### Beispiel 1: Türklingel mit Snapshot

```yaml
alias: Türklingel Activity Feed
trigger:
  - platform: state
    entity_id: binary_sensor.doorbell
    to: "on"
action:
  - service: notify.mobile_app_handy
    data:
      message: "Es wurde geklingelt"
  - service: camera.snapshot
    target:
      entity_id: camera.doorbell
    data:
      filename: /config/www/doorbell_latest.jpg
  - service: rest_command.daily_activity_event
    data:
      type: "doorbell"
      title: "Türklingel"
      text: "Es wurde an der Haustür geklingelt"
      image: "/local/doorbell_latest.jpg"
```

#### Beispiel 2: Haustür geöffnet

```yaml
alias: Haustür Activity Feed
trigger:
  - platform: state
    entity_id: binary_sensor.front_door
    to: "on"
action:
  - service: notify.mobile_app_handy
    data:
      message: "Die Haustür wurde geöffnet"
  - service: rest_command.daily_activity_event
    data:
      type: "door"
      title: "Haustür"
      text: "Die Haustür wurde um {{ now().strftime('%H:%M') }} Uhr geöffnet"
```

#### Beispiel 3: Hoher Energieverbrauch

```yaml
alias: Hoher Verbrauch Activity Feed
trigger:
  - platform: numeric_state
    entity_id: sensor.house_power
    above: 5000
    for:
      minutes: 5
action:
  - service: notify.mobile_app_handy
    data:
      message: "Hausverbrauch überschreitet 5 kW"
  - service: rest_command.daily_activity_event
    data:
      type: "energy"
      title: "Hoher Verbrauch"
      text: "Aktueller Hausverbrauch: {{ states('sensor.house_power') }} W"
```

### Dashboard Integration

#### Einfache Markdown Card

```yaml
type: markdown
content: |
  ## 📋 Aktivitäten Heute
  
  {% set events = state_attr('sensor.daily_activity_today', 'entries') %}
  {% if events and events|length > 0 %}
    {% for event in events %}
  ---
  **{{ event.timestamp }}** - {{ event.title }}
  {{ event.text }}
      {% if event.image %}
  ![]({{ event.image }})
      {% endif %}
    {% endfor %}
  {% else %}
  _Keine Aktivitäten heute_
  {% endif %}
```

#### Mit custom:button-card (erfordert HACS)

```yaml
type: vertical-stack
cards:
  - type: custom:button-card
    name: Aktivitäten Heute
    icon: mdi:calendar-today
    entity: sensor.daily_activity_today
    show_state: true
    state_display: '[[[ return `${entity.state} Ereignisse` ]]]'
```

Weitere Beispiele findest du im Ordner [`examples/`](examples/).

## 🔧 API Dokumentation

### Endpoints

#### POST /api/event

Fügt ein neues Event hinzu.

**Request Body:**
```json
{
  "type": "doorbell",
  "title": "Türklingel",
  "text": "Es wurde geklingelt",
  "image": "/local/snapshot.jpg"
}
```

**Response:**
```json
{
  "status": "success",
  "event": {
    "type": "doorbell",
    "title": "Türklingel",
    "text": "Es wurde geklingelt",
    "image": "/local/snapshot.jpg",
    "timestamp": "14:32:15",
    "date": "2026-02-08"
  }
}
```

#### GET /api/events/today

Gibt alle Events von heute zurück.

**Response:**
```json
{
  "date": "2026-02-08",
  "count": 5,
  "events": [...]
}
```

#### GET /api/events/yesterday

Gibt alle Events von gestern zurück.

#### DELETE /api/events/{day}

Löscht alle Events eines Tages (`today` oder `yesterday`).

## 📝 Event Types

Du kannst beliebige Event Types verwenden. Empfohlene Standard-Typen:

- `doorbell` (Türklingel)
- `door` (Tür geöffnet/geschlossen)
- `energy` (Energieereignisse)
- `security` (Sicherheitsereignisse)
- `notification` (Allgemeine Benachrichtigungen)
- `device` (Geräte-Events)
- `custom` (Benutzerdefiniert)

## ⚙️ Konfiguration

### Addon Konfiguration

Im Addon selbst kannst du folgende Optionen anpassen:

```json
{
  "max_events_per_day": 100,
  "port": 8099
}
```

### Integration Konfiguration

In der `configuration.yaml`:

```yaml
daily_activity_feed:
  addon_url: "http://addon-daily-activity-feed:8099"
  scan_interval: 30  # Aktualisierung alle 30 Sekunden
```

## 🐛 Troubleshooting

### Addon startet nicht

1. Prüfe die Logs im Addon
2. Stelle sicher, dass Port 8099 nicht bereits belegt ist
3. Prüfe die Berechtigungen für `/data`

### Sensoren zeigen keine Daten

1. Prüfe, ob das Addon läuft
2. Teste die API manuell: `http://addon-daily-activity-feed:8099/api/events/today`
3. Prüfe die Logs der Custom Integration

### Events werden nicht gespeichert

1. Teste den REST Command manuell in den Developer Tools
2. Prüfe die Logs des Addons
3. Stelle sicher, dass der `rest_command` korrekt konfiguriert ist

## 📄 Datenspeicherung

Alle Events werden in `/data/events.json` gespeichert:

```json
{
  "today": [
    {
      "type": "doorbell",
      "title": "Türklingel",
      "text": "Es wurde geklingelt",
      "timestamp": "14:32:15",
      "date": "2026-02-08",
      "image": "/local/doorbell.jpg"
    }
  ],
  "yesterday": [...]
}
```

Die Daten werden automatisch bereinigt:
- Events älter als gestern werden gelöscht
- Beim Start des Addons
- Bei jedem neuen Event

## 🔐 Sicherheit

- Das Addon läuft nur lokal im Home Assistant Netzwerk
- Kein externer Zugriff erforderlich
- Alle Daten bleiben auf deinem System

## 📚 Weitere Ressourcen

- [Home Assistant Dokumentation](https://www.home-assistant.io/)
- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [Issues](https://github.com/TillitschScHocK/DAF---DailyActivityFeed/issues)

## 👏 Mitwirken

Beiträge sind willkommen! Bitte erstelle einen Pull Request oder öffne ein Issue.

## 📜 Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei.

## ❤️ Danksagungen

Erstellt mit Home Assistant, FastAPI und Liebe zum Detail.

---

**Hinweis:** Dieses Projekt befindet sich in aktiver Entwicklung. Feedback und Verbesserungsvorschläge sind herzlich willkommen!
