@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo  KASSENBON-ANALYZER STARTER
echo ========================================
echo.
echo Verzeichnis: %CD%
echo.
echo --- Datei-Kontrolle ---

if exist "web_app.py" (
    for %%A in (web_app.py) do (
        echo web_app.py  : %%~zA bytes  %%~tA
    )
) else (
    echo web_app.py  : NICHT GEFUNDEN!
)

if exist "batch_import.py" (
    for %%A in (batch_import.py) do (
        echo batch_import.py   : %%~zA bytes  %%~tA
    )
) else (
    echo batch_import.py   : NICHT GEFUNDEN!
)

if exist "receipt_analyzer.py" (
    for %%A in (receipt_analyzer.py) do (
        echo receipt_analyzer.py: %%~zA bytes  %%~tA
    )
) else (
    echo receipt_analyzer.py: NICHT GEFUNDEN!
)

if exist "templates\index.html" (
    for %%A in (templates\index.html) do (
        echo index.html        : %%~zA bytes  %%~tA
    )
) else (
    echo index.html        : NICHT GEFUNDEN!
)

if not exist "PDF" mkdir PDF

echo.
echo Erwartete Groesse web_app_fixed.py: ca. 18.300 bytes
echo Falls deutlich kleiner = alte Version, neue kopieren!
echo ========================================
echo.

python web_app.py

pause
