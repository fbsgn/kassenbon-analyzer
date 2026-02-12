╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║         KASSENBON-ANALYZER - OFFLINE VOLLVERSION                ║
║                                                                  ║
║         Vollständig eigenständiges Offline-Paket                ║
║         Mit Auto-Backup & Komfort-Features                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════
  🚀 SCHNELLSTART (für Eilige)
═══════════════════════════════════════════════════════════════════

Windows:
  1. INSTALL.bat ausführen (einmalig)
  2. START.bat ausführen
  3. Browser öffnet sich automatisch

Linux/macOS:
  1. chmod +x install.sh start.sh
  2. ./install.sh (einmalig)
  3. ./start.sh
  4. Browser zu http://127.0.0.1:5000

═══════════════════════════════════════════════════════════════════
  📋 VOLLSTÄNDIGE INSTALLATION (Schritt-für-Schritt)
═══════════════════════════════════════════════════════════════════

SCHRITT 1: Python installieren (falls noch nicht vorhanden)
   Windows: https://www.python.org/downloads/
            ⚠️ WICHTIG: "Add Python to PATH" anhaken!
   
   Linux:   sudo apt install python3 python3-pip
   macOS:   brew install python3

SCHRITT 2: Abhängigkeiten installieren
   Windows: Doppelklick auf INSTALL.bat
   
   Linux/macOS: 
      chmod +x install.sh
      ./install.sh

SCHRITT 3: App starten
   Windows: Doppelklick auf START.bat
   
   Linux/macOS:
      chmod +x start.sh
      ./start.sh

SCHRITT 4: Browser öffnen
   Die App ist erreichbar unter:
   http://127.0.0.1:5000

═══════════════════════════════════════════════════════════════════
  ✨ FEATURES
═══════════════════════════════════════════════════════════════════

✓ Vollständig offline nutzbar (kein Internet nötig)
✓ Automatisches Backup bei jedem Start
✓ PDF-Upload & Analyse (REWE, EDEKA, Lidl, Aldi, DM, Müller)
✓ Kategorie-Verwaltung mit Keywords
✓ Preisverlaufs-Tracking (optional mit Chart.js)
✓ Excel/CSV Export
✓ PWA-Support (als App installierbar)
✓ Responsive Design (Desktop, Tablet, Mobile)

═══════════════════════════════════════════════════════════════════
  📊 OPTIONAL: Preisdiagramme aktivieren
═══════════════════════════════════════════════════════════════════

Die App funktioniert komplett ohne Internet!

Für Preisverlaufs-Diagramme wird Chart.js benötigt:

AUTOMATISCH (mit Internet):
   Windows: python download_chartjs.py
   Linux:   python3 download_chartjs.py

MANUELL (ohne Internet):
   1. Lade herunter: 
      https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js
   2. Kopiere nach: static/js/chart.umd.min.js

═══════════════════════════════════════════════════════════════════
  💾 BACKUP & DATENSICHERHEIT
═══════════════════════════════════════════════════════════════════

AUTOMATISCHES BACKUP:
   ✓ Wird bei JEDEM Start automatisch erstellt
   ✓ Speicherort: backups/
   ✓ Gesichert: Datenbank + PDFs + Einstellungen

MANUELLES BACKUP:
   python backup_restore.py backup

BACKUPS ANZEIGEN:
   python backup_restore.py list

BACKUP WIEDERHERSTELLEN:
   python backup_restore.py restore <DATEINAME>
   ⚠️ Dein aktueller Stand wird vorher als Safety-Backup gesichert!

═══════════════════════════════════════════════════════════════════
  🌐 ERWEITERTE OPTIONEN
═══════════════════════════════════════════════════════════════════

LAN-ZUGRIFF (z.B. von Handy/Tablet):
   Windows: 
      set ALLOW_LAN=1
      python local_launch.py
   
   Linux/macOS:
      ALLOW_LAN=1 python local_launch.py
   
   Dann erreichbar unter: http://<DEINE-IP>:5000

PORT ÄNDERN:
   Bearbeite local_launch.py, Zeile:
   app.run(debug=False, host=host, port=5000)
   → ändere 5000 zu deinem Port

═══════════════════════════════════════════════════════════════════
  🐛 PROBLEMLÖSUNG
═══════════════════════════════════════════════════════════════════

"Python nicht gefunden":
   → Python 3.8+ installieren (siehe Schritt 1 oben)
   → Windows: Bei Installation "Add to PATH" anhaken!

"Module nicht gefunden" / "ImportError":
   → Führe INSTALL.bat / install.sh erneut aus
   → Oder manuell: pip install -r requirements.txt

"Port bereits belegt":
   → Anderer Dienst nutzt Port 5000
   → Port ändern (siehe Erweiterte Optionen)
   → Oder anderen Dienst stoppen

"Keine Preisdiagramme":
   → Chart.js fehlt (siehe "Preisdiagramme aktivieren")
   → App funktioniert trotzdem, nur ohne Diagramme

"Backup schlägt fehl":
   → Prüfe Schreibrechte im Ordner backups/
   → Stelle sicher, dass genug Speicherplatz frei ist

═══════════════════════════════════════════════════════════════════
  📁 ORDNERSTRUKTUR
═══════════════════════════════════════════════════════════════════

kassenbon_analyzer_offline_full/
│
├─ INSTALL.bat / install.sh       # Installation (einmalig)
├─ START.bat / start.sh           # App starten
├─ download_chartjs.py            # Chart.js Download-Helper
│
├─ web_app.py                     # Haupt-Anwendung
├─ local_launch.py                # Lokaler Server-Starter
├─ backup_restore.py              # Backup-System
│
├─ requirements.txt               # Python-Abhängigkeiten
├─ categories.json                # Kategorie-Einstellungen
├─ manifest.json                  # PWA Manifest
├─ service-worker.js              # Offline-Support
├─ index.html                     # Frontend
│
├─ backups/                       # Automatische Backups
├─ Ablage/                        # PDF-Archiv (wird erstellt)
├─ static/                        # Statische Dateien
│  ├─ icons/                      # App-Icons
│  └─ js/                         # JavaScript (Chart.js hier)
│
└─ receipts.db                    # Datenbank (wird erstellt)

═══════════════════════════════════════════════════════════════════
  📚 DOKUMENTATION
═══════════════════════════════════════════════════════════════════

Ausführliche Anleitung:     README_OFFLINE.md
Kategorie-Einstellungen:    (im Hauptprojekt)
Allgemeine Hilfe:           (im Hauptprojekt)

═══════════════════════════════════════════════════════════════════
  ℹ️  INFORMATION
═══════════════════════════════════════════════════════════════════

Version:      Offline-Full 2.0
Erstellt:     Februar 2026
Lizenz:       Für persönlichen Gebrauch
Support:      Siehe README_OFFLINE.md

═══════════════════════════════════════════════════════════════════

           Viel Erfolg mit dem Kassenbon-Analyzer! 🎉

═══════════════════════════════════════════════════════════════════
