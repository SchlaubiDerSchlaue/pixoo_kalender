"""Konfiguration — liest alle Werte aus Umgebungsvariablen."""

import os

ICAL_URL = os.getenv("ICAL_URL", "")
PIXOO_IP = os.getenv("PIXOO_IP", "192.168.178.188")
MAX_EVENTS = int(os.getenv("MAX_EVENTS", "5"))
TIMEZONE = os.getenv("TIMEZONE", "Europe/Berlin")
BRIGHTNESS = int(os.getenv("BRIGHTNESS", "80"))
