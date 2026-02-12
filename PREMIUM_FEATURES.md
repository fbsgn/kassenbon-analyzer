# 🚀 Neue Premium-Features - Vollversion

## ✨ Was ist neu?

Du hast jetzt **4 mächtige neue Features**:

1. **🔍 Filter nach Geschäft & Zeitraum**
2. **📊 Preisverlaufs-Diagramme**
3. **📥 Excel-Export**
4. **📈 Erweiterte Statistiken**

---

## 1. 🔍 Filter-Funktion

### Was kann ich filtern?

**Geschäft** 🏪
- Zeige nur Einkäufe von einem bestimmten Geschäft
- z.B. nur EDEKA oder nur FFFrische-Center

**Zeitraum** 📅
- Von-Datum: Startdatum
- Bis-Datum: Enddatum
- z.B. "Nur Januar 2026"

### Wie funktioniert es?

```
1. Wähle Geschäft aus Dropdown
2. Setze Datums-Bereich
3. Klicke "Filter anwenden"
4. ✅ Alle Daten werden gefiltert!
```

### Was wird gefiltert?

✅ **Kategorien-Statistiken**
✅ **Kategorie-Details**
✅ **Gesamtausgaben**
✅ **Excel-Export**

### Beispiel-Szenarien:

#### Szenario 1: Geschäftsvergleich
```
Frage: "Bei welchem Geschäft gebe ich mehr aus?"

Lösung:
1. Filter: EDEKA → Notiere Gesamtausgaben
2. Filter: FFFrische-Center → Vergleiche
3. Ergebnis: Klarer Vergleich!
```

#### Szenario 2: Monatsanalyse
```
Frage: "Wie viel habe ich im Januar ausgegeben?"

Lösung:
1. Von: 01.01.2026
2. Bis: 31.01.2026
3. Filter anwenden
4. Ergebnis: Monatsausgaben sichtbar
```

#### Szenario 3: Kombiniert
```
Frage: "Was habe ich bei EDEKA im Januar gekauft?"

Lösung:
1. Geschäft: EDEKA
2. Zeitraum: Januar 2026
3. Klicke auf Kategorien für Details
4. Ergebnis: Detaillierte Auflistung!
```

---

## 2. 📊 Preisverlaufs-Diagramme

### Wann sehe ich das Chart-Icon?

Das **📈-Icon** erscheint bei Artikeln die **mindestens 2x** gekauft wurden.

### Wie öffne ich ein Diagramm?

```
1. Klicke auf Kategorie (z.B. "Obst & Gemüse")
2. Details öffnen sich
3. Klicke auf 📈 neben Artikelname
4. Modal mit Diagramm öffnet sich!
```

### Was zeigt das Diagramm?

**Haupt-Chart:**
- X-Achse: Kaufdatum
- Y-Achse: Preis in €
- Linie: Preisentwicklung
- Punkte: Einzelne Käufe (hover für Details)

**Statistik-Boxen:**

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Minimum    │ Durchschnitt│  Maximum    │    Trend    │
│   1.11 €    │   1.31 €    │   1.50 €    │  📈 +15%   │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

- **Minimum**: Günstigster Preis
- **Durchschnitt**: Ø über alle Käufe
- **Maximum**: Teuerster Preis
- **Trend**: Änderung vom ersten zum letzten Kauf

### Beispiel-Interpretation:

```
MOEHREN - Preisverlauf

Chart zeigt:
08.01.26: 1.50 € (FFFrische-Center)
15.01.26: 1.11 € (EDEKA) ← GÜNSTIG!
26.01.26: 1.35 € (FFFrische-Center)
31.01.26: 1.50 € (EDEKA)

Statistiken:
Min: 1.11 € | Ø: 1.37 € | Max: 1.50 € | Trend: 📈 +7%

Erkenntnis:
💡 Am 15.01. gab es ein Angebot!
💡 Preis schwankt um 0.39 € (35%)
💡 Lohnt sich auf Angebote zu warten
```

### Features:

✅ **Interaktiv**: Hover über Punkte für Details
✅ **Übersichtlich**: Klare Zeitachse
✅ **Statistiken**: Min/Max/Durchschnitt/Trend
✅ **Geschäfts-Info**: Sieh wo es günstiger war
✅ **Responsive**: Funktioniert auf allen Geräten

