# 🧾 Kassenbon-Analyzer für Windows 11

## 🪟 Windows-spezifische Installation

### Voraussetzungen

**Python installieren:**

1. Gehe zu: https://www.python.org/downloads/
2. Lade die neueste Python-Version herunter (3.8 oder höher)
3. **WICHTIG**: Aktiviere bei der Installation "Add Python to PATH"!
4. Klicke auf "Install Now"

![Python Installation](https://i.imgur.com/9YKvZlQ.png)

### Schritt-für-Schritt Installation

#### Methode 1: Automatisch (Empfohlen) ✨

1. **Doppelklick auf `install.bat`**
2. Das Script installiert automatisch alle Abhängigkeiten
3. Fertig! 🎉

#### Methode 2: Manuell

Öffne **PowerShell** oder **CMD** und führe aus:

```cmd
cd C:\Pfad\zum\kassenbon-analyzer
python -m pip install PyPDF2 Flask
```

## 🚀 Verwendung auf Windows

### Option 1: Web-Interface (Empfohlen)

**Doppelklick auf `start_web.bat`**

- Browser öffnet sich automatisch auf `http://localhost:5000`
- Kassenbons per Drag & Drop hochladen
- Statistiken in Echtzeit sehen

### Option 2: Demo ausführen

**Doppelklick auf `start_demo.bat`**

- Zeigt Beispiel-Analysen
- Keine eigenen PDFs nötig

### Option 3: Kommandozeile

Öffne **PowerShell** oder **CMD**:

```cmd
cd C:\Pfad\zum\kassenbon-analyzer
python receipt_analyzer.py C:\Users\DeinName\Documents\Kassenbons
```

## 📁 Empfohlene Ordnerstruktur (Windows)

```
C:\Users\DeinName\Documents\
└── Kassenbons\
    ├── 2026\
    │   ├── 01-Januar\
    │   │   ├── EDEKA_2026-01-08.pdf
    │   │   └── Rewe_2026-01-15.pdf
    │   └── 02-Februar\
    └── 2025\
```

Dann ausführen:
```cmd
python receipt_analyzer.py C:\Users\DeinName\Documents\Kassenbons\2026\01-Januar
```

## 🎯 Windows-spezifische Tipps

### PDF-Scanner Apps für Windows 11

- **Microsoft Lens** (kostenlos im Microsoft Store)
- **Adobe Scan** (kostenlos)
- **CamScanner**

Diese Apps können Kassenbons mit dem Handy scannen und als PDF auf deinen PC übertragen.

### Automatisierung mit Windows Task Scheduler

1. Öffne **Task Scheduler** (Aufgabenplanung)
2. Erstelle neue Aufgabe
3. Trigger: Täglich, z.B. jeden Abend um 22:00 Uhr
4. Aktion: Python-Script ausführen
   ```
   Programm: C:\Users\DeinName\AppData\Local\Programs\Python\Python311\python.exe
   Argumente: receipt_analyzer.py C:\Users\DeinName\Documents\Kassenbons
   ```

### Integration mit OneDrive/Google Drive

Speichere deine Kassenbons in:
```
C:\Users\DeinName\OneDrive\Kassenbons\
```

So sind sie automatisch in der Cloud gesichert!

## 🔧 Windows-Problemlösungen

### "Python ist kein interner oder externer Befehl"

**Lösung:**
1. Python neu installieren
2. "Add Python to PATH" aktivieren
3. ODER manuell PATH setzen:
   - Systemsteuerung → System → Erweiterte Systemeinstellungen
   - Umgebungsvariablen → Path → Bearbeiten
   - Hinzufügen: `C:\Users\DeinName\AppData\Local\Programs\Python\Python311\`

### Firewall-Warnung beim Start

**Das ist normal!** 
- Flask öffnet Port 5000 für das Web-Interface
- Klicke auf "Zugriff zulassen" (nur privates Netzwerk nötig)

### "Zugriff verweigert" beim Installieren

**Lösung:**
```cmd
python -m pip install --user PyPDF2 Flask
```

### Umlaute werden nicht korrekt angezeigt

Windows CMD hat manchmal Probleme mit UTF-8. Lösung:

```cmd
chcp 65001
python receipt_demo.py
```

Oder benutze **Windows Terminal** (empfohlen, kostenlos im Microsoft Store)

## 📊 Performance-Tipps für Windows

### Große PDF-Sammlungen

Bei vielen PDFs (100+):
```cmd
REM Nur neue PDFs verarbeiten
python receipt_analyzer.py C:\Kassenbons --incremental
```

### Windows Defender Ausnahme

Für schnellere Verarbeitung:
1. Windows-Sicherheit öffnen
2. Viren- & Bedrohungsschutz
3. Einstellungen verwalten
4. Ausschlüsse hinzufügen
5. Ordner: `kassenbon-analyzer` Verzeichnis hinzufügen

## 🎨 Windows Terminal Customization

Für eine bessere Darstellung empfehle ich **Windows Terminal**:

1. Im Microsoft Store herunterladen
2. Schöne Farbschemata
3. Bessere Unicode-Unterstützung (für Emojis in der Ausgabe)

## 📱 Mobile Integration (Windows 11)

### Option 1: Phone Link (Ihr Smartphone)
1. App "Ihr Smartphone" öffnen
2. Handy verbinden
3. Fotos von Kassenbons direkt übertragen

### Option 2: OneDrive Mobile App
1. OneDrive App auf dem Handy
2. Kassenbon fotografieren
3. Zu OneDrive-Ordner hochladen
4. Automatisch auf PC verfügbar

## 🔐 Datenschutz

Alle Daten bleiben **lokal auf deinem PC**!
- Keine Cloud-Uploads
- Keine Tracking
- SQLite-Datenbank in: `receipts.db`

## 🎁 Bonus: Desktop-Verknüpfung erstellen

1. Rechtsklick auf Desktop → Neu → Verknüpfung
2. Pfad eingeben:
   ```
   C:\Windows\System32\cmd.exe /c "cd /d C:\Pfad\zum\kassenbon-analyzer && start_web.bat"
   ```
3. Name: "Kassenbon-Analyzer"
4. Icon ändern (optional)

Jetzt kannst du die App vom Desktop starten! 🎉

## 📞 Support für Windows-User

### Hilfreiche Kommandos

```cmd
REM Python-Version prüfen
python --version

REM Installierte Pakete anzeigen
pip list

REM Datenbank zurücksetzen
del receipts.db

REM Cache leeren
rmdir /s /q __pycache__
```

### Log-Dateien

Bei Problemen, erstelle ein Log:
```cmd
python receipt_demo.py > log.txt 2>&1
```

Dann `log.txt` zur Fehleranalyse öffnen.

## 🚀 Nächste Schritte

- [ ] Installiere Python (falls noch nicht vorhanden)
- [ ] Führe `install.bat` aus
- [ ] Teste mit `start_demo.bat`
- [ ] Starte Web-Interface mit `start_web.bat`
- [ ] Lade deine ersten Kassenbons hoch!

---

## 💡 Windows 11 Features nutzen

### Snap Layouts
- Web-Interface auf der einen Seite
- Datei-Explorer mit PDFs auf der anderen Seite
- Einfaches Drag & Drop!

### Widgets
Zukünftig geplant: Dashboard-Widget für Windows 11 Widgets-Panel

---

**Viel Erfolg auf Windows 11! 🪟🎉**

Bei Fragen oder Problemen, schau in die `README.md` oder erstelle ein Issue.
