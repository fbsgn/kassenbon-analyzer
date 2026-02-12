#!/usr/bin/env python3
"""
Migration: Fügt pdf_path und pdf_hash Spalten zur Datenbank hinzu
"""

import sqlite3
from pathlib import Path

DB_PATH = 'receipts.db'

def migrate():
    """Führt die Migration durch"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🔧 Starte Migration...")
    
    # Prüfe ob Spalten bereits existieren
    cursor.execute("PRAGMA table_info(receipts)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'pdf_path' not in columns:
        print("  ➕ Füge Spalte 'pdf_path' hinzu...")
        cursor.execute('ALTER TABLE receipts ADD COLUMN pdf_path TEXT')
        print("  ✅ pdf_path hinzugefügt")
    else:
        print("  ⏭️  pdf_path existiert bereits")
    
    if 'pdf_hash' not in columns:
        print("  ➕ Füge Spalte 'pdf_hash' hinzu...")
        cursor.execute('ALTER TABLE receipts ADD COLUMN pdf_hash TEXT')
        print("  ✅ pdf_hash hinzugefügt")
    else:
        print("  ⏭️  pdf_hash existiert bereits")
    
    # Erstelle Index auf pdf_hash
    print("  🔍 Erstelle Index auf pdf_hash...")
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_receipts_pdf_hash ON receipts(pdf_hash)')
        print("  ✅ Index erstellt")
    except sqlite3.Error as e:
        print(f"  ⚠️  Index-Erstellung: {e}")
    
    conn.commit()
    conn.close()
    
    print("✅ Migration abgeschlossen!\n")
    print("📝 WICHTIG:")
    print("   - Alte Kassenbons haben kein pdf_path/pdf_hash (= NULL)")
    print("   - Neue Uploads werden korrekt gespeichert")
    print("   - PDF-Anzeige funktioniert NUR für neue Uploads")
    print("\n💡 Empfehlung: Batch-Re-Import der PDFs aus C:\\Kassenbons\\Ablage\\")

if __name__ == '__main__':
    if not Path(DB_PATH).exists():
        print(f"❌ Datenbank nicht gefunden: {DB_PATH}")
        print("   Bitte zuerst web_app.py starten!")
        exit(1)
    
    migrate()
