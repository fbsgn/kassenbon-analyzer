#!/bin/bash
# Installation für Kassenbon-Analyzer Offline

echo "========================================================="
echo "  KASSENBON-ANALYZER OFFLINE - INSTALLATION"
echo "========================================================="
echo

# Prüfe Python
echo "[1/3] Prüfe Python-Installation..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 nicht gefunden!"
    echo
    echo "Bitte installiere Python 3.8 oder neuer:"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  - macOS: brew install python3"
    echo
    exit 1
fi

python3 --version
echo "[OK] Python gefunden!"
echo

# Installiere Requirements
echo "[2/3] Installiere Python-Pakete..."
echo
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Installation fehlgeschlagen!"
    echo
    echo "Versuche alternativ:"
    echo "  python3 -m pip install --user -r requirements.txt"
    echo
    exit 1
fi

echo
echo "[OK] Alle Pakete installiert!"
echo

# Optionaler Chart.js Download
echo "[3/3] Chart.js für Preisdiagramme (optional)"
echo
read -p "Chart.js jetzt herunterladen? (j/n): " download
if [ "$download" = "j" ] || [ "$download" = "J" ]; then
    echo
    python3 download_chartjs.py
fi

echo
echo "========================================================="
echo "  INSTALLATION ABGESCHLOSSEN!"
echo "========================================================="
echo
echo "Starte die App mit:"
echo "  ./start.sh"
echo
