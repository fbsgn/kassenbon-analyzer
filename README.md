# 🧾 Kassenbon-Analyzer

**Intelligente PDF-Kassenbon-Analyse mit automatischer Kategorisierung und Preisverlaufs-Tracking**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]() 
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Status](https://img.shields.io/badge/status-active-success)]()

---

## 📋 Features

- ✅ **PDF-Upload & Parsing** - Automatische Extraktion von Kassenbondaten
- 📊 **Kategorisierung** - Intelligente Zuordnung mit anpassbaren Keywords
- 💰 **Ausgaben-Tracking** - Übersicht nach Kategorien mit Visualisierung
- 📈 **Preisverlauf** - Historische Preisentwicklung einzelner Artikel
- 🔍 **Artikelsuche** - Schnelle Suche über alle Einkäufe
- 📥 **Excel/CSV Export** - Datenexport mit Filtern
- 🗂️ **PDF-Archiv** - Automatische Ablage der Original-PDFs
- 💾 **Backup-System** - Automatische Datensicherung
- 📱 **PWA-Support** - Als App installierbar (Desktop & Mobile)
- 🌐 **Offline-fähig** - Funktioniert komplett ohne Internet

### Unterstützte Geschäfte

REWE • EDEKA • Lidl • Aldi • dm • Müller • Kaufland • Penny • Netto • Norma • Rossmann

---

## 🚀 Quick Start

### Voraussetzungen

- Python 3.8 oder höher
- ca. 50 MB freier Speicherplatz

### Installation

**Windows:**
```cmd
git clone https://github.com/fbsgn/kassenbon-analyzer.git
cd kassenbon-analyzer
install.bat
```

**Linux/macOS:**
```bash
git clone https://github.com/fbsgn/kassenbon-analyzer.git
cd kassenbon-analyzer
chmod +x install.sh
./install.sh
```

### Starten

**Windows:**
```cmd
start_web.bat
```

**Linux/macOS:**
```bash
python3 web_app.py
```

Öffne im Browser: **http://localhost:5000**

---

## 📖 Dokumentation

### Hauptfunktionen

#### 1. PDF-Upload
- Drag & Drop oder Dateiauswahl
- Automatische Duplikat-Erkennung via Hash
- Batch-Import aus Ordner `PDF/`

#### 2. Kategorien verwalten
- **Einstellungen** (⚙️ oben rechts) öffnen
- Keywords hinzufügen/entfernen
- Kategorien anlegen/umbenennen/löschen
- **"Alle neu klassifizieren"** wendet neue Keywords an

#### 3. Ausgaben analysieren
- Filter nach Geschäft & Zeitraum
- Presets: "Diesen Monat", "Dieses Jahr", "Custom"
- Klick auf Kategorie → Details zu allen Artikeln
- Klick auf 📈 Icon → Preisverlauf eines Artikels

#### 4. Export
- CSV/Excel-Export mit aktuellen Filtern
- Format: Semikolon-separiert, Excel-kompatibel

---

## 🗂️ Projektstruktur

```
kassenbon-analyzer/
├─ web_app.py                    # Flask-Backend
├─ receipt_analyzer.py           # PDF-Parser & Klassifizierung
├─ batch_import.py               # Batch-Import-Logik
├─ category_api.py               # Kategorie-API (optional)
├─ migrate_db.py                 # Datenbank-Migration
├─ reclassify.py                 # Standalone Reklassifizierung
│
├─ templates/
│  └─ index.html                 # Frontend (Single-Page)
├─ static/
│  ├─ icons/                     # PWA-Icons
│  └─ js/                        # Optional: Chart.js
│
├─ manifest.json                 # PWA Manifest
├─ service-worker.js             # Offline-Support
├─ requirements.txt              # Python-Abhängigkeiten
│
├─ backup_erstellen.bat          # Backup-Tool
├─ backup_wiederherstellen.bat   # Restore-Tool
├─ reset.bat                     # System-Reset
├─ start_web.bat                 # Windows-Starter
├─ install.bat / install.sh      # Installation
│
├─ kassenbon_analyzer_offline_full/  # Offline-Paket
│  ├─ INSTALL.bat / install.sh   # Standalone-Installation
│  ├─ START.bat / start.sh       # Standalone-Starter
│  ├─ backup_restore.py          # Backup-System
│  ├─ download_chartjs.py        # Chart.js Download-Helper
│  └─ README_START_HIER.txt      # Vollständige Anleitung
│
└─ README.md                     # Diese Datei
```

---

## 💾 Datenbank-Schema

### Tabellen

**receipts** - Kassenbons
- `receipt_id` (PK), `store_name`, `date`, `total_amount`, `pdf_path`, `pdf_hash`

**items** - Artikel
- `item_id` (PK), `receipt_id` (FK), `name`, `unit_price`, `quantity`, `category`

**price_history** - Preisverlauf
- `history_id` (PK), `item_name`, `price`, `date`, `store_name`

---

## 🔧 Konfiguration

### Kategorien anpassen

1. Öffne **Einstellungen** (⚙️)
2. Bearbeite Keywords pro Kategorie
3. **Speichern** klicken
4. Optional: **"Alle neu klassifizieren"** für vorhandene Artikel

### Kategorien-Format (categories.json)

```json
{
  "Getränke - Softdrinks": [
    "cola",
    "fanta",
    "sprite"
  ],
  "Obst & Gemüse - Obst": [
    "apfel",
    "banane"
  ]
}
```

**Matching:** Einfache Substring-Suche (case-insensitive)

---

## 📦 Offline-Paket

Für vollständig eigenständige Nutzung ohne Internet:

```
kassenbon_analyzer_offline_full/
```

**Features:**
- ✅ Automatisches Backup bei jedem Start
- ✅ Einfache Installation (INSTALL.bat)
- ✅ Portable (USB-Stick-fähig)
- ✅ Keine Abhängigkeit vom Hauptprojekt

**Start:**
```cmd
cd kassenbon_analyzer_offline_full
START.bat
```

Siehe: [OFFLINE_PAKET_INFO.md](OFFLINE_PAKET_INFO.md)

---

## 🐛 Troubleshooting

### Server startet nicht

**Problem:** Port 5000 bereits belegt

**Lösung:**
```python
# In web_app.py, letzte Zeile ändern:
app.run(debug=False, host='0.0.0.0', port=8080)  # anderer Port
```

### PDF wird nicht erkannt

**Problem:** Geschäft/Format nicht unterstützt

**Lösung:**
1. Prüfe Konsolenausgabe auf Parser-Fehler
2. Öffne Issue mit anonymisierter PDF-Probe

### Kategorien werden nicht angewendet

**Problem:** Reklassifizierung nicht ausgeführt

**Lösung:**
1. Einstellungen öffnen
2. Auf **"🔄 Alle neu klassifizieren"** klicken
3. Bestätigen

---

## 🤝 Contributing

Contributions sind willkommen! 

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

---

## 📄 Lizenz

Dieses Projekt ist lizenziert unter der MIT-Lizenz - siehe [LICENSE](LICENSE) für Details.

---

## 🙏 Danksagungen

- [Flask](https://flask.palletsprojects.com/) - Web Framework
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF-Parsing
- [Chart.js](https://www.chartjs.org/) - Diagramme
- [dateparser](https://dateparser.readthedocs.io/) - Robustes Datum-Parsing

---

## 📧 Kontakt

Bei Fragen oder Problemen öffne bitte ein [Issue](https://github.com/fbsgn/kassenbon-analyzer/issues).

---

**Version:** 2.0  
**Erstellt:** Februar 2026  
**Status:** ✅ Production-Ready
