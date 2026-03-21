#!/usr/bin/env python3
"""
Pixoo64 Kalender-Anzeige via iCal-Link
Zeigt tägliche Termine vom Outlook-Kalender auf dem Pixoo64
"""

import requests
from datetime import datetime, timedelta
from icalendar import Calendar
from zoneinfo import ZoneInfo
from pixoo import Pixoo
from config import ICAL_URL
from dateutil.rrule import rrulestr

# ===========================================
# KONFIGURATION - Anpassen!
# ===========================================
PIXOO_IP = "192.168.178.188"

# Zeitzone (Deutschland)
TIMEZONE = "Europe/Berlin"

# Anzahl Termine, die angezeigt werden sollen
MAX_EVENTS = 5

# Farben (RGB-Tupel)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_CYAN = (0, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)

# ===========================================
# Kalender Funktionen
# ===========================================

def download_ical(url):
    """Lädt den iCal-Feed herunter"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Calendar.from_ical(response.content)
    except Exception as e:
        raise Exception(f"Fehler beim Laden des Kalenders: {e}")

def get_todays_events(calendar):
    """Filtert die heutigen Termine aus dem Kalender"""
    tz = ZoneInfo(TIMEZONE)
    now = datetime.now(tz)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    events = []
    
    for component in calendar.walk():
        if component.name == "VEVENT":
            dtstart = component.get('dtstart')
            if not dtstart:
                continue
            
            # Basis-Startzeit
            start_dt = dtstart.dt
            if isinstance(start_dt, datetime):
                if start_dt.tzinfo is None:
                    start_dt = start_dt.replace(tzinfo=tz)
                else:
                    start_dt = start_dt.astimezone(tz)
            else:
                start_dt = datetime.combine(start_dt, datetime.min.time()).replace(tzinfo=tz)
            
            # Prüfen, ob RRULE vorhanden
            rrule = component.get('rrule')
            if rrule:
                # RRULE expandieren
                rrule_str = rrule.to_ical().decode('utf-8')
                rule = rrulestr(rrule_str, dtstart=start_dt)
                # Instanzen für heute generieren
                for instance in rule.between(today_start, today_end - timedelta(seconds=1), inc=True):
                    instance_tz = instance
                    if instance_tz.tzinfo is None:
                        instance_tz = instance_tz.replace(tzinfo=tz)
                    else:
                        instance_tz = instance_tz.astimezone(tz)
                    
                    if today_start <= instance_tz < today_end:
                        summary = str(component.get('summary', 'Kein Titel'))
                        location = component.get('location')
                        events.append({
                            'start': instance_tz,
                            'summary': summary,
                            'location': str(location) if location else None,
                            'is_allday': isinstance(dtstart.dt, datetime) == False
                        })
            else:
                # Einzeltermin prüfen
                if today_start <= start_dt < today_end:
                    summary = str(component.get('summary', 'Kein Titel'))
                    location = component.get('location')
                    events.append({
                        'start': start_dt,
                        'summary': summary,
                        'location': str(location) if location else None,
                        'is_allday': isinstance(dtstart.dt, datetime) == False
                    })
    
    # Nach Startzeit sortieren
    events.sort(key=lambda x: x['start'])
    return events

# ===========================================
# Hauptprogramm
# ===========================================

def main():
    print("=" * 60)
    print("Pixoo64 Kalender-Anzeige")
    print(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("=" * 60)
    
    # 1. Verbindung zum Pixoo herstellen
    print("\n[1] Verbinde mit Pixoo64...")
    try:
        pixoo = Pixoo(PIXOO_IP)
        print(f"   ✓ Verbunden mit {PIXOO_IP}")
        # Bildschirm einschalten
        print("   → Schalte Bildschirm ein...")
        pixoo.set_screen_on()
        pixoo.set_brightness(80)
        print("   ✓ Bildschirm eingeschaltet (Helligkeit: 80%)")
    except Exception as e:
        print(f"   ✗ Fehler: {e}")
        return
    
    # 2. Kalender laden
    print("\n[2] Lade Kalender...")
    try:
        calendar = download_ical(ICAL_URL)
        print("   ✓ Kalender geladen")
    except Exception as e:
        print(f"   ✗ Fehler: {e}")
        # Fehler auf Display anzeigen
        pixoo.clear()
        pixoo.draw_text("Kalender-", (5, 20), COLOR_RED)
        pixoo.draw_text("Fehler!", (5, 30), COLOR_RED)
        pixoo.push()
        return
    
    # 3. Heutige Termine filtern
    print("\n[3] Filtere heutige Termine...")
    events = get_todays_events(calendar)
    print(f"   ✓ {len(events)} Termine gefunden")
    
    # 4. Auf Pixoo anzeigen
    print("\n[4] Zeige auf Pixoo64...")
    
    try:
        # Canvas vorbereiten
        pixoo.clear()
        
        if not events:
            # Keine Termine
            message = "Keine Termine"
            print(f"   {message}")
            
            # Anzeige erstellen
            pixoo.draw_text(datetime.now().strftime("%d.%m.%Y"), 
                          (5, 10), COLOR_YELLOW)
            pixoo.draw_line((0, 18), (63, 18), COLOR_YELLOW)
            pixoo.draw_text(message, (5, 25), COLOR_GREEN)
            pixoo.draw_text("heute!", (15, 35), COLOR_GREEN)
            
        else:
            # Termine anzeigen
            y_pos = 2
            
            # Datum als Header
            header = datetime.now().strftime("%d.%m.%Y")
            pixoo.draw_text(header, (2, y_pos), COLOR_YELLOW)
            y_pos += 10
            
            # Linie unter Header
            pixoo.draw_line((0, y_pos), (63, y_pos), COLOR_YELLOW)
            y_pos += 4
            
            # Termine durchgehen (maximal 5)
            for i, event in enumerate(events[:MAX_EVENTS], 1):
                time_str = event['start'].strftime("%H:%M") if not event['is_allday'] else "GT"
                title = event['summary'][:12]  # Auf 12 Zeichen kürzen
                
                print(f"   {i}. {time_str} {event['summary']}")
                
                # Zeit
                pixoo.draw_text(time_str, (2, y_pos), COLOR_WHITE)
                
                # Titel
                pixoo.draw_text(title, (23, y_pos), COLOR_CYAN)
                
                y_pos += 9
                
                # Nach 5 Terminen ist das Display voll
                if i >= 5:
                    break
            
            # Falls mehr Termine vorhanden
            if len(events) > MAX_EVENTS:
                pixoo.draw_text(f"+{len(events)-MAX_EVENTS}", (2, y_pos), COLOR_RED)
        
        # Auf Display senden
        pixoo.push()
        print("   ✓ Anzeige aktualisiert")
        
    except Exception as e:
        print(f"   ✗ Fehler beim Anzeigen: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✓ Fertig!")
    print("=" * 60)

if __name__ == "__main__":
    main()