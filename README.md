# Pixoo64 Kalender-Anzeige

Einfaches Tool, um aus einem freigegebenen Outlook-Kalender die Termine des aktuellen Tags auf dem Pixoo64 Bildschirm darzustellen.

## Funktionen

- Lädt Termine aus einem iCal-Feed (z.B. Outlook-Kalender)
- Zeigt bis zu 5 Termine des aktuellen Tages an
- Unterstützt wiederkehrende Termine (RRULE)
- Zeigt Datum, Uhrzeit und Titel der Termine
- Automatische Anpassung an die Zeitzone (Europe/Berlin)

## Voraussetzungen

- Python 3.9 oder höher
- Pixoo64 Display im lokalen Netzwerk
- Freigegebener iCal-Link von Outlook oder einem anderen Kalenderdienst

## Installation

### Mit Docker (empfohlen)

1. Repository klonen oder herunterladen
2. `.env.example` nach `.env` kopieren:
   ```bash
   cp .env.example .env
   ```
3. `.env` anpassen (ICS-URL, Pixoo-IP etc.)
4. Container starten:
   ```bash
   docker compose up --build
   ```

Ohne Docker:

1. Virtuelle Umgebung erstellen (empfohlen):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
3. Umgebungsvariablen setzen oder `.env` laden

## Konfiguration

Alle Einstellungen werden über **Umgebungsvariablen** gesteuert. Kopiere `.env.example` nach `.env` und passe die Werte an:

| Variable | Beschreibung | Standard |
|---|---|---|
| `ICAL_URL` | iCal-Link vom Kalender (Outlook, Nextcloud, …) | — (required) |
| `PIXOO_IP` | IP-Adresse des Pixoo64 im LAN | `192.168.178.188` |
| `MAX_EVENTS` | Anzahl angezeigter Termine | `5` |
| `TIMEZONE` | Zeitzone | `Europe/Berlin` |
| `BRIGHTNESS` | Helligkeit 0–100 | `80` |

Unter Docker liest `docker-compose.yml` automatisch die `.env`-Datei.

## Verwendung

### Docker

```bash
docker compose up --build          # einmalig starten
docker compose up -d --build       # im Hintergrund (daemon)
docker compose logs -f             # Logs ansehen
```

### Direkt unter Python

```bash
export ICAL_URL="https://outlook.live.com/owa/calendar/.../calendar.ics"
export PIXOO_IP="192.168.178.188"
python pixoo_kalender.py
```

Das Programm:

1. Verbindet sich mit dem Pixoo64
2. Lädt den Kalender
3. Filtert die heutigen Termine
4. Zeigt sie auf dem Display an

## Fehlerbehebung

- Stelle sicher, dass der Pixoo64 eingeschaltet und im Netzwerk erreichbar ist
- Überprüfe den iCal-URL (funktioniert er im Browser?)
- Bei Zeitzonen-Problemen die `TIMEZONE` anpassen
- Unter Docker: `network_mode: host` ist erforderlich, damit der Container das Pixoo im lokalen Netz findet

## Abhängigkeiten

- `requests`: HTTP-Anfragen
- `icalendar`: iCal-Feed parsen
- `pixoo`: Pixoo64 Steuerung
- `python-dateutil`: RRULE-Verarbeitung
