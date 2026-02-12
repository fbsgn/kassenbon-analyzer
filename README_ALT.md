# 🧾 Kassenbon-Analyzer

Eine Python-Anwendung zur automatischen Analyse und Klassifizierung von Kassenbons aus PDF-Dateien.

## 🌟 Features

- **PDF-Parsing**: Automatisches Auslesen von Kassenbon-PDFs
- **Artikel-Klassifizierung**: Intelligente Kategorisierung in:
  - Getränke
  - Obst & Gemüse
  - Milchprodukte
  - Fleisch & Wurst
  - Tiefkühlprodukte
  - Haushalt & Reinigung
  - Brot & Backwaren
  - Konserven & Haltbares
  - Sonstiges

- **Preisverlauf**: Tracking von Preisänderungen über Zeit
- **Statistiken**: Ausgaben pro Kategorie, durchschnittliche Preise
- **Einkaufshistorie**: Übersicht aller getätigten Einkäufe
- **Web-Interface**: Benutzerfreundliche Oberfläche
- **Artikelsuche**: Schnelles Finden von Produkten

## 📋 Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

## 🚀 Installation

### 1. Repository klonen oder Dateien kopieren

```bash
mkdir kassenbon-analyzer
cd kassenbon-analyzer
```

### 2. Abhängigkeiten installieren

```bash
pip install PyPDF2 Flask --break-system-packages
```

### 3. Anwendung starten

#### Kommandozeilen-Version:

```bash
python receipt_analyzer.py /pfad/zu/kassenbons/
```

#### Web-Interface:

```bash
python web_app.py
```

Dann Browser öffnen: `http://localhost:5000`

## 📁 Projektstruktur

```
kassenbon-analyzer/
│
├── receipt_analyzer.py    # Hauptanwendung (CLI)
├── web_app.py             # Web-Interface (Flask)
├── templates/
│   └── index.html         # HTML-Template
├── static/                # Statische Dateien
├── receipts.db            # SQLite-Datenbank (wird erstellt)
└── README.md              # Diese Datei
```

## 💻 Verwendung

### Kommandozeile

```bash
# Einzelnes Verzeichnis verarbeiten
python receipt_analyzer.py /pfad/zu/kassenbons/

# Mit Preisverlauf-Analyse
python receipt_analyzer.py /pfad/zu/kassenbons/
```

### Web-Interface

1. Server starten:
   ```bash
   python web_app.py
   ```

2. Browser öffnen: `http://localhost:5000`

3. PDF-Dateien hochladen per Drag & Drop oder File-Upload

4. Statistiken und Analysen werden automatisch aktualisiert

## 🔍 API-Endpunkte

Die Web-Anwendung bietet folgende REST-API:

### Upload
```
POST /api/upload
Content-Type: multipart/form-data
Body: file=<PDF-Datei>
```

### Statistiken
```
GET /api/statistics
Response: {
  "Getränke": {
    "count": 10,
    "total_spent": 45.50,
    "avg_price": 4.55
  },
  ...
}
```

### Einkaufshistorie
```
GET /api/history?limit=20
Response: [
  {
    "receipt_id": 1,
    "store_name": "EDEKA",
    "date": "2026-01-26T13:35:00",
    "total_amount": 42.01,
    "payment_method": "Mastercard"
  },
  ...
]
```

### Artikelsuche
```
GET /api/search?q=salat
Response: [
  {
    "name": "EHL BALLENSALAT",
    "category": "Obst & Gemüse",
    "avg_price": 1.49,
    "purchase_count": 2
  },
  ...
]
```

### Preisverlauf
```
GET /api/price-history/<item_name>
Response: [
  {
    "item_name": "EHL BALLENSALAT",
    "price": 1.99,
    "date": "2026-01-26T13:35:00",
    "store_name": "FFFrische-Center"
  },
  ...
]
```

## 🗄️ Datenbankschema

