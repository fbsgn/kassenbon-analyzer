#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ersetzt DEIN-USERNAME durch fbsgn in allen relevanten Dateien
"""

from pathlib import Path
import re

USERNAME = "fbsgn"

files_to_update = [
    "README.md",
    "GITHUB_ANLEITUNG.txt",
    "kassenbon_analyzer_offline_full/README_OFFLINE.md",
    "kassenbon_analyzer_offline_full/README_START_HIER.txt",
]

print("=" * 60)
print("USERNAME-REPLACER")
print("=" * 60)
print(f"\nErsetze 'DEIN-USERNAME' durch '{USERNAME}'\n")

updated_count = 0

for file_path in files_to_update:
    path = Path(file_path)
    
    if not path.exists():
        print(f"⏭️  SKIP: {file_path} (nicht gefunden)")
        continue
    
    try:
        content = path.read_text(encoding='utf-8')
        original_content = content
        
        # Ersetze alle Vorkommen
        content = content.replace('DEIN-USERNAME', USERNAME)
        content = content.replace('DEIN-username', USERNAME)
        content = content.replace('dein-username', USERNAME)
        
        if content != original_content:
            path.write_text(content, encoding='utf-8')
            count = original_content.count('DEIN-USERNAME')
            print(f"✅ {file_path}: {count} Ersetzungen")
            updated_count += 1
        else:
            print(f"⏭️  {file_path}: Keine Änderungen nötig")
            
    except Exception as e:
        print(f"❌ FEHLER bei {file_path}: {e}")

print("\n" + "=" * 60)
print(f"✅ FERTIG! {updated_count} Dateien aktualisiert")
print("=" * 60)
print("\nNächste Schritte:")
print("  git add .")
print('  git commit -m "Update GitHub username to fbsgn"')
print("  git push")
print("=" * 60)
