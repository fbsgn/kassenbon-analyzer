@echo off
REM ═══════════════════════════════════════════════════════════
REM BACKUP WIEDERHERSTELLEN
REM ═══════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════
echo  BACKUP WIEDERHERSTELLEN
echo ═══════════════════════════════════════════════════════════
echo.
echo ⚠️  WARNUNG: Dies überschreibt die aktuellen Dateien!
echo.
echo Verfügbare Backups:
echo ─────────────────────────────────────────────────────────
dir /b /ad Backups\backup_*
echo ─────────────────────────────────────────────────────────
echo.
set /p BACKUP_NAME="Backup-Name eingeben (z.B. backup_20260208_105754): "

if not exist "Backups\%BACKUP_NAME%" (
    echo.
    echo ❌ Backup nicht gefunden: Backups\%BACKUP_NAME%
    echo.
    pause
    exit /b 1
)

echo.
echo 📦 Wiederherstelle aus: Backups\%BACKUP_NAME%
echo.
echo ⚠️  LETZTE WARNUNG: Aktuelle Dateien werden überschrieben!
echo.
set /p CONFIRM="Fortfahren? (j/n): "

if /i not "%CONFIRM%"=="j" (
    echo.
    echo ❌ Abgebrochen
    pause
    exit /b 0
)

echo.
echo 🔄 Stelle Dateien wieder her...
echo.

REM Dateien wiederherstellen
copy "Backups\%BACKUP_NAME%\web_app.py" . >nul 2>&1 && echo   ✅ web_app.py || echo   ⚠️  web_app.py
copy "Backups\%BACKUP_NAME%\web_app_v2.py" . >nul 2>&1 && echo   ✅ web_app_v2.py || echo   ⚠️  web_app_v2.py
copy "Backups\%BACKUP_NAME%\migrate_db.py" . >nul 2>&1 && echo   ✅ migrate_db.py || echo   ⚠️  migrate_db.py
copy "Backups\%BACKUP_NAME%\receipts.db" . >nul 2>&1 && echo   ✅ receipts.db || echo   ⚠️  receipts.db
copy "Backups\%BACKUP_NAME%\batch_import.py" . >nul 2>&1 && echo   ✅ batch_import.py || echo   ⚠️  batch_import.py
copy "Backups\%BACKUP_NAME%\receipt_analyzer.py" . >nul 2>&1 && echo   ✅ receipt_analyzer.py || echo   ⚠️  receipt_analyzer.py
copy "Backups\%BACKUP_NAME%\categories.json" . >nul 2>&1 && echo   ✅ categories.json || echo   ⚠️  categories.json
copy "Backups\%BACKUP_NAME%\templates\index.html" templates\ >nul 2>&1 && echo   ✅ templates\index.html || echo   ⚠️  templates\index.html

echo.
echo ═══════════════════════════════════════════════════════════
echo  ✅ WIEDERHERSTELLUNG ABGESCHLOSSEN!
echo ═══════════════════════════════════════════════════════════
echo.
echo 💡 NÄCHSTE SCHRITTE:
echo    1. Server neu starten: python web_app.py
echo    2. Testen ob alles funktioniert
echo.
pause