### Tabelle: receipts
```sql
- receipt_id (PRIMARY KEY)
- store_name
- store_address
- date
- total_amount
- payment_method
- created_at
```

### Tabelle: items
```sql
- item_id (PRIMARY KEY)
- receipt_id (FOREIGN KEY)
- name
- unit_price
- quantity
- total_price
- tax_category
- category
```

### Tabelle: price_history
```sql
- history_id (PRIMARY KEY)
- item_name
- price
- date
- store_name
```

## 🎯 Klassifizierung

Die Artikel werden anhand von Schlüsselwörtern klassifiziert:

| Kategorie | Schlüsselwörter |
|-----------|----------------|
| Getränke | wasser, cola, saft, bier, wein, etc. |
| Obst & Gemüse | möhren, zwiebel, salat, orange, etc. |
| Milchprodukte | joghurt, quark, milch, käse, etc. |
| Fleisch & Wurst | fleisch, wurst, schinken, etc. |
| Tiefkühl | pommes, frites, tk-, eis, etc. |
| Haushalt | reiniger, papier, salz, etc. |

## 📊 Beispiel-Ausgabe

```
KASSENBON-ANALYSE
============================================================

📊 Ausgaben nach Kategorie:
------------------------------------------------------------
Getränke                  32.66 € (6 Artikel, ⌀ 5.44 €)
Obst & Gemüse             14.04 € (8 Artikel, ⌀ 1.76 €)
Haushalt & Reinigung       6.37 € (3 Artikel, ⌀ 2.12 €)

🛒 Letzte Einkäufe:
------------------------------------------------------------
2026-01-26 13:34 | FFFrische-Center           |   42.01 € | Mastercard
2026-01-08 15:16 | EDEKA Schonungen           |   34.60 € | PAYBACK
```

## 🔧 Anpassungen

### Eigene Kategorien hinzufügen

In `receipt_analyzer.py`, Klasse `CategoryClassifier`:

```python
CATEGORIES = {
    'Meine Kategorie': [
        r'keyword1|keyword2|keyword3',
    ],
    # ...
}
```

### Parser-Regeln anpassen

Falls deine Kassenbons ein anderes Format haben, passe die Regex-Pattern in der Klasse `ReceiptParser` an.

## ⚠️ Bekannte Einschränkungen

- Funktioniert am besten mit deutschen Kassenbons
- PDF muss durchsuchbaren Text enthalten (kein Scan)
- Artikelnamen sind oft abgekürzt
- Preiserkennung basiert auf typischen Formaten

## 🐛 Fehlerbehebung

### PDF wird nicht erkannt
- Stelle sicher, dass das PDF durchsuchbaren Text enthält
- Teste mit `pdftotext` ob Text extrahiert werden kann

### Artikel werden falsch klassifiziert
- Passe die Schlüsselwörter in `CategoryClassifier` an
- Füge spezifische Begriffe für deine Produkte hinzu

### Datenbank-Fehler
- Lösche `receipts.db` und starte neu
- Prüfe Schreibrechte im Verzeichnis

## 📝 Lizenz

MIT License - Frei verwendbar für private und kommerzielle Projekte

## 🤝 Beitragen

Contributions sind willkommen! Erstelle einfach einen Pull Request oder öffne ein Issue.

## 💡 Ideen für Erweiterungen

- [ ] Export als Excel/CSV
- [ ] Visualisierung mit Charts (matplotlib/plotly)
- [ ] OCR für gescannte PDFs
- [ ] Mobile App
- [ ] Budgetverwaltung
- [ ] Vergleich zwischen Geschäften
- [ ] Automatische Einkaufsliste basierend auf Historie
- [ ] Rezeptvorschläge basierend auf gekauften Artikeln
- [ ] Push-Benachrichtigungen bei Preisänderungen

## 📧 Kontakt

Bei Fragen oder Problemen erstelle ein GitHub Issue.

---

**Viel Erfolg beim Analysieren deiner Einkäufe! 🛒📊**
