#!/bin/bash
#
# Installations-Script für Kassenbon-Analyzer
#

echo "🧾 Kassenbon-Analyzer Installation"
echo "===================================="
echo ""

# Prüfe Python-Version
echo "Prüfe Python-Installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert!"
    echo "Bitte installiere Python 3.8 oder höher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION gefunden"

# Erstelle virtuelle Umgebung (optional)
read -p "Möchtest du eine virtuelle Umgebung erstellen? (empfohlen) [j/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Jj]$ ]]; then
    echo "Erstelle virtuelle Umgebung..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtuelle Umgebung aktiviert"
fi

# Installiere Abhängigkeiten
echo ""
echo "Installiere Python-Pakete..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Alle Pakete erfolgreich installiert"
else
    echo "❌ Fehler bei der Installation der Pakete"
    exit 1
fi

# Erstelle notwendige Verzeichnisse
echo ""
echo "Erstelle Verzeichnisse..."
mkdir -p uploads
mkdir -p static
echo "✓ Verzeichnisse erstellt"

# Test
echo ""
echo "Teste Installation..."
python3 -c "import PyPDF2; import flask; print('✓ Alle Module verfügbar')"

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ Installation erfolgreich!"
    echo "======================================"
    echo ""
    echo "Nächste Schritte:"
    echo ""
    echo "1. Demo ausführen:"
    echo "   python3 receipt_demo.py"
    echo ""
    echo "2. Web-Interface starten:"
    echo "   python3 web_app.py"
    echo "   Dann Browser öffnen: http://localhost:5000"
    echo ""
    echo "3. Kommandozeilen-Version:"
    echo "   python3 receipt_analyzer.py /pfad/zu/pdfs/"
    echo ""
else
    echo "❌ Test fehlgeschlagen"
    exit 1
fi
