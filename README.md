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

1. Repository klonen oder herunterladen
2. Virtuelle Umgebung erstellen (empfohlen):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

## Konfiguration

1. `config.example.py` nach `config.py` kopieren
2. In `config.py` den iCal-URL eintragen:
   ```python
   ICAL_URL = "https://outlook.office365.com/owa/calendar/.../calendar.ics"
   ```
3. In `pixoo_kalender.py` die IP-Adresse des Pixoo64 anpassen:
   ```python
   PIXOO_IP = "192.168.178.188"  # Ihre Pixoo-IP
   ```

## Verwendung

Das Skript ausführen:

```bash
python pixoo_kalender.py
```

Das Programm:

1. Verbindet sich mit dem Pixoo64
2. Lädt den Kalender
3. Filtert die heutigen Termine
4. Zeigt sie auf dem Display an

## Anpassungen

- `MAX_EVENTS`: Maximale Anzahl angezeigter Termine (Standard: 5)
- `TIMEZONE`: Zeitzone (Standard: Europe/Berlin)
- Farben können in den Konstanten angepasst werden

## Fehlerbehebung

- Stelle sicher, dass der Pixoo64 eingeschaltet und im Netzwerk erreichbar ist
- Überprüfe den iCal-URL (funktioniert er im Browser?)
- Bei Zeitzonen-Problemen die TIMEZONE anpassen

## Abhängigkeiten

- `requests`: HTTP-Anfragen
- `icalendar`: iCal-Feed parsen
- `pixoo`: Pixoo64 Steuerung
- `python-dateutil`: RRULE-Verarbeitung
