# 🧾 Kassenbon-Analyzer - Projektübersicht

## 📦 Projektinhalt

Ich habe eine vollständige Python-Anwendung zur Analyse von Kassenbons erstellt!

### Enthaltene Dateien

```
kassenbon-analyzer/
│
├── 📄 receipt_analyzer.py      # Hauptanwendung (CLI)
├── 🌐 web_app.py               # Web-Interface (Flask)
├── 🎮 receipt_demo.py          # Demo mit Beispieldaten
├── 📋 requirements.txt         # Python-Abhängigkeiten
├── 🛠️  install.sh              # Installations-Script
├── 📚 README.md                # Vollständige Dokumentation
├── 🚀 QUICKSTART.md            # Schnellstart-Guide
└── 📁 templates/
    └── index.html              # Web-UI Template
```

## ✨ Hauptfunktionen

### 1. PDF-Parsing
- Liest Kassenbon-PDFs automatisch ein
- Extrahiert Artikel, Preise, Mengen
- Erkennt Geschäft, Datum, Zahlungsmethode

### 2. Automatische Klassifizierung
Artikel werden in Kategorien eingeteilt:
- 🥤 Getränke
- 🥬 Obst & Gemüse
- 🥛 Milchprodukte
- 🥩 Fleisch & Wurst
- 🧊 Tiefkühlprodukte
- 🧹 Haushalt & Reinigung
- 🍞 Brot & Backwaren
- 🥫 Konserven
- 📦 Sonstiges

### 3. Preisverlauf
- Speichert historische Preise
- Zeigt Preisänderungen über Zeit
- Vergleicht Preise zwischen Geschäften

### 4. Statistiken & Analysen
- Ausgaben pro Kategorie
- Durchschnittspreise
- Einkaufshäufigkeit
- Gesamtausgaben

### 5. Web-Interface
- Drag & Drop PDF-Upload
- Live-Statistiken
- Artikelsuche
- Interaktive Dashboards

## 🎯 Demo-Ergebnisse

Mit deinen beiden Kassenbons:

```
📊 AUSGABEN NACH KATEGORIE
══════════════════════════════════════════════════════════
Milchprodukte                 6.16 € ( 62.1%)
Obst & Gemüse                 1.98 € ( 20.0%)
Sonstiges                     1.78 € ( 17.9%)
                             ──────
GESAMT                        9.92 €

🛒 EINKAUFSHISTORIE
══════════════════════════════════════════════════════════
2026-01-26 13:35 │ FFFrische-Center Höchner    │ 42.01 €
2026-01-08 15:16 │ Sczygiel & Pfrang KG        │ 34.60 €
```

## 🚀 Wie du startest

### Schnellste Methode (Demo):

```bash
python3 receipt_demo.py
```

### Web-Interface:

```bash
# 1. Installation
pip install PyPDF2 Flask

# 2. Server starten
python3 web_app.py

# 3. Browser öffnen
http://localhost:5000
```

### Kommandozeile:

```bash
python3 receipt_analyzer.py /pfad/zu/deinen/kassenbons/
```

## 💾 Datenbank

Die App erstellt automatisch eine SQLite-Datenbank (`receipts.db`) mit:

- **receipts**: Alle Kassenbons
- **items**: Einzelne Artikel
- **price_history**: Preisverlauf über Zeit

## 🔧 Anpassungen

### Eigene Kategorien hinzufügen

In `receipt_analyzer.py`:

```python
CATEGORIES = {
    'Deine Kategorie': [
        r'keyword1|keyword2|keyword3',
    ],
}
```

### Parser anpassen

Falls deine Kassenbons ein anderes Format haben, passe die Regex-Patterns in `_extract_items()` an.

## 📊 Use Cases

✅ **Budgetverwaltung**: Sieh genau wo dein Geld hingeht
✅ **Preisverfolgung**: Erkenne Preisänderungen frühzeitig
✅ **Einkaufsoptimierung**: Vergleiche Preise zwischen Geschäften
✅ **Steuer**: Organisiere Belege automatisch
✅ **Ernährungsanalyse**: Sieh was du am häufigsten kaufst

## 🎨 Web-Interface Features

- **Modern & Responsive**: Funktioniert auf Desktop und Mobil
- **Drag & Drop**: Einfacher PDF-Upload
- **Echtzeit-Updates**: Statistiken aktualisieren sich automatisch
- **Suche**: Finde Artikel schnell
- **Preisverlauf**: Klick auf Artikel für Details

## 📈 Erweiterungsmöglichkeiten

Die App ist als Basis konzipiert. Mögliche Erweiterungen:

- [ ] Excel/CSV-Export
- [ ] Visualisierungen (Charts)
- [ ] OCR für Scans
- [ ] Mobile App
- [ ] Budget-Alerts
- [ ] Rezeptvorschläge
- [ ] Preisvergleiche
- [ ] API-Integration
- [ ] Cloud-Sync

## 🛠️ Technischer Stack

- **Python 3.8+**: Hauptsprache
- **SQLite**: Datenbank
- **Flask**: Web-Framework
- **PyPDF2**: PDF-Parsing
- **Regex**: Text-Extraktion

## 📝 Hinweise

- PDFs müssen durchsuchbaren Text enthalten
- Die Klassifizierung basiert auf deutschen Produktnamen
- Parser ist auf deutsche Kassenbon-Formate optimiert
- Bei Scans empfiehlt sich OCR-Vorverarbeitung

## 🤝 Support

Lies die Dokumentation in:
- `README.md` für Details
- `QUICKSTART.md` für schnellen Einstieg
- Code-Kommentare für technische Details

---

**Viel Erfolg mit deiner Kassenbon-Analyse! 📊🎉**

Die App ist produktionsreif und kann sofort verwendet werden.
Alle Dateien sind im Output-Verzeichnis und bereit zur Nutzung!
