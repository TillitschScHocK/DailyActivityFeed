# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [2.0.0] - 2026-02-09

### 🎉 Hauptfeatures

#### Native Action-Integration
- **Kein YAML mehr nötig!** Der `rest_command` Eintrag in der `configuration.yaml` ist nicht mehr erforderlich
- Neue native Action: `daily_activity_feed.add_event`
- Automatische Action-Registrierung bei Integration-Setup
- Vollständige Integration in Home Assistant Action-Browser
- Autocomplete und Validierung für alle Parameter
- **Moderne Syntax:** Verwendet `action:` statt des veralteten `service:`

#### GUI-Unterstützung
- 🖥️ **Vollständige UI-Integration** durch `services.yaml`
- Dropdowns für Event-Typen und Prioritäten
- Entity-Selector für Kamera-Auswahl
- Mehrzeilige Textfelder für Beschreibungen
- Keine YAML-Kenntnisse mehr erforderlich
- Komfortable Konfiguration direkt im Automation-Editor

#### Kamera-Integration
- Automatische Snapshots über `camera_entity` Parameter
- Keine manuelle `camera.snapshot` Action mehr nötig
- Automatische Dateinamen-Generierung mit Zeitstempel
- Speicherung in `/config/www/` mit `/local/` URL
- Fallback bei Snapshot-Fehler (Event wird trotzdem erstellt)

#### Neue Action-Parameter
- `camera_entity`: Automatischer Snapshot von Kamera-Entity
- `priority`: Event-Priorität (`low`, `normal`, `high`)
- `timestamp`: Optionaler eigener Zeitstempel (HH:MM:SS)
- Vollständige Template-Unterstützung für alle Text-Parameter

### 🔧 Technische Verbesserungen

- Moderne async/await Action-Handler
- Bessere Fehlerbehandlung mit aussagekräftigen Meldungen
- Timeout-Handling für API-Aufrufe (10 Sekunden)
- Action wird nur einmal registriert (Schutz vor Doppel-Registrierung)
- Automatisches Action-Cleanup beim Entfernen der Integration
- Optimierte Abhängigkeiten (`aiohttp>=3.9.0`)
- `services.yaml` für UI-Feld-Definitionen

### 📚 Dokumentation

- Vollständig aktualisiertes README
- Moderne Beispiel-Automationen mit `action:` Syntax
- GUI-Nutzungs-Anleitung
- Moderne Beispiele:
  - Türklingel mit Auto-Snapshot
  - Tür-Monitor mit Kontext-Logik
  - Energie-Warnungen
  - Motion Detection mit Bildern
- Migrations-Guide von v1.x zu v2.0
- Aktualisierte Troubleshooting-Sektion
- Action-Parameter-Tabelle mit allen Optionen

### ⚡ Breaking Changes

**Migration erforderlich:**
1. Entfernen des `rest_command.daily_activity_event` aus `configuration.yaml`
2. Ersetzen von `rest_command.daily_activity_event` durch `daily_activity_feed.add_event` in allen Automationen
3. Ändern von `service:` zu `action:` (moderne Home Assistant Syntax)
4. Home Assistant Neustart nach Integration-Update

**Alte Syntax (v1.x):**
```yaml
action:
  - service: rest_command.daily_activity_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang"
      image: "/local/snapshot.jpg"
```

**Neue Syntax (v2.0):**
```yaml
action:
  - action: daily_activity_feed.add_event
    data:
      type: "doorbell"
      title: "Doorbell"
      text: "Someone rang"
      camera_entity: camera.front_door  # Automatischer Snapshot!
      priority: "high"
```

### 🐛 Bugfixes

- Verbesserte Fehlerbehandlung bei Verbindungsproblemen
- Besseres Logging für Debugging
- Korrekte Cleanup-Logik beim Entfernen der Integration
- Fehlender `asyncio` Import hinzugefügt

---

## [1.0.0] - 2026-02-08

### Hinzugefügt

- Initiales Release des Daily Activity Feed Addons
- FastAPI-basierte REST API für Event-Verwaltung
- Persistente Speicherung in JSON-Format
- Automatische Bereinigung alter Events (>1 Tag)
- Custom Home Assistant Integration mit zwei Sensoren:
  - `sensor.daily_activity_today`
  - `sensor.daily_activity_yesterday`
- Event-Typen: doorbell, door, energy, security, notification, device, custom
- Unterstützung für Bilder/Snapshots
- Beispiel-Automationen für:
  - Türklingel mit Snapshot
  - Haustür geöffnet
  - Hoher Energieverbrauch
- Beispiel-Lovelace-Cards:
  - Einfache Markdown Card
  - Custom Button Card Integration
- Vollständige deutsche Dokumentation
- API Endpoints:
  - `POST /api/event` - Event hinzufügen
  - `GET /api/events/today` - Heutige Events abrufen
  - `GET /api/events/yesterday` - Gestrige Events abrufen
  - `DELETE /api/events/{day}` - Events löschen
- Docker-basiertes Addon für Home Assistant
- Konfigurierbare Optionen:
  - Maximale Events pro Tag
  - API Port
  - Scan-Intervall

### Technische Details

- Python 3.11 Alpine-basiertes Docker Image
- FastAPI für REST API
- Uvicorn als ASGI Server
- Pydantic für Datenvalidierung
- JSON-basierte Datenspeicherung
- Automatisches Cleanup bei Startup und jedem Event
- Unterstützung für alle gängigen Architekturen (aarch64, amd64, armhf, armv7, i386)

### Dokumentation

- Umfassendes README mit Installationsanleitung
- API-Dokumentation
- Beispiel-Konfigurationen
- Troubleshooting-Guide
- Architektur-Diagramm

---

## [Unreleased]

### Geplant

- Web-UI für Event-Verwaltung
- Erweiterte Filteroptionen
- Export-Funktion (CSV, JSON)
- Event-Kategorien und Tags
- Benachrichtigungsregeln
- SQLite als alternative Datenbank
- Event-Statistiken
- Mehrsprachige Unterstützung (Englisch)
- Custom Event-Icons
- Event-Suche und Filter in Dashboard
