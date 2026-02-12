@echo off
setlocal enableextensions enabledelayedexpansion

echo =========================================================
echo   KASSENBON-ANALYZER OFFLINE - INSTALLATION
echo =========================================================
echo.

REM Pruefe Python
echo [1/3] Pruefe Python-Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python nicht gefunden!
    echo.
    echo Bitte installiere Python 3.8 oder neuer von:
    echo https://www.python.org/downloads/
    echo.
    echo Waehle bei der Installation: "Add Python to PATH"
    pause
    exit /b 1
)

python --version
echo [OK] Python gefunden!
echo.

REM Installiere Requirements
echo [2/3] Installiere Python-Pakete...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Installation fehlgeschlagen!
    echo.
    echo Versuche alternativ:
    echo   pip install --user -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Alle Pakete installiert!
echo.

REM Optionaler Chart.js Download
echo [3/3] Chart.js fuer Preisdiagramme (optional)
echo.
set /p download="Chart.js jetzt herunterladen? (j/n): "
if /i "%download%"=="j" (
    echo.
    python download_chartjs.py
)

echo.
echo =========================================================
echo   INSTALLATION ABGESCHLOSSEN!
echo =========================================================
echo.
echo Starte die App mit:
echo   START.bat
echo.
pause