---

## 3. 📥 Excel-Export

### Was wird exportiert?

Alle deine Kassenbons als **CSV-Datei** (öffenbar in Excel, Google Sheets, etc.)

### Spalten im Export:

| Spalte | Beschreibung | Beispiel |
|--------|--------------|----------|
| Datum | Kaufdatum | 26.01.2026 |
| Geschäft | Ladenname | FFFrische-Center |
| Artikel | Produktname | MOEHREN |
| Kategorie | Artikel-Kategorie | Obst & Gemüse |
| Einzelpreis | Preis pro Stück | 1,11 |
| Menge | Anzahl | 1 |
| Gesamtpreis | Einzelpreis × Menge | 1,11 |
| Kassenbon-Summe | Total des Bons | 42,01 |
| Zahlungsmethode | Wie bezahlt | Mastercard |

### Wie exportiere ich?

```
1. (Optional) Setze Filter
2. Klicke "📥 Als Excel exportieren"
3. Datei wird heruntergeladen
4. Öffne in Excel/LibreOffice/Google Sheets
```

### Export berücksichtigt Filter!

**Wichtig:** Der Export enthält **nur gefilterte Daten**!

```
Beispiel 1: Ohne Filter
→ Export: ALLE Kassenbons

Beispiel 2: Filter EDEKA + Januar
→ Export: NUR EDEKA-Käufe aus Januar
```

### Use Cases:

#### Steuer / Buchhaltung:
```
1. Filter: Geschäftsjahr 2026
2. Export
3. An Steuerberater senden
```

#### Budgetanalyse:
```
1. Export alle Daten
2. Öffne in Excel
3. Erstelle Pivot-Tabellen
4. Analysiere Ausgabenmuster
```

#### Geschäftsvergleich:
```
1. Export EDEKA
2. Export Rewe
3. Vergleiche in Excel
4. Finde günstigstes Geschäft
```

#### Backup:
```
1. Export ohne Filter (alle Daten)
2. Speichere Datei
3. Backup erstellt!
```

---

## 4. 📈 Erweiterte Statistiken

### Kategorien mit Live-Filter

Die Kategorie-Ansicht zeigt jetzt:

✅ **Gefilterte Summen**: Nur ausgewählter Zeitraum/Geschäft
✅ **Dropdown-Details**: Klick auf Kategorie für Liste
✅ **Artikel-Statistiken**: Häufigkeit, Preisspanne
✅ **Chart-Icons**: Bei mehrfach gekauften Artikeln

### Beispiel-Workflow:

```
Ziel: "Wo spare ich am meisten bei Getränken?"

Schritte:
1. Filter: EDEKA
2. Klicke "Getränke"
3. Notiere: 25.50 €
4. Filter: FFFrische-Center  
5. Klicke "Getränke"
6. Notiere: 28.90 €

Ergebnis: Bei EDEKA 3.40 € günstiger! 💰
```

---

## 🎯 Praktische Anwendungen

### 1. Preisvergleich zwischen Geschäften

```
Workflow:
┌─────────────────────────────────────────┐
│ 1. Filter: EDEKA                        │
│ 2. Notiere Ausgaben pro Kategorie       │
│ 3. Filter: Rewe                         │
│ 4. Vergleiche Kategorien                │
│ 5. Entscheide: Wo lohnt sich was?       │
└─────────────────────────────────────────┘

Beispiel-Ergebnis:
- Getränke: EDEKA günstiger (-15%)
- Obst: Rewe günstiger (-8%)
- Fleisch: Gleich
```

### 2. Monatliches Budget tracken

```
Workflow:
┌─────────────────────────────────────────┐
│ 1. Filter: Aktueller Monat              │
│ 2. Sieh Gesamtausgaben                  │
│ 3. Vergleiche mit Budget                │
│ 4. Export für Aufzeichnung              │
└─────────────────────────────────────────┘

Budget: 300 €/Monat
Aktuell: 245 € (18 Tage)
Hochrechnung: 408 € → ⚠️ Über Budget!
```

### 3. Spar-Potenzial identifizieren

