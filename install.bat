@echo off
REM Installations-Script für Kassenbon-Analyzer (Windows 11)

echo.
echo ========================================
echo   Kassenbon-Analyzer Installation
echo   Windows 11
echo ========================================
echo.

REM Prüfe Python-Installation
echo Pruefe Python-Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [FEHLER] Python ist nicht installiert!
    echo.
    echo Bitte installiere Python von:
    echo https://www.python.org/downloads/
    echo.
    echo WICHTIG: Aktiviere "Add Python to PATH" bei der Installation!
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% gefunden
echo.

REM Upgrade pip
echo Aktualisiere pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [WARNUNG] pip-Update fehlgeschlagen, fahre trotzdem fort...
)
echo.

REM Installiere Abhängigkeiten
echo Installiere Python-Pakete...
echo - PyPDF2
echo - Flask
echo.
python -m pip install PyPDF2 Flask

if errorlevel 1 (
    echo.
    echo [FEHLER] Installation der Pakete fehlgeschlagen!
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Alle Pakete erfolgreich installiert
echo.

REM Erstelle Verzeichnisse
echo Erstelle Verzeichnisse...
if not exist "uploads" mkdir uploads
if not exist "static" mkdir static
echo [OK] Verzeichnisse erstellt
echo.

REM Test
echo Teste Installation...
python -c "import PyPDF2; import flask; print('[OK] Alle Module verfuegbar')"

if errorlevel 1 (
    echo.
    echo [FEHLER] Test fehlgeschlagen!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation erfolgreich!
echo ========================================
echo.
echo Naechste Schritte:
echo.
echo 1. Demo ausfuehren:
echo    python receipt_demo.py
echo.
echo 2. Web-Interface starten:
echo    python web_app.py
echo    Dann Browser oeffnen: http://localhost:5000
echo.
echo 3. Kommandozeilen-Version:
echo    python receipt_analyzer.py C:\Pfad\zu\PDFs
echo.
echo ========================================
echo.
pause
