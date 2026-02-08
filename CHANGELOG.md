# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

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

- HACS Integration
- Web-UI für Event-Verwaltung
- Erweiterte Filteroptionen
- Export-Funktion (CSV, JSON)
- Event-Kategorien und Tags
- Benachrichtigungsregeln
- SQLite als alternative Datenbank
- Event-Statistiken
- Mehrsprachige Unterstützung (Englisch)
