#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erstellt PWA-Icons für Kassenbon-Analyzer"""

from pathlib import Path

print("=" * 70)
print("PWA ICON GENERATOR")
print("=" * 70)

# Erstelle static-Ordner falls nicht vorhanden
static_dir = Path('static')
static_dir.mkdir(exist_ok=True)

# SVG Icon (für hochauflösende Darstellung)
svg_icon = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <!-- Hintergrund -->
  <rect width="512" height="512" rx="115" fill="#4f46e5"/>
  
  <!-- Kassenbon -->
  <rect x="140" y="80" width="232" height="352" rx="8" fill="white"/>
  
  <!-- Gezackte Kante unten -->
  <path d="M140,432 L156,420 L172,432 L188,420 L204,432 L220,420 L236,432 L252,420 L268,432 L284,420 L300,432 L316,420 L332,432 L348,420 L364,432 L372,432 L372,440 L140,440 Z" fill="white"/>
  
  <!-- Text-Linien -->
  <line x1="180" y1="140" x2="332" y2="140" stroke="#4f46e5" stroke-width="8" stroke-linecap="round"/>
  <line x1="180" y1="180" x2="332" y2="180" stroke="#d1d5db" stroke-width="6" stroke-linecap="round"/>
  <line x1="180" y1="210" x2="280" y2="210" stroke="#d1d5db" stroke-width="6" stroke-linecap="round"/>
  <line x1="180" y1="240" x2="320" y2="240" stroke="#d1d5db" stroke-width="6" stroke-linecap="round"/>
  <line x1="180" y1="270" x2="260" y2="270" stroke="#d1d5db" stroke-width="6" stroke-linecap="round"/>
  
  <!-- Trennlinie -->
  <line x1="160" y1="320" x2="352" y2="320" stroke="#e5e7eb" stroke-width="2" stroke-dasharray="8,4"/>
  
  <!-- Summe -->
  <line x1="180" y1="360" x2="332" y2="360" stroke="#4f46e5" stroke-width="10" stroke-linecap="round"/>
  
  <!-- Euro-Symbol -->
  <circle cx="420" cy="380" r="60" fill="#f97316"/>
  <text x="420" y="410" font-family="Arial, sans-serif" font-size="60" font-weight="bold" fill="white" text-anchor="middle">€</text>
</svg>'''

# Schreibe SVG
svg_path = static_dir / 'icon.svg'
svg_path.write_text(svg_icon, encoding='utf-8')
print(f"\n✓ SVG Icon erstellt: {svg_path}")

# Hinweis für PNG-Konvertierung
print("\n" + "=" * 70)
print("PNG ICONS ERSTELLEN")
print("=" * 70)
print("\nDu hast 2 Optionen:")
print("\n1. AUTOMATISCH (empfohlen):")
print("   pip install pillow cairosvg")
print("   Dann dieses Skript nochmal ausführen")
print("\n2. MANUELL:")
print("   - Öffne icon.svg in einem Browser")
print("   - Screenshot machen")
print("   - Auf 512x512 skalieren → icon-512.png")
print("   - Auf 192x192 skalieren → icon-192.png")
print("   - In C:\\Kassenbons\\static\\ speichern")

# Versuche PIL + cairosvg zu nutzen falls installiert
try:
    from PIL import Image
    import cairosvg
    import io
    
    print("\n✓ PIL & cairosvg gefunden - erstelle PNG-Icons...")
    
    # 512x512
    png_512 = cairosvg.svg2png(bytestring=svg_icon.encode('utf-8'), 
                                output_width=512, output_height=512)
    with open(static_dir / 'icon-512.png', 'wb') as f:
        f.write(png_512)
    print("✓ icon-512.png erstellt")
    
    # 192x192
    png_192 = cairosvg.svg2png(bytestring=svg_icon.encode('utf-8'), 
                                output_width=192, output_height=192)
    with open(static_dir / 'icon-192.png', 'wb') as f:
        f.write(png_192)
    print("✓ icon-192.png erstellt")
    
    print("\n" + "=" * 70)
    print("✓ ALLE ICONS ERFOLGREICH ERSTELLT!")
    print("=" * 70)
    
except ImportError:
    print("\n⚠ PIL oder cairosvg nicht installiert")
    print("   Verwende manuelle Methode (siehe oben)")
    print("\nODER installiere:")
    print("   pip install pillow cairosvg")

print()
