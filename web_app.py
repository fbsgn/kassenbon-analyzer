#!/usr/bin/env python3
"""
Web-Interface für Kassenbon-Analyse (VERBESSERT)
✅ 3️⃣ Verlässliche PDF-Zuordnung via DB
✅ 2️⃣ Sauberes Fehler-Handling + Logging
"""

from flask import Flask, render_template, request, jsonify, g, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import sqlite3
import os
import shutil
import hashlib
import logging
from receipt_analyzer import ReceiptParser
from batch_import import run_import, EINGANG
from datetime import datetime
import json

# ══════════════════════════════════════════════════════
# LOGGING SETUP
# ══════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('kassenbon_analyzer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════
# FLASK APP SETUP
# ══════════════════════════════════════════════════════
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['DATABASE'] = 'receipts.db'
app.config['PDF_STORAGE'] = Path('Ablage')  # PDF-Archiv

# Template-Caching deaktivieren
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.jinja_env.auto_reload = True
app.jinja_env.cache = {}

# Erstelle notwendige Ordner
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
app.config['PDF_STORAGE'].mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════════════════
# ERROR CLASSES
# ══════════════════════════════════════════════════════
class AppError(Exception):
    """Basis-Fehlerklasse für alle App-Fehler"""
    def __init__(self, message, code=500, details=None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

class PDFNotFoundError(AppError):
    """PDF-Datei nicht gefunden"""
    def __init__(self, receipt_id):
        super().__init__(
            f"PDF für Kassenbon #{receipt_id} nicht gefunden",
            code=404,
            details={'receipt_id': receipt_id}
        )

class ReceiptNotFoundError(AppError):
    """Kassenbon nicht in DB gefunden"""
    def __init__(self, receipt_id):
        super().__init__(
            f"Kassenbon #{receipt_id} nicht in Datenbank",
            code=404,
            details={'receipt_id': receipt_id}
        )

class ParseError(AppError):
    """Fehler beim PDF-Parsing"""
    def __init__(self, filename, original_error):
        super().__init__(
            f"Parsing fehlgeschlagen: {filename}",
            code=500,
            details={'filename': filename, 'error': str(original_error)}
        )


# ══════════════════════════════════════════════════════
# DATABASE FUNCTIONS
# ══════════════════════════════════════════════════════
def get_db():
    """Erstellt eine neue Datenbankverbindung für jeden Thread/Request"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        init_database(db)
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Schließt die DB-Verbindung am Ende des Requests"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_database(db):
    """Erstellt die Datenbankstruktur falls nicht vorhanden"""
    cursor = db.cursor()
    
    # ✅ NEU: pdf_path Spalte hinzugefügt!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT,
            store_address TEXT,
            date TIMESTAMP,
            total_amount REAL,
            payment_method TEXT,
            pdf_path TEXT,
            pdf_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER,
            name TEXT,
            unit_price REAL,
            quantity INTEGER,
            total_price REAL,
            tax_category TEXT,
            category TEXT,
            FOREIGN KEY (receipt_id) REFERENCES receipts (receipt_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            price REAL,
            date TIMESTAMP,
            store_name TEXT,
            UNIQUE(item_name, date, store_name)
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_name ON items(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_price_history_name ON price_history(item_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_receipts_pdf_hash ON receipts(pdf_hash)')
    
    db.commit()
    logger.info("[OK] Datenbank initialisiert")


# ══════════════════════════════════════════════════════
# PDF HELPER FUNCTIONS
# ══════════════════════════════════════════════════════
def calculate_file_hash(filepath):
    """Berechnet SHA256-Hash einer Datei"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def store_pdf(source_path, receipt_date, store_name):
    """
    ✅ 3️⃣ Speichert PDF im Ablage-Ordner und gibt Pfad zurück
    
    Returns: (pdf_path, pdf_hash)
    """
    try:
        # Erstelle Ordnerstruktur: Ablage/YYYY/MM/
        year = receipt_date.strftime("%Y")
        month = receipt_date.strftime("%m")
        storage_dir = app.config['PDF_STORAGE'] / year / month
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Generiere eindeutigen Dateinamen
        date_str = receipt_date.strftime("%Y-%m-%d")
        base_name = f"Kassenbon_{date_str}_{store_name.replace(' ', '_')}"
        
        # Finde freien Dateinamen (falls Duplikate)
        counter = 1
        pdf_filename = f"{base_name}.pdf"
        pdf_path = storage_dir / pdf_filename
        
        while pdf_path.exists():
            pdf_filename = f"{base_name}_{counter}.pdf"
            pdf_path = storage_dir / pdf_filename
            counter += 1
        
        # Kopiere PDF
        shutil.copy2(source_path, pdf_path)
        
        # Berechne Hash
        pdf_hash = calculate_file_hash(pdf_path)
        
        # Relativer Pfad zur Speicherung in DB
        rel_path = str(pdf_path.relative_to(Path.cwd()))
        
        logger.info(f"[OK] PDF gespeichert: {rel_path}")
        return rel_path, pdf_hash
        
    except Exception as e:
        logger.error(f"[ERROR] PDF-Speicherung fehlgeschlagen: {e}")
        raise AppError(f"PDF-Speicherung fehlgeschlagen: {e}", code=500)


def check_duplicate_by_hash(pdf_hash):
    """Prüft ob PDF mit diesem Hash bereits existiert"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT receipt_id FROM receipts WHERE pdf_hash = ?', (pdf_hash,))
    row = cursor.fetchone()
    return row['receipt_id'] if row else None


# ══════════════════════════════════════════════════════
# DATABASE OPERATIONS
# ══════════════════════════════════════════════════════
def save_receipt_to_db(receipt, pdf_path, pdf_hash):
    """Speichert einen Kassenbon MIT PDF-Referenz in der Datenbank"""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO receipts (store_name, store_address, date, total_amount, 
                                payment_method, pdf_path, pdf_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (receipt.store_name, receipt.store_address, receipt.date, 
              receipt.total_amount, receipt.payment_method, pdf_path, pdf_hash))
        
        receipt_id = cursor.lastrowid
        
        for item in receipt.items:
            cursor.execute('''
                INSERT INTO items (receipt_id, name, unit_price, quantity, total_price, 
                                  tax_category, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (receipt_id, item.name, item.unit_price, item.quantity, 
                  item.total_price, item.tax_category, item.category))
            
            try:
                cursor.execute('''
                    INSERT INTO price_history (item_name, price, date, store_name)
                    VALUES (?, ?, ?, ?)
                ''', (item.name, item.unit_price, receipt.date, receipt.store_name))
            except sqlite3.IntegrityError:
                pass  # Duplikat in Price History - ist OK
        
        db.commit()
        logger.info(f"[OK] Kassenbon #{receipt_id} gespeichert")
        return receipt_id
        
    except sqlite3.Error as e:
        db.rollback()
        logger.error(f"[ERROR] DB-Fehler: {e}")
        raise AppError(f"Datenbank-Fehler: {e}", code=500)


# ══════════════════════════════════════════════════════
# API ROUTES
# ══════════════════════════════════════════════════════
@app.route('/')
def index():
    """Hauptseite"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_receipt():
    """
    ✅ VERBESSERT: Upload mit PDF-Speicherung und Duplikat-Check
    """
    try:
        # Validierung
        if 'file' not in request.files:
            raise AppError('Keine Datei hochgeladen', code=400)
        
        file = request.files['file']
        if file.filename == '':
            raise AppError('Keine Datei ausgewählt', code=400)
        
        if not file.filename.endswith('.pdf'):
            raise AppError('Nur PDF-Dateien erlaubt', code=400)
        
        # Temporäre Speicherung
        filename = secure_filename(file.filename)
        temp_path = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(temp_path)
        
        try:
            # Berechne Hash BEVOR Parsing
            pdf_hash = calculate_file_hash(temp_path)
            
            # Duplikat-Check
            existing_id = check_duplicate_by_hash(pdf_hash)
            if existing_id:
                logger.warning(f"[WARN] Duplikat erkannt: {filename} (bereits als #{existing_id})")
                return jsonify({
                    'success': False,
                    'error': 'Duplikat',
                    'message': f'Diese PDF wurde bereits verarbeitet (Kassenbon #{existing_id})',
                    'existing_receipt_id': existing_id
                }), 409
            
            # Parse PDF
            parser = ReceiptParser()
            receipt = parser.parse_pdf(temp_path)
            
            # Speichere PDF im Archiv
            pdf_path, pdf_hash = store_pdf(temp_path, receipt.date, receipt.store_name)
            
            # Speichere in DB
            receipt_id = save_receipt_to_db(receipt, pdf_path, pdf_hash)
            
            logger.info(f"[OK] Upload erfolgreich: {filename} -> #{receipt_id}")
            
            return jsonify({
                'success': True,
                'receipt_id': receipt_id,
                'store': receipt.store_name,
                'date': receipt.date.isoformat() if receipt.date else None,
                'total': receipt.total_amount,
                'items_count': len(receipt.items)
            })
            
        except Exception as e:
            logger.error(f"[ERROR] Parsing-Fehler {filename}: {e}")
            raise ParseError(filename, e)
        
        finally:
            # Lösche temporäre Datei
            temp_path.unlink(missing_ok=True)
    
    except AppError as e:
        return jsonify({'success': False, 'error': e.message}), e.code
    except Exception as e:
        logger.exception("[ERROR] Unerwarteter Fehler beim Upload")
        return jsonify({'success': False, 'error': 'Interner Serverfehler'}), 500


@app.route('/api/receipt/<int:receipt_id>/pdf')
def serve_receipt_pdf(receipt_id):
    """
    HYBRID: Funktioniert mit alter UND neuer Datenbank
    - Neue DB: pdf_path vorhanden -> direkt verwenden
    - Alte DB: pdf_path NULL -> Glob-Suche im Ablage-Ordner
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Hole Kassenbon-Details
        cursor.execute('''
            SELECT pdf_path, store_name, date
            FROM receipts
            WHERE receipt_id = ?
        ''', (receipt_id,))
        
        row = cursor.fetchone()
        if not row:
            raise ReceiptNotFoundError(receipt_id)
        
        # HYBRID: Prüfe ob pdf_path vorhanden (neue DB)
        if row['pdf_path'] and row['pdf_path'].strip():
            # NEU: Direkter Pfad aus DB
            pdf_path = Path(row['pdf_path'])
            
            if not pdf_path.exists():
                logger.error(f"[ERROR] PDF existiert nicht: {pdf_path}")
                raise PDFNotFoundError(receipt_id)
            
            logger.info(f"[PDF] PDF ausgeliefert (DB): {pdf_path.name}")
        else:
            # ALT: Fallback auf Glob-Suche
            store_name = row['store_name']
            date = row['date']
            
            if not date:
                return jsonify({'error': 'Kein Datum vorhanden'}), 404
            
            # Baue Pfad im Ablage-Ordner
            from datetime import datetime as dt
            date_obj = dt.fromisoformat(date)
            year = date_obj.strftime("%Y")
            month = date_obj.strftime("%m")
            date_str = date_obj.strftime("%Y-%m-%d")
            
            ablage_dir = Path('Ablage') / year / month
            
            if not ablage_dir.exists():
                return jsonify({'error': 'Ablage-Ordner nicht gefunden'}), 404
            
            # Suche nach passender PDF
            pattern = f"Kassenbon_{date_str}_*.pdf"
            matching_files = list(ablage_dir.glob(pattern))
            
            if not matching_files:
                return jsonify({'error': 'PDF-Datei nicht gefunden'}), 404
            
            pdf_path = matching_files[0]
            logger.info(f"[PDF] PDF ausgeliefert (GLOB): {pdf_path.name}")
        
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=False,
            download_name=pdf_path.name
        )
    
    except AppError as e:
        return jsonify({'error': e.message}), e.code
    except Exception as e:
        logger.exception(f"[ERROR] Fehler beim PDF-Abruf für #{receipt_id}")
        return jsonify({'error': 'Interner Serverfehler'}), 500


# ══════════════════════════════════════════════════════
# REST: Alle anderen Endpoints (unverändert)
# ══════════════════════════════════════════════════════
@app.route('/api/import/check')
def import_check():
    """Gibt an wie viele PDFs im Eingangsordner auf Verarbeitung warten."""
    pdfs = sorted(EINGANG.glob("*.pdf"))
    return jsonify({
        'ordner': str(EINGANG),
        'anzahl': len(pdfs),
        'dateien': [p.name for p in pdfs]
    })


@app.route('/api/import/start', methods=['POST'])
def import_start():
    """Startet den Batch-Import aller PDFs aus dem Eingangsordner."""
    try:
        results = run_import()
        ok  = sum(1 for r in results if r["status"] == "ok")
        dup = sum(1 for r in results if r["status"] == "duplikat")
        err = sum(1 for r in results if r["status"] == "fehler")

        return jsonify({
            'success': True,
            'zusammenfassung': {
                'gesamt': len(results),
                'neu': ok,
                'duplikat': dup,
                'fehler': err
            },
            'details': results
        })
    except Exception as e:
        logger.exception("[ERROR] Batch-Import fehlgeschlagen")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/statistics')
def get_statistics():
    """Statistiken über alle Kategorien - mit optionalen Filtern"""
    db = get_db()
    cursor = db.cursor()
    
    store = request.args.get('store', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = '''
        SELECT i.category, 
               COUNT(*) as count,
               SUM(i.total_price) as total_spent,
               AVG(i.unit_price) as avg_price
        FROM items i
        JOIN receipts r ON i.receipt_id = r.receipt_id
        WHERE i.category != 'System'
    '''
    params = []
    
    if store:
        query += ' AND r.store_name LIKE ?'
        params.append(f'%{store}%')
    if date_from:
        query += ' AND r.date >= ?'
        params.append(date_from)
    if date_to:
        query += ' AND r.date <= ?'
        params.append(date_to + 'T23:59:59')
    
    query += ' GROUP BY i.category ORDER BY total_spent DESC'
    
    cursor.execute(query, params)
    
    stats = {}
    for row in cursor.fetchall():
        stats[row['category']] = {
            'count': row['count'],
            'total_spent': round(row['total_spent'], 2),
            'avg_price': round(row['avg_price'], 2)
        }
    
    return jsonify(stats)


@app.route('/api/history')
def get_history():
    """Einkaufshistorie – mit optionalen Filtern"""
    db = get_db()
    cursor = db.cursor()
    limit = request.args.get('limit', 20, type=int)

    store = request.args.get('store', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    query = 'SELECT receipt_id, store_name, date, total_amount, payment_method FROM receipts WHERE 1=1'
    params = []

    if store:
        query += ' AND store_name LIKE ?'
        params.append(f'%{store}%')
    if date_from:
        query += ' AND date >= ?'
        params.append(date_from)
    if date_to:
        query += ' AND date <= ?'
        params.append(date_to + 'T23:59:59')

    query += ' ORDER BY date DESC LIMIT ?'
    params.append(limit)

    cursor.execute(query, params)
    
    history = []
    for row in cursor.fetchall():
        history.append({
            'receipt_id': row['receipt_id'],
            'store_name': row['store_name'],
            'date': row['date'],
            'total_amount': row['total_amount'],
            'payment_method': row['payment_method']
        })
    
    return jsonify(history)


@app.route('/api/search')
def search_items():
    """Artikelsuche"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT DISTINCT i.name, i.category, 
               AVG(i.unit_price) as avg_price,
               COUNT(*) as purchase_count
        FROM items i
        WHERE i.name LIKE ? AND i.category != 'System'
        GROUP BY i.name, i.category
        ORDER BY purchase_count DESC
    ''', (f'%{query}%',))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'name': row['name'],
            'category': row['category'],
            'avg_price': round(row['avg_price'], 2),
            'purchase_count': row['purchase_count']
        })
    
    return jsonify(results)


@app.route('/api/category-details/<category>')
def get_category_details(category):
    """Details zu allen Artikeln einer Kategorie"""
    db = get_db()
    cursor = db.cursor()
    
    store = request.args.get('store', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = '''
        SELECT i.name, i.unit_price as price, i.quantity,
               r.date, r.store_name
        FROM items i
        JOIN receipts r ON i.receipt_id = r.receipt_id
        WHERE i.category = ?
    '''
    params = [category]
    
    if store:
        query += ' AND r.store_name LIKE ?'
        params.append(f'%{store}%')
    if date_from:
        query += ' AND r.date >= ?'
        params.append(date_from)
    if date_to:
        query += ' AND r.date <= ?'
        params.append(date_to + 'T23:59:59')
    
    query += ' ORDER BY r.date DESC, i.name'
    
    cursor.execute(query, params)
    
    items = []
    for row in cursor.fetchall():
        items.append({
            'name': row['name'],
            'price': row['price'],
            'quantity': row['quantity'],
            'date': row['date'],
            'store_name': row['store_name']
        })
    
    return jsonify(items)


@app.route('/api/stores')
def get_stores():
    """Liste aller Geschäfte"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT DISTINCT store_name FROM receipts ORDER BY store_name')
    stores = [row['store_name'] for row in cursor.fetchall()]
    return jsonify(stores)


@app.route('/api/date-range')
def get_date_range():
    """Zeitraum der vorhandenen Daten"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT MIN(date) as min_date, MAX(date) as max_date FROM receipts')
    row = cursor.fetchone()
    return jsonify({'min_date': row['min_date'], 'max_date': row['max_date']})


@app.route('/api/export/excel')
def export_excel():
    """Exportiere alle Daten als CSV"""
    try:
        import io, csv
        from flask import Response
        
        db = get_db()
        cursor = db.cursor()
        
        store = request.args.get('store', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        query = '''
            SELECT r.date, r.store_name, r.total_amount, r.payment_method,
                   i.name, i.category, i.unit_price, i.quantity, i.total_price
            FROM receipts r
            JOIN items i ON r.receipt_id = i.receipt_id
            WHERE i.category != 'System'
        '''
        params = []
        
        if store:
            query += ' AND r.store_name LIKE ?'
            params.append(f'%{store}%')
        if date_from:
            query += ' AND r.date >= ?'
            params.append(date_from)
        if date_to:
            query += ' AND r.date <= ?'
            params.append(date_to + 'T23:59:59')
        
        query += ' ORDER BY r.date DESC'
        cursor.execute(query, params)
        
        output = io.StringIO()
        writer = csv.writer(output, delimiter=';')
        
        writer.writerow(['Datum', 'Geschäft', 'Artikel', 'Kategorie', 'Einzelpreis', 
                        'Menge', 'Gesamtpreis', 'Kassenbon-Summe', 'Zahlungsmethode'])
        
        for row in cursor.fetchall():
            date_str = row['date'][:10] if row['date'] else ''
            writer.writerow([
                date_str, row['store_name'], row['name'], row['category'],
                f"{row['unit_price']:.2f}".replace('.', ','),
                row['quantity'],
                f"{row['total_price']:.2f}".replace('.', ','),
                f"{row['total_amount']:.2f}".replace('.', ','),
                row['payment_method']
            ])
        
        output.seek(0)
        filename = f"kassenbons_{datetime.now().strftime('%Y-%m-%d')}.csv"
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        logger.exception("[ERROR] Export fehlgeschlagen")
        return jsonify({'error': str(e)}), 500


@app.route('/api/item-price-history/<item_name>')
def get_item_price_history(item_name):
    """Preisverlauf eines spezifischen Artikels"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT i.unit_price as price, r.date, r.store_name
        FROM items i
        JOIN receipts r ON i.receipt_id = r.receipt_id
        WHERE i.name = ?
        ORDER BY r.date ASC
    ''', (item_name,))
    
    history = []
    for row in cursor.fetchall():
        history.append({
            'price': row['price'],
            'date': row['date'],
            'store_name': row['store_name']
        })
    
    return jsonify(history)


