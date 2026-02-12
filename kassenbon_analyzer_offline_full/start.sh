#!/bin/bash
set -e

echo "==========================================="
echo "   KASSENBON-ANALYZER OFFLINE STARTER"
echo "==========================================="

echo "[INFO] Fuehre Auto-Backup aus..."
python backup_restore.py backup || echo "[WARN] Backup fehlgeschlagen"

echo "[INFO] Starte lokalen Server..."
python local_launch.py
