# Kassenbon-Analyzer – Offline-Paket (Vollversion)

**Selbstständiges Offline-Paket** für vollständig lokalen Betrieb ohne Internet.

## ⚡ Quick Start

### Windows
```cmd
START.bat
```

### Linux/macOS
```bash
chmod +x start.sh
./start.sh
```

Die App öffnet sich automatisch auf **http://127.0.0.1:5000**

## 📦 Was ist enthalten?

- ✅ Vollständige Web-App mit allen Features
- ✅ **Automatisches Backup** bei jedem Start
- ✅ PWA-Support (kann als App installiert werden)
- ✅ Backup & Restore System
- ✅ Komfortable Start-Skripte

## 🎨 Optional: Preisdiagramme aktivieren

Die App funktioniert komplett ohne Internet, aber für **Preisdiagramme** wird Chart.js benötigt.

### Automatisch (mit Internet):
```bash
python download_chartjs.py
```

### Manuell (ohne Internet):
1. Lade `chart.umd.min.js` (v4.x) herunter von:
   https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js
2. Kopiere die Datei nach: `static/js/chart.umd.min.js`

**Hinweis:** Ohne Chart.js funktioniert die App, zeigt aber keine Preisverlaufs-Diagramme.

## 🔧 Erweiterte Optionen

### LAN-Zugriff erlauben (z.B. von Tablet/Handy)

**Windows (temporär):**
```cmd
set ALLOW_LAN=1
python local_launch.py
```

**Linux/macOS:**
```bash
ALLOW_LAN=1 python local_launch.py
```

Dann ist die App im LAN unter `http://<DEINE-IP>:5000` erreichbar.

### Port ändern

Bearbeite `local_launch.py` und ändere:
```python
app.run(debug=False, host=host, port=5000)  # z.B. port=8080
```

## 💾 Backup & Restore

### Backup erstellen (manuell)
```bash
python backup_restore.py backup
```
*Wird automatisch bei jedem Start gemacht!*

### Backups auflisten
```bash
python backup_restore.py list
```

### Backup wiederherstellen
```bash
python backup_restore.py restore <DATEINAME>
```
*Dein aktueller Zustand wird VOR dem Restore automatisch als Safety-Backup gesichert!*

## 📁 Gesicherte Daten

Bei jedem Backup werden gesichert:
- 📊 `receipts.db` – Die komplette Datenbank
- 📄 `Ablage/` – Alle PDF-Kassenbons
- ⚙️ `categories.json` – Deine Kategorie-Einstellungen

## 🔒 Sicherheit

- ✅ Standardmäßig nur lokal (127.0.0.1) erreichbar
- ✅ Automatische Backups bei jedem Start
- ✅ Safety-Backup vor jedem Restore
- ✅ Keine Daten verlassen deinen Computer

## 🐛 Probleme?

**Server startet nicht:**
- Prüfe ob Python 3.8+ installiert ist: `python --version`
- Installiere Abhängigkeiten: `pip install -r requirements.txt`
- Prüfe ob Port 5000 frei ist

**Backups funktionieren nicht:**
- Prüfe Schreibrechte im Ordner `backups/`

**Keine Preisdiagramme:**
- Chart.js fehlt! Siehe "Preisdiagramme aktivieren" oben

## 📚 Weitere Dokumentation

- Hauptprojekt: `../README.md`
- Kategorie-Einstellungen: `../KATEGORIE_SETTINGS_ANLEITUNG.txt`
- Allgemeine Hilfe: `../SCHNELLSTART.txt`

---

**Version:** Offline-Full 2.0  
**Erstellt:** Februar 2026
