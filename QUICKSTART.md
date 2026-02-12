# 🚀 Quick Start Guide

## Schnellstart in 3 Schritten

### 1. Installation

```bash
# Klone oder lade das Projekt herunter
cd kassenbon-analyzer

# Führe das Installations-Script aus
chmod +x install.sh
./install.sh
```

Oder manuell:
```bash
pip install PyPDF2 Flask
```

### 2. Demo ausführen

Teste die Anwendung mit den Beispieldaten:

```bash
python3 receipt_demo.py
```

Du solltest eine Ausgabe wie diese sehen:

```
🧾 Kassenbon-Analyzer Demo
======================================================================

Verarbeite Kassenbon 1...
  ✓ 13 Artikel gespeichert

📊 AUSGABEN NACH KATEGORIE
======================================================================
Getränke                  19.28 € (45.9%) [4 Artikel, ⌀ 4.82 €]
Obst & Gemüse             14.04 € (33.4%) [8 Artikel, ⌀ 1.76 €]
...
```

### 3. Eigene Kassenbons verarbeiten

#### Option A: Web-Interface

```bash
python3 web_app.py
```

Öffne dann im Browser: `http://localhost:5000`

Hier kannst du:
- PDFs per Drag & Drop hochladen
- Statistiken in Echtzeit sehen
- Nach Artikeln suchen
- Preisentwicklungen verfolgen

#### Option B: Kommandozeile

```bash
python3 receipt_analyzer.py /pfad/zu/deinen/kassenbons/
```

## 📁 Deine Kassenbons organisieren

Empfohlene Verzeichnisstruktur:

```
~/Dokumente/Kassenbons/
├── 2026/
│   ├── 01-Januar/
│   │   ├── kassenbon-2026-01-08.pdf
│   │   └── kassenbon-2026-01-26.pdf
│   └── 02-Februar/
└── 2025/
```

Dann einfach ausführen:
```bash
python3 receipt_analyzer.py ~/Dokumente/Kassenbons/2026/01-Januar/
```

## 🎯 Was wird analysiert?

Die App extrahiert automatisch:

- ✅ **Artikel**: Name, Preis, Menge
- ✅ **Kategorie**: Automatische Klassifizierung
- ✅ **Geschäft**: Name und Adresse
- ✅ **Datum & Uhrzeit**
- ✅ **Zahlungsmethode**
- ✅ **Gesamtbetrag**

Und erstellt:

- 📊 Ausgabenstatistiken nach Kategorie
- 📈 Preisverlauf für jeden Artikel
- 🛒 Chronologische Einkaufshistorie
- 🔍 Durchsuchbare Artikeldatenbank

## 💡 Tipps

### Beste Ergebnisse

1. **PDF-Qualität**: Kassenbons sollten durchsuchbaren Text enthalten
2. **Scannen**: Bei Scans verwende hohe Auflösung (300 DPI+)
3. **Benennung**: Nutze sprechende Dateinamen (z.B. `EDEKA_2026-01-26.pdf`)

### Kategorien anpassen

Bearbeite `receipt_analyzer.py` und passe die `CATEGORIES` an:

```python
CATEGORIES = {
    'Meine Kategorie': [
        r'keyword1|keyword2',  # Regex-Pattern
    ],
}
```

### Datenbank zurücksetzen

```bash
rm receipts.db
python3 receipt_demo.py  # Erstellt neue Datenbank
```

## 🔧 Problemlösung

### "PDF kann nicht gelesen werden"

- Prüfe ob das PDF Text enthält: `pdftotext kassenbon.pdf -`
- Falls Scan: Nutze OCR-Software zuerst

### "Keine Artikel gefunden"

- Der Parser erkennt nur bestimmte Formate
- Schau dir die Regex-Patterns in `_extract_items()` an
- Passe sie an dein Kassenbon-Format an

### "Module not found"

```bash
pip install PyPDF2 Flask --upgrade
```

## 📊 Beispiel-Auswertungen

### Monatsausgaben

```python
# In Python
from receipt_analyzer import ReceiptDatabase

db = ReceiptDatabase()
stats = db.get_category_statistics()
total = sum(s['total_spent'] for s in stats.values())
print(f"Diesen Monat ausgegeben: {total:.2f} €")
```

### Top 10 Artikel

```sql
-- Direkt in der Datenbank (receipts.db)
SELECT name, COUNT(*) as count, AVG(unit_price) as avg_price
FROM items
WHERE category != 'System'
GROUP BY name
ORDER BY count DESC
LIMIT 10;
```

## 🌟 Nächste Schritte

- [ ] Automatisiere den Upload (z.B. per Cron-Job)
- [ ] Erstelle monatliche Reports
- [ ] Setze Budget-Limits
- [ ] Vergleiche Preise zwischen Geschäften
- [ ] Exportiere Daten nach Excel

## 📚 Weitere Ressourcen

- `README.md` - Vollständige Dokumentation
- `receipt_analyzer.py` - Hauptcode mit Kommentaren
- `web_app.py` - Web-Interface Code

---

**Viel Erfolg! 🎉**

Bei Fragen oder Problemen erstelle ein Issue auf GitHub.
