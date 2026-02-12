#!/usr/bin/env python3
"""
reclassify.py
Reklassifiziert alle bestehenden Artikel in der Datenbank
mit der verbesserten Kategorisierung (inkl. Unterkategorien).
"""

import sqlite3
from pathlib import Path
from collections import defaultdict
from receipt_analyzer import CategoryClassifier

DB_PATH = Path(__file__).parent / 'receipts.db'

def reclassify_all():
    """Reklassifiziert alle Artikel in der Datenbank"""
    if not DB_PATH.exists():
        print("❌ receipts.db nicht gefunden!")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Alle Artikel laden
    cursor.execute('SELECT item_id, name, category FROM items')
    items = cursor.fetchall()
    
    if not items:
        print("📭 Keine Artikel in der Datenbank.")
        conn.close()
        return
    
    print()
    print("=" * 80)
    print("  REKLASSIFIZIERUNG MIT UNTERKATEGORIEN")
    print("=" * 80)
    print(f"  Gefundene Artikel: {len(items)}")
    print()
    
    # Änderungen sammeln
    changes = []
    for item_id, name, old_category in items:
        new_category = CategoryClassifier.classify(name)
        if new_category != old_category:
            changes.append((item_id, name, old_category, new_category))
    
    if not changes:
        print("  ✅ Alle Artikel sind bereits korrekt klassifiziert.")
        print("=" * 80)
        conn.close()
        return
    
    # Gruppiere nach Hauptkategorie (vor dem "-")
    grouped = defaultdict(list)
    for item_id, name, old_cat, new_cat in changes:
        main_cat = new_cat.split(' - ')[0] if ' - ' in new_cat else new_cat
        grouped[main_cat].append((item_id, name, old_cat, new_cat))
    
    print(f"  📊 Änderungen: {len(changes)} Artikel in {len(grouped)} Hauptkategorien")
    print()
    
    # Zeige gruppiert nach Hauptkategorie
    shown = 0
    for main_cat in sorted(grouped.keys()):
        items_in_cat = grouped[main_cat]
        print(f"  ─── {main_cat} ({len(items_in_cat)} Artikel) ───")
        
        for item_id, name, old_cat, new_cat in items_in_cat[:5]:  # Max 5 pro Kategorie
            old_short = old_cat.split(' - ')[-1] if ' - ' in old_cat else old_cat
            new_short = new_cat.split(' - ')[-1] if ' - ' in new_cat else new_cat
            print(f"    {name[:40]:42s}  {old_short:15s} → {new_short}")
            shown += 1
        
        if len(items_in_cat) > 5:
            print(f"    ... und {len(items_in_cat) - 5} weitere")
        print()
        
        if shown >= 30:  # Max 30 gesamt
            remaining = len(changes) - shown
            if remaining > 0:
                print(f"  ... und {remaining} weitere Änderungen")
            break
    
    print("=" * 80)
    
    confirm = input("  Änderungen übernehmen? (JA/nein): ")
    if confirm.upper() != "JA":
        print("  Abgebrochen.")
        conn.close()
        return
    
    # Änderungen durchführen
    for item_id, _, _, new_category in changes:
        cursor.execute('UPDATE items SET category = ? WHERE item_id = ?',
                      (new_category, item_id))
    
    conn.commit()
    conn.close()
    
    print()
    print(f"  ✅ {len(changes)} Artikel neu klassifiziert!")
    print("=" * 80)
    print()


if __name__ == '__main__':
    reclassify_all()
    input("  Drücke ENTER zum Beenden…")

