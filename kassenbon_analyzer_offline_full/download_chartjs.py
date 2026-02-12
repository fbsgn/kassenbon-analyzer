#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chart.js Download-Helper für Offline-Paket

Lädt Chart.js herunter falls Internet verfügbar ist.
"""

import urllib.request
from pathlib import Path

CHARTJS_URL = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"
TARGET = Path(__file__).parent / "static" / "js" / "chart.umd.min.js"

def download_chartjs():
    print("=" * 60)
    print("Chart.js Download-Helper")
    print("=" * 60)
    
    if TARGET.exists():
        print(f"\n✓ Chart.js bereits vorhanden: {TARGET}")
        print("\nLösche die Datei wenn du sie neu herunterladen möchtest.")
        return
    
    print(f"\nLade herunter von: {CHARTJS_URL}")
    print(f"Ziel: {TARGET}")
    
    try:
        print("\n[...] Downloading...")
        with urllib.request.urlopen(CHARTJS_URL) as response:
            data = response.read()
        
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_bytes(data)
        
        size_kb = len(data) / 1024
        print(f"\n✅ ERFOLG! Chart.js heruntergeladen ({size_kb:.1f} KB)")
        print("\nDie App unterstützt jetzt Preisdiagramme!")
        
    except urllib.error.URLError as e:
        print(f"\n❌ FEHLER: Keine Internetverbindung")
        print(f"   {e}")
        print("\nDie App funktioniert auch ohne Chart.js,")
        print("aber OHNE Preisdiagramme.")
        print("\nAlternativ: Lade die Datei manuell herunter:")
        print(f"  {CHARTJS_URL}")
        print(f"und kopiere sie nach:")
        print(f"  {TARGET}")
        
    except Exception as e:
        print(f"\n❌ FEHLER: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    download_chartjs()
    input("\nDrücke Enter zum Beenden...")
