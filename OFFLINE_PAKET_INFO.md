# Kassenbon-Analyzer - Offline-Paket Vollversion

## 📦 Was ist das?

Ein **selbstständiges, vollständig offline nutzbares Paket** des Kassenbon-Analyzers.

Perfekt für:
- ✅ Nutzung ohne Internetverbindung
- ✅ Maximale Datensicherheit (alles lokal)
- ✅ Weitergabe an andere Computer
- ✅ Portable Installation auf USB-Stick
- ✅ Automatische Backups

## 🚀 Schnellstart

**Windows:**
```cmd
cd kassenbon_analyzer_offline_full
INSTALL.bat    # Einmalig
START.bat      # App starten
```

**Linux/macOS:**
```bash
cd kassenbon_analyzer_offline_full
chmod +x install.sh start.sh
./install.sh   # Einmalig
./start.sh     # App starten
```

## ✨ Unterschiede zum Hauptprojekt

| Feature | Hauptprojekt | Offline-Paket |
|---------|--------------|---------------|
| Internet benötigt | Nur für Updates | ❌ Nie |
| Auto-Backup | ❌ | ✅ Bei jedem Start |
| Start-Komfort | Manuell | ✅ 1-Klick |
| Portabel | ❌ | ✅ Ja |
| Installation | Komplex | ✅ INSTALL.bat |

## 📁 Ordner-Übersicht

```
kassenbon_analyzer_offline_full/
├─ README_START_HIER.txt    ← LIES MICH ZUERST!
├─ INSTALL.bat              ← Installation (einmalig)
├─ START.bat                ← App starten
├─ requirements.txt         ← Python-Pakete
├─ download_chartjs.py      ← Chart.js Download-Helper
└─ ... (alle nötigen Dateien)
```

## 🎯 Empfohlene Nutzung

**Szenario 1: Normale Nutzung (mit Internet)**
- Nutze das **Hauptprojekt** (hier im Hauptordner)
- Bessere Performance
- Automatische Updates möglich

**Szenario 2: Ohne Internet / Maximale Sicherheit**
- Nutze das **Offline-Paket**
- Komplett autark
- Auto-Backups
- Ideal zum Weitergeben

## 💡 Tipp: Beide parallel nutzen

Du kannst BEIDE Versionen haben:
1. Hauptprojekt für tägliche Nutzung
2. Offline-Paket als Backup/Weitergabe-Version

Die Datenbanken sind getrennt!

## 📚 Vollständige Dokumentation

Siehe: `kassenbon_analyzer_offline_full/README_START_HIER.txt`

---

**Version:** Offline-Full 2.0  
**Erstellt:** Februar 2026
