@echo off
setlocal enableextensions enabledelayedexpansion

echo ===========================================
echo   KASSENBON-ANALYZER OFFLINE STARTER
echo ===========================================
echo.

REM Pruefe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python nicht gefunden!
    echo Bitte installiere Python 3.8+ von python.org
    pause
    exit /b 1
)

echo [INFO] Starte Server mit Auto-Backup...
echo.
python local_launch.py

if errorlevel 1 (
    echo.
    echo [ERROR] Server konnte nicht gestartet werden!
    pause
    exit /b 1
)

pause