@app.route('/api/dashboard')
def get_dashboard_data():
    """Dashboard-Daten"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT category, COUNT(*) as count, SUM(total_price) as total_spent, AVG(unit_price) as avg_price
        FROM items WHERE category != 'System'
        GROUP BY category ORDER BY total_spent DESC
    ''')
    
    stats = {}
    for row in cursor.fetchall():
        stats[row['category']] = {
            'count': row['count'],
            'total_spent': round(row['total_spent'], 2),
            'avg_price': round(row['avg_price'], 2)
        }
    
    total_spent = sum(cat['total_spent'] for cat in stats.values())
    
    cursor.execute('SELECT COUNT(*) as cnt FROM receipts')
    total_receipts = cursor.fetchone()['cnt']
    
    cursor.execute("SELECT COUNT(*) as cnt FROM items WHERE category != 'System'")
    total_items = cursor.fetchone()['cnt']
    
    return jsonify({
        'total_spent': round(total_spent, 2),
        'total_receipts': total_receipts,
        'total_items': total_items
    })


@app.route('/api/system/reset', methods=['POST'])
def system_reset():
    """Kompletter System-Reset"""
    try:
        errors = []
        
        # Datenbank löschen
        db_path = Path(app.config['DATABASE'])
        if db_path.exists():
            try:
                db_path.unlink()
                logger.info("[OK] Datenbank gelöscht")
            except Exception as e:
                errors.append(f"Datenbank: {e}")
        
        # Ablage-Ordner löschen
        if app.config['PDF_STORAGE'].exists():
            try:
                shutil.rmtree(app.config['PDF_STORAGE'])
                app.config['PDF_STORAGE'].mkdir()
                logger.info("[OK] Ablage gelöscht")
            except Exception as e:
                errors.append(f"Ablage: {e}")
        
        # Fehler-Ordner löschen
        fehler_path = Path('Fehler')
        if fehler_path.exists():
            try:
                shutil.rmtree(fehler_path)
                logger.info("[OK] Fehler-Ordner gelöscht")
            except Exception as e:
                errors.append(f"Fehler: {e}")
        
        # Neue DB initialisieren
        try:
            conn = sqlite3.connect(str(db_path))
            init_database(conn)
            conn.close()
            logger.info("[OK] Neue Datenbank erstellt")
        except Exception as e:
            errors.append(f"DB-Init: {e}")
        
        if errors:
            return jsonify({'success': False, 'error': '; '.join(errors)}), 500
        
        return jsonify({'success': True, 'message': 'System zurückgesetzt'})
    
    except Exception as e:
        logger.exception("[ERROR] System-Reset fehlgeschlagen")
        return jsonify({'success': False, 'error': str(e)}), 500






# ══════════════════════════════════════════════════════
# PWA SUPPORT
# ══════════════════════════════════════════════════════
@app.route('/manifest.json')
def manifest():
    """PWA Manifest"""
    return send_file('manifest.json', mimetype='application/json')


@app.route('/service-worker.js')
def service_worker():
    """Service Worker für Offline-Support"""
    return send_file('service-worker.js', mimetype='application/javascript')


# ══════════════════════════════════════════════════════
# KATEGORIE-VERWALTUNG
# ══════════════════════════════════════════════════════
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Lade alle Kategorien aus categories.json"""
    try:
        with open('categories.json', 'r', encoding='utf-8') as f:
            categories = json.load(f)
        logger.info(f"[OK] {len(categories)} Kategorien geladen")
        return jsonify(categories)
    except Exception as e:
        logger.exception("[ERROR] Kategorien laden fehlgeschlagen")
        return jsonify({'error': str(e)}), 500


