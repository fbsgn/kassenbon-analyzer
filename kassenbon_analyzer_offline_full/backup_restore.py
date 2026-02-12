#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Backup & Restore für Kassenbon-Analyzer (offline)
#
# Befehle:
#   python backup_restore.py backup          # erstellt Backup in backups/
#   python backup_restore.py list            # listet Backups
#   python backup_restore.py restore <name>  # stellt gewähltes Backup wieder her
#
# Gesichert werden:
#   - receipts.db (falls vorhanden)
#   - Ablage/ (PDF-Archiv, rekursiv)
#   - categories.json
#
# Sicherungsformat:
#   backups/<timestamp>_kb_backup.zip
#
# Restore legt aktuelle Daten vor Überschreiben als backups/safety_<timestamp>/ ab.

import argparse
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
BACKUPS = ROOT / 'backups'
DB = ROOT / 'receipts.db'
ARCHIVE_DIR = ROOT / 'Ablage'
CATEGORIES = ROOT / 'categories.json'

BACKUPS.mkdir(exist_ok=True)

def make_backup():
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    name = BACKUPS / f"{ts}_kb_backup.zip"
    with zipfile.ZipFile(name, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        if DB.exists():
            z.write(DB, arcname='receipts.db')
        if CATEGORIES.exists():
            z.write(CATEGORIES, arcname='categories.json')
        if ARCHIVE_DIR.exists():
            for p in ARCHIVE_DIR.rglob('*'):
                if p.is_file():
                    z.write(p, arcname=str(p.relative_to(ROOT)))
    print(f"[OK] Backup erzeugt: {name}")

def list_backups():
    files = sorted(BACKUPS.glob('*_kb_backup.zip'))
    if not files:
        print("Keine Backups vorhanden.")
        return
    for f in files:
        print(f.name)

def restore_backup(name: str):
    zip_path = BACKUPS / name
    if not zip_path.exists():
        print(f"Backup nicht gefunden: {zip_path}")
        return
    # Safety copy aktueller Zustand
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    safety = BACKUPS / f"safety_{ts}"
    safety.mkdir(exist_ok=True)
    if DB.exists():
        shutil.copy2(DB, safety / 'receipts.db')
    if CATEGORIES.exists():
        shutil.copy2(CATEGORIES, safety / 'categories.json')
    if ARCHIVE_DIR.exists():
        dest = safety / 'Ablage'
        shutil.copytree(ARCHIVE_DIR, dest, dirs_exist_ok=True)
    # Entpacken
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(ROOT)
    print(f"[OK] Wiederhergestellt aus: {zip_path}")
    print(f"[SAFE] Vorheriger Zustand gesichert in: {safety}")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('backup')
    sub.add_parser('list')
    r = sub.add_parser('restore')
    r.add_argument('name', help='Dateiname des Backups in backups/')
    args = ap.parse_args()
    if args.cmd == 'backup':
        make_backup()
    elif args.cmd == 'list':
        list_backups()
    elif args.cmd == 'restore':
        restore_backup(args.name)

if __name__ == '__main__':
    main()
