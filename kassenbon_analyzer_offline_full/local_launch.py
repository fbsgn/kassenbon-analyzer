#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from web_app import app

def run_backup():
    try:
        print("[INFO] Erstelle automatisches Backup...")
        subprocess.run(["python", "backup_restore.py", "backup"], check=False)
    except Exception as e:
        print(f"[WARN] Backup fehlgeschlagen: {e}")

if __name__ == "__main__":
    run_backup()
    host = "0.0.0.0" if os.getenv("ALLOW_LAN") == "1" else "127.0.0.1"
    print(f"[INFO] Starte App auf http://{host}:5000")
    app.run(debug=False, host=host, port=5000, use_reloader=False)
