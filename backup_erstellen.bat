@echo off
REM ═══════════════════════════════════════════════════════════
REM KASSENBON-ANALYZER - BACKUP-SCRIPT
REM ═══════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════
echo  BACKUP WIRD ERSTELLT...
echo ═══════════════════════════════════════════════════════════
echo.

REM Timestamp generieren
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,4%%datetime:~4,2%%datetime:~6,2%_%datetime:~8,2%%datetime:~10,2%%datetime:~12,2%

REM Backup-Ordner erstellen
set BACKUP_DIR=Backups\backup_%TIMESTAMP%
mkdir "%BACKUP_DIR%" 2>nul
mkdir "%BACKUP_DIR%\templates" 2>nul

echo 📦 Backup-Ordner: %BACKUP_DIR%
echo.

REM Dateien sichern
echo 📄 Sichere Hauptdateien...
copy web_app.py "%BACKUP_DIR%\" >nul 2>&1 && echo   ✅ web_app.py || echo   ⚠️  web_app.py nicht gefunden
copy web_app_v2.py "%BACKUP_DIR%\" >nul 2>&1 && echo   ✅ web_app_v2.py || echo   ⚠️  web_app_v2.py nicht gefunden
copy migrate_db.py "%BACKUP_DIR%\" >nul 2>&1 && echo   ✅ migrate_db.py || echo   ⚠️  migrate_db.py nicht gefunden
copy receipts.db "%BACKUP_DIR%\" >nul 2>&1 && echo   ✅ receipts.db || echo   ⚠️  receipts.db nicht gefunden
copy batch_import.py "%BACKUP_DIR%\" >nul 2>&1 && echo   ✅ batch_import.py || echo   ⚠️  batch_import.py nicht gefunden
copy receipt_analyzer.py "%BACKUP_DIR%\" >nul 2>&1 && echo   ✅ receipt_analyzer.py || echo   ⚠️  receipt_analyzer.py nicht gefunden
copy categories.json "%BACKUP_DIR%\" >nul 2>&1 && echo   ✅ categories.json || echo   ⚠️  categories.json nicht gefunden
copy VERBESSERUNGEN_V2.md "%BACKUP_DIR%\" >nul 2>&1 && echo   ✅ VERBESSERUNGEN_V2.md || echo   ⚠️  VERBESSERUNGEN_V2.md nicht gefunden

echo.
echo 📄 Sichere Templates...
copy templates\index.html "%BACKUP_DIR%\templates\" >nul 2>&1 && echo   ✅ templates\index.html || echo   ⚠️  templates\index.html nicht gefunden

echo.
echo 📝 Erstelle Backup-Info...

REM Erstelle README
(
echo ═══════════════════════════════════════════════════════════
echo BACKUP VOM %date% %time%
echo ═══════════════════════════════════════════════════════════
echo.
echo 📦 BACKUP-INHALT:
echo ─────────────────────────────────────────────────────────
echo   • web_app.py          - Original Web-App
echo   • web_app_v2.py        - Verbesserte Web-App
echo   • migrate_db.py        - Migrations-Skript
echo   • receipts.db          - Datenbank
echo   • batch_import.py      - Batch-Import
echo   • receipt_analyzer.py  - PDF-Parser
echo   • categories.json      - Kategorien
echo   • templates\index.html - Frontend mit PDF-Modal-Fix
echo   • VERBESSERUNGEN_V2.md - Dokumentation
echo.
echo 🔄 WIEDERHERSTELLUNG:
echo ─────────────────────────────────────────────────────────
echo 1. Server stoppen ^(Strg+C^)
echo 2. Gewünschte Dateien nach C:\Kassenbons\ kopieren
echo 3. Server neu starten: python web_app.py
echo.
echo 📌 VERSIONEN:
echo ─────────────────────────────────────────────────────────
echo   web_app.py   - Stabile Version mit PDF-Modal-Fix
echo   web_app_v2.py - Neue Version mit Verbesserungen:
echo                   ✅ PDF-Zuordnung via DB
echo                   ✅ Strukturiertes Error-Handling
echo                   ✅ Duplikat-Erkennung
echo                   ✅ Logging
echo.
echo 💡 EMPFEHLUNG:
echo ─────────────────────────────────────────────────────────
echo Bei Problemen: Einfach alle Dateien aus diesem Backup
echo zurück nach C:\Kassenbons\ kopieren.
echo.
echo ═══════════════════════════════════════════════════════════
) > "%BACKUP_DIR%\README.txt"

echo   ✅ README.txt erstellt

echo.
echo ═══════════════════════════════════════════════════════════
echo  ✅ BACKUP FERTIG!
echo ═══════════════════════════════════════════════════════════
echo.
echo 📁 Backup-Ordner: %BACKUP_DIR%
echo.
echo 💡 NÄCHSTE SCHRITTE:
echo    1. Siehe README.txt im Backup-Ordner
echo    2. Backup-Ordner ist sicher aufbewahrt
echo    3. Bei Bedarf: Dateien zurückkopieren
echo.
pause
