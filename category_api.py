"""
API-Endpunkte für Kategorie-Verwaltung
"""

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Lade alle Kategorien aus categories.json"""
    try:
        import json
        with open('categories.json', 'r', encoding='utf-8') as f:
            categories = json.load(f)
        return jsonify(categories)
    except Exception as e:
        logger.exception("[ERROR] Kategorien laden fehlgeschlagen")
        return jsonify({'error': str(e)}), 500


@app.route('/api/categories', methods=['POST'])
def save_categories():
    """Speichere Kategorien in categories.json"""
    try:
        import json
        categories = request.json
        
        # Validierung
        if not isinstance(categories, dict):
            return jsonify({'error': 'Ungültiges Format'}), 400
        
        # Backup erstellen
        import shutil
        from pathlib import Path
        backup_path = Path('categories.json.backup')
        if Path('categories.json').exists():
            shutil.copy2('categories.json', backup_path)
        
        # Speichern
        with open('categories.json', 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[OK] Kategorien gespeichert ({len(categories)} Kategorien)")
        return jsonify({'success': True, 'count': len(categories)})
        
    except Exception as e:
        logger.exception("[ERROR] Kategorien speichern fehlgeschlagen")
        return jsonify({'error': str(e)}), 500


@app.route('/api/categories/reclassify', methods=['POST'])
def reclassify_items():
    """Klassifiziere alle Artikel neu mit aktualisierten Kategorien"""
    try:
        # Lade neue Kategorien
        import json
        with open('categories.json', 'r', encoding='utf-8') as f:
            categories = json.load(f)
        
        # Importiere Klassifizierungs-Logik
        from receipt_analyzer import classify_item
        
        db = get_db()
        cursor = db.cursor()
        
        # Hole alle Artikel
        cursor.execute('SELECT item_id, name, category FROM items')
        items = cursor.fetchall()
        
        updated = 0
        for item in items:
            old_category = item['category']
            new_category = classify_item(item['name'], categories)
            
            if new_category != old_category:
                cursor.execute(
                    'UPDATE items SET category = ? WHERE item_id = ?',
                    (new_category, item['item_id'])
                )
                updated += 1
        
        db.commit()
        logger.info(f"[OK] {updated} Artikel neu klassifiziert")
        
        return jsonify({
            'success': True,
            'total_items': len(items),
            'updated': updated
        })
        
    except Exception as e:
        logger.exception("[ERROR] Neu-Klassifizierung fehlgeschlagen")
        return jsonify({'error': str(e)}), 500
