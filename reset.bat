@echo off
REM reset.bat – Kompletter Reset des Kassenbon-Analyzers
REM Löscht: Datenbank, Ablage-PDFs, Fehler-PDFs
REM Behält: Programmdateien, Templates, Eingangsordner PDF

cd /d "%~dp0"

color 0C
echo.
echo ========================================================================
echo   ACHTUNG: VOLLSTAENDIGER RESET
echo ========================================================================
echo.
echo   Dieses Skript loescht ALLE gespeicherten Daten:
echo.
echo   - receipts.db           (komplette Datenbank)
echo   - Ablage\               (alle archivierten PDFs)
echo   - Fehler\               (alle fehlerhaften PDFs)
echo.
echo   Der Eingangsordner PDF\ bleibt erhalten.
echo   Alle Programmdateien bleiben erhalten.
echo.
echo ========================================================================
echo.

set /p confirm1="Bist du dir SICHER dass du alles loeschen willst? (JA/nein): "
if /i not "%confirm1%"=="JA" (
    echo.
    echo Abgebrochen.
    pause
    exit /b
)

echo.
set /p confirm2="LETZTE WARNUNG - Wirklich ALLE Daten loeschen? (JA LOESCHEN/nein): "
if /i not "%confirm2%"=="JA LOESCHEN" (
    echo.
    echo Abgebrochen.
    pause
    exit /b
)

echo.
echo ========================================================================
echo   Loesche Daten...
echo ========================================================================
echo.

REM Datenbank löschen
if exist "receipts.db" (
    del /q "receipts.db"
    echo   receipts.db geloescht
) else (
    echo   receipts.db nicht vorhanden
)

REM Ablage-Ordner löschen
if exist "Ablage\" (
    rd /s /q "Ablage"
    echo   Ablage\ geloescht
) else (
    echo   Ablage\ nicht vorhanden
)

REM Fehler-Ordner löschen
if exist "Fehler\" (
    rd /s /q "Fehler"
    echo   Fehler\ geloescht
) else (
    echo   Fehler\ nicht vorhanden
)

echo.
echo ========================================================================
echo   Reset abgeschlossen!
echo ========================================================================
echo.
echo   Das System ist jetzt leer und bereit fuer einen Neustart.
echo   Lege neue PDFs in PDF\ ab und starte den Server.
echo.
echo ========================================================================

pause