@app.route('/api/categories', methods=['POST'])
def save_categories():
    """Speichere Kategorien in categories.json"""
    try:
        categories = request.json
        
        if not isinstance(categories, dict):
            return jsonify({'error': 'Ungültiges Format'}), 400
        
        backup_path = Path('categories.json.backup')
        if Path('categories.json').exists():
            shutil.copy2('categories.json', backup_path)
            logger.info("[OK] Backup erstellt")
        
        with open('categories.json', 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[OK] {len(categories)} Kategorien gespeichert")
        return jsonify({'success': True, 'count': len(categories)})
        
    except Exception as e:
        logger.exception("[ERROR] Kategorien speichern fehlgeschlagen")
        return jsonify({'error': str(e)}), 500


@app.route('/api/categories/reclassify', methods=['POST'])
def reclassify_items():
    """Klassifiziere alle Artikel neu mit aktualisierten Kategorien"""
    try:
        # Lade die AKTUELLEN Kategorien aus der Datei
        with open('categories.json', 'r', encoding='utf-8') as f:
            categories = json.load(f)
        
        logger.info(f"[INFO] Starte Reklassifizierung mit {len(categories)} Kategorien")
        
        # Erstelle neuen Parser (lädt alte Kategorien)
        parser = ReceiptParser()
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT item_id, name, category FROM items')
        items = cursor.fetchall()
        
        updated = 0
        for item in items:
            old_category = item['category']
            # WICHTIG: Übergebe die NEUEN Kategorien an classify_item!
            new_category = parser.classify_item(item['name'], categories)
            
            if new_category != old_category:
                cursor.execute(
                    'UPDATE items SET category = ? WHERE item_id = ?',
                    (new_category, item['item_id'])
                )
                updated += 1
                logger.info(f"[RECLASSIFY] '{item['name']}': {old_category} → {new_category}")
        
        db.commit()
        logger.info(f"[OK] {updated} von {len(items)} Artikeln neu klassifiziert")
        
        return jsonify({
            'success': True,
            'total_items': len(items),
            'updated': updated
        })
        
    except Exception as e:
        logger.exception("[ERROR] Neu-Klassifizierung fehlgeschlagen")
        return jsonify({'error': str(e)}), 500


# ══════════════════════════════════════════════════════
# ERROR HANDLERS
# ══════════════════════════════════════════════════════
@app.errorhandler(AppError)
def handle_app_error(error):
    """Zentrale Fehlerbehandlung für AppError"""
    logger.error(f"AppError: {error.message} (Code {error.code})")
    return jsonify({'error': error.message, 'details': error.details}), error.code


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpunkt nicht gefunden'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.exception("❌ Interner Serverfehler")
    return jsonify({'error': 'Interner Serverfehler'}), 500


# ══════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════
if __name__ == '__main__':
    print("\n" + "="*60)
    print("KASSENBON-ANALYZER V2 (VERBESSERT)")
    print("="*60)
    print("[OK] PDF-Zuordnung via Datenbank")
    print("[OK] Sauberes Error-Handling + Logging")
    print("[OK] Duplikat-Erkennung via Hash")
    print(f"\n[DIR] Working Directory: {os.getcwd()}")
    print(f"[DIR] PDF Storage: {app.config['PDF_STORAGE']}")
    print(f"[LOG] Logfile: kassenbon_analyzer.log")
    print("\n[WEB] Server: http://localhost:5000")
    print("="*60 + "\n")
    
    logger.info("[START] Server gestartet")
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