```
Workflow:
┌─────────────────────────────────────────┐
│ 1. Klicke Kategorie                     │
│ 2. Finde Artikel mit Preis-Schwankung   │
│ 3. Klicke 📈 für Diagramm               │
│ 4. Identifiziere günstigste Zeiten      │
│ 5. Kaufe strategisch!                   │
└─────────────────────────────────────────┘

Beispiel:
BALLENSALAT: 1,00 - 1,99 €
→ Warte auf 1,00 € Preis
→ Spare 0,99 € pro Stück!
```

### 4. Jahresauswertung

```
Workflow:
┌─────────────────────────────────────────┐
│ 1. Filter: 01.01.2026 - 31.12.2026     │
│ 2. Export als Excel                     │
│ 3. Öffne in Excel                       │
│ 4. Pivot-Tabelle erstellen              │
│ 5. Jahres-Report fertig!                │
└─────────────────────────────────────────┘
```

---

## 💡 Pro-Tipps

### Tipp 1: Wochen-Vergleich
```
Vergleiche einzelne Wochen:
- KW 1: 65 €
- KW 2: 82 €
- KW 3: 71 €
→ KW 2 war teuer, warum? → Details prüfen
```

### Tipp 2: Geschäfts-Rotation
```
Kaufe gezielt:
- Getränke: EDEKA (günstiger)
- Obst: Rewe (frischer + günstiger)
- Fleisch: FFFrische (Qualität)
```

### Tipp 3: Angebots-Tracking
```
Nutze Preisverlauf:
1. Öffne Chart für häufig gekauften Artikel
2. Notiere Mindest-Preis
3. Warte auf diesen Preis
4. Kaufe dann größere Menge
```

### Tipp 4: Export-Backup
```
Jeden Monat:
1. Export ohne Filter
2. Speichere: "Kassenbons_2026-01.csv"
3. Backup auf Cloud
4. Immer Zugriff auf Historie!
```

---

## 🔧 Technische Details

### API-Endpunkte:

```
GET /api/stores
→ Liste aller Geschäfte

GET /api/date-range  
→ Min/Max Datum der Daten

GET /api/category-details/<category>?store=X&date_from=Y&date_to=Z
→ Gefilterte Artikel einer Kategorie

GET /api/item-price-history/<item>
→ Preisverlauf für Chart

GET /api/export/excel?store=X&date_from=Y&date_to=Z
→ CSV-Download (gefiltert)
```

### Chart-Bibliothek:

**Chart.js 4.4.0**
- Responsive
- Touch-freundlich
- Moderne Optik
- Interaktive Tooltips

### Export-Format:

**CSV mit Semikolon** (`;`)
- Standard für deutsche Excel-Versionen
- UTF-8 Encoding
- Komma als Dezimaltrennzeichen
- Öffenbar in allen Spreadsheet-Apps

---

## ✅ Feature-Checkliste

Nach dem Update sollten folgende Features funktionieren:

- [ ] Geschäfts-Filter wird geladen
- [ ] Datums-Filter setzt Min/Max automatisch
- [ ] Filter anwenden aktualisiert Kategorien
- [ ] Dropdown zeigt gefilterte Artikel
- [ ] 📈-Icon erscheint bei Mehrfachkäufen
- [ ] Chart öffnet sich und zeigt Verlauf
- [ ] Statistiken (Min/Max/Ø/Trend) werden angezeigt
- [ ] Export-Button lädt CSV herunter
- [ ] CSV öffnet in Excel korrekt
- [ ] Filter beeinflussen Export

---

## 🎓 Video-Tutorial (Konzept)

### Teil 1: Filter (2 Min)
```
1. Zeige Filter-Bereich
2. Wähle Geschäft aus
3. Setze Datum
4. Demonstriere Änderungen
```

### Teil 2: Charts (3 Min)
```
1. Öffne Kategorie-Details
2. Klicke Chart-Icon
3. Erkläre Statistiken
4. Zeige Interpretation
```

### Teil 3: Export (2 Min)
```
1. Setze Filter
2. Klicke Export
3. Öffne in Excel
4. Zeige Möglichkeiten
```

---

**Viel Erfolg mit den neuen Features! 🚀📊💰**

Bei Fragen: Siehe `TROUBLESHOOTING.md`
