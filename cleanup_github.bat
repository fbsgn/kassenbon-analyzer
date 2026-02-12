@echo off
setlocal enableextensions enabledelayedexpansion

echo =========================================================
echo   CLEANUP - VORBEREITUNG FUER GITHUB
echo =========================================================
echo.
echo Dieses Script loescht alle Debug-, Test- und Temp-Dateien
echo die nicht fuer GitHub benoetigt werden.
echo.
echo WARNUNG: Dieser Vorgang kann NICHT rueckgaengig gemacht werden!
echo.
pause

echo.
echo [1/5] Loesche Debug-Skripte...
del /Q debug_categories.py 2>nul
del /Q debug_templates.py 2>nul
del /Q emergency_fix.py 2>nul
del /Q FINAL_FIX.py 2>nul
del /Q fix_category_save.bat 2>nul
del /Q fix_keywords.py 2>nul
del /Q diagnose.bat 2>nul
del /Q ultimate_fix.bat 2>nul
del /Q FIX_ANLEITUNG.txt 2>nul
echo    OK - Debug-Skripte geloescht

echo.
echo [2/5] Loesche alte Versionen...
del /Q categories.old 2>nul
del /Q categories.json.backup 2>nul
del /Q receipt_analyzer.old 2>nul
del /Q web_app_backup.py 2>nul
del /Q index.html 2>nul
echo    OK - Alte Versionen geloescht

echo.
echo [3/5] Loesche Patch-Dokumentation...
del /Q BROWSER_CACHE_FIX.md 2>nul
del /Q CSS_PATCH_PDF_VIEWER.css 2>nul
del /Q FEATURE_DROPDOWNS.md 2>nul
del /Q FILTER_FIX.md 2>nul
del /Q PDF_VIEWER_UPDATE.md 2>nul
del /Q THREADING_FIX.md 2>nul
del /Q UPDATE_KLASSIFIZIERUNG.md 2>nul
del /Q VERBESSERUNGEN_V2.md 2>nul
del /Q README_PATCHES.txt 2>nul
echo    OK - Patch-Dokumentation geloescht

echo.
echo [4/5] Loesche veraltete Install-Skripte...
del /Q install_category_settings.bat 2>nul
del /Q install_pwa.bat 2>nul
del /Q update_backend.py 2>nul
del /Q update_frontend.py 2>nul
del /Q update_pwa.py 2>nul
del /Q update_pwa_backend.py 2>nul
echo    OK - Install-Skripte geloescht

echo.
echo [5/5] Loesche Demo/Test-Dateien...
del /Q receipt_demo.py 2>nul
del /Q start_demo.bat 2>nul
del /Q test_classification.py 2>nul
del /Q test_filter.html 2>nul
del /Q edeka.xlsx 2>nul
echo    OK - Demo/Test-Dateien geloescht

echo.
echo [6/5] Loesche doppelte Offline-Version...
if exist "kassenbon_analyzer_offline" (
    rmdir /S /Q kassenbon_analyzer_offline
    echo    OK - kassenbon_analyzer_offline geloescht
) else (
    echo    SKIP - kassenbon_analyzer_offline existiert nicht
)

echo.
echo [7/5] Loesche Cache-Ordner...
if exist ".vs" rmdir /S /Q .vs
if exist "__pycache__" rmdir /S /Q __pycache__
echo    OK - Cache geloescht

echo.
echo [8/5] Loesche diese Cleanup-Dateien...
del /Q CLEANUP_LISTE.txt 2>nul
echo    OK - Cleanup-Liste geloescht

echo.
echo =========================================================
echo   CLEANUP ABGESCHLOSSEN!
echo =========================================================
echo.
echo Naechste Schritte:
echo   1. Pruefe ob alles OK ist
echo   2. Erstelle .gitignore (siehe .gitignore Datei)
echo   3. GitHub Repository erstellen
echo.
echo Dieses Script loescht sich NICHT selbst.
echo Loesche cleanup_github.bat manuell wenn gewuenscht.
echo.
pause
