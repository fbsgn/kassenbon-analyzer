#!/usr/bin/env python3
"""
batch_import.py
───────────────
Verarbeitet alle PDFs aus dem Eingangsordner (C:\Kassenbons\PDF)
und legt sie nach Jahr/Monat sortiert in das Ablage-Verzeichnis ab.

Verzeichnisstruktur nach Verarbeitung:

    C:\Kassenbons\
    ├── PDF\                        ← Eingangsordner (hier werden neue PDFs abgelegt)
    ├── Ablage\                     ← Sortiertes Archiv
    │   ├── 2025\
    │   │   └── 08\
    │   │       └── Kassenbon_2025-08-01_Sczygiel_Pfrang.pdf
    │   └── 2026\
    │       └── 01\
    │           └── Kassenbon_2026-01-26_FFFrische-Center.pdf
    ├── Fehler\                     ← PDFs die nicht verarbeitet werden konnten
    ├── receipts.db
    ├── web_app_fixed.py
    └── receipt_analyzer.py
"""

import re
import shutil
import sqlite3
from pathlib import Path
from receipt_analyzer import ReceiptParser, Receipt


# ─── Pfade (relativ zum Skript-Ordner) ──────────────────────────────────────
BASE_DIR    = Path(__file__).parent.resolve()
EINGANG     = BASE_DIR / "PDF"
ABLAGE      = BASE_DIR / "Ablage"
FEHLER      = BASE_DIR / "Fehler"
DB_PATH     = BASE_DIR / "receipts.db"


# ─── Hilfsfunktionen ─────────────────────────────────────────────────────────

def ensure_dirs():
    """Erstellt Eingang / Ablage / Fehler falls nicht vorhanden."""
    for d in (EINGANG, ABLAGE, FEHLER):
        d.mkdir(parents=True, exist_ok=True)


def get_db() -> sqlite3.Connection:
    """Öffnet eine Verbindung zur Datenbank."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def is_duplicate(conn: sqlite3.Connection, receipt: Receipt) -> bool:
    """
    Prüft ob ein Kassenbon mit gleichem Geschäft + Datum + Betrag
    bereits in der Datenbank existiert.
    """
    if not receipt.date:
        return False
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM receipts WHERE store_name=? AND date=? AND total_amount=?",
        (receipt.store_name, receipt.date, receipt.total_amount)
    )
    return cur.fetchone() is not None


def save_to_db(conn: sqlite3.Connection, receipt: Receipt) -> int:
    """Speichert Kassenbon + Artikel + Preishistorie in die Datenbank."""
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO receipts (store_name, store_address, date, total_amount, payment_method) "
        "VALUES (?, ?, ?, ?, ?)",
        (receipt.store_name, receipt.store_address,
         receipt.date, receipt.total_amount, receipt.payment_method)
    )
    receipt_id = cur.lastrowid

    for item in receipt.items:
        cur.execute(
            "INSERT INTO items (receipt_id, name, unit_price, quantity, total_price, "
            "tax_category, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (receipt_id, item.name, item.unit_price, item.quantity,
             item.total_price, item.tax_category, item.category)
        )
        try:
            cur.execute(
                "INSERT INTO price_history (item_name, price, date, store_name) "
                "VALUES (?, ?, ?, ?)",
                (item.name, item.unit_price, receipt.date, receipt.store_name)
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    return receipt_id


def safe_name(text: str) -> str:
    """Bereinigt einen String für die Verwendung als Dateiname."""
    s = re.sub(r"[^\w\-\. ]", "_", text)
    s = re.sub(r"_+", "_", s).strip("_ ")
    return s


def target_path_for(receipt: Receipt) -> Path:
    """
    Gibt den vollständigen Zielpfad im Ablage-Ordner zurück und
    erstellt dabei die Unterverzeichnisse (Jahr / Monat) automatisch.

    Beispiel:  Ablage/2026/01/Kassenbon_2026-01-26_FFFrische-Center.pdf
    """
    if receipt.date:
        year     = receipt.date.strftime("%Y")
        month    = receipt.date.strftime("%m")
        date_str = receipt.date.strftime("%Y-%m-%d")
    else:
        year     = "Unbekannt"
        month    = "Unbekannt"
        date_str = "kein-Datum"

    ordner = ABLAGE / year / month
    ordner.mkdir(parents=True, exist_ok=True)

    dateiname = f"Kassenbon_{date_str}_{safe_name(receipt.store_name)}.pdf"
    return ordner / dateiname


def move_pdf(src: Path, dst: Path) -> Path:
    """
    Verschiebt eine PDF vom Eingang zum Ziel.
    Falls der Zielname bereits existiert, wird ein Suffix _2, _3 … angehängt.
    """
    if not dst.exists():
        shutil.move(str(src), str(dst))
        return dst

    counter = 2
    while True:
        candidate = dst.parent / f"{dst.stem}_{counter}{dst.suffix}"
        if not candidate.exists():
            shutil.move(str(src), str(candidate))
            return candidate
        counter += 1


# ─── Hauptlogik ──────────────────────────────────────────────────────────────

def process_pdf(pdf_path: Path, conn: sqlite3.Connection) -> dict:
    """
    Verarbeitet eine einzelne PDF.
    Gibt ein Status-Dict zurück: datei, status, nachricht, ziel
    """
    out = {"datei": pdf_path.name, "status": "", "nachricht": "", "ziel": ""}

    try:
        receipt = ReceiptParser().parse_pdf(pdf_path)

        # Duplikat?
        if is_duplicate(conn, receipt):
            out["status"] = "duplikat"
            date_txt = receipt.date.strftime("%d.%m.%Y") if receipt.date else "?"
            out["nachricht"] = (
                f"Bereits importiert – {receipt.store_name}, "
                f"{date_txt}, {receipt.total_amount:.2f} €"
            )
            ziel = move_pdf(pdf_path, target_path_for(receipt))
            out["ziel"] = str(ziel)
            return out

        # Neu → in DB speichern
        save_to_db(conn, receipt)

        # In Ablage verschieben
        ziel = move_pdf(pdf_path, target_path_for(receipt))
        out["status"] = "ok"
        date_txt = receipt.date.strftime("%d.%m.%Y") if receipt.date else "?"
        out["nachricht"] = (
            f"{receipt.store_name}, {date_txt}, "
            f"{receipt.total_amount:.2f} € – {len(receipt.items)} Artikel"
        )
        out["ziel"] = str(ziel)

    except Exception as exc:
        out["status"] = "fehler"
        out["nachricht"] = str(exc)
        try:
            shutil.move(str(pdf_path), str(FEHLER / pdf_path.name))
            out["ziel"] = str(FEHLER / pdf_path.name)
        except Exception:
            pass

    return out


def run_import() -> list:
    """
    Hauptfunktion: Verarbeitet alle PDFs im Eingangsordner.
    Gibt eine Liste von Ergebnis-Dicts zurück.
    Wird sowohl von der Flask-App als auch von der Kommandozeile aufgerufen.
    """
    ensure_dirs()

    pdfs = sorted(EINGANG.glob("*.pdf"))
    if not pdfs:
        return []

    conn    = get_db()
    results = []
    for pdf in pdfs:
        results.append(process_pdf(pdf, conn))
    conn.close()

    return results


# ─── Kommandozeilen-Einstieg ─────────────────────────────────────────────────
if __name__ == "__main__":
    print()
    print("=" * 68)
    print("  📦  KASSENBON BATCH-IMPORT")
    print("=" * 68)
    print(f"  Eingangsordner : {EINGANG}")
    print(f"  Ablageordner   : {ABLAGE}")
    print(f"  Fehlerordner   : {FEHLER}")
    print(f"  Datenbank      : {DB_PATH}")
    print("-" * 68)

    anzahl = len(list(EINGANG.glob("*.pdf")))
    print(f"  Gefundene PDFs : {anzahl}")

    if anzahl == 0:
        print()
        print(f"  📭  Keine PDFs zum Verarbeiten.")
        print(f"      Lege PDFs in: {EINGANG}")
    else:
        print()
        results = run_import()

        for r in results:
            icon = {"ok": "✅", "duplikat": "⏭️ ", "fehler": "❌"}.get(r["status"], "❓")
            print(f"  {icon}  {r['datei']}")
            print(f"       {r['nachricht']}")
            if r["ziel"]:
                print(f"       → {r['ziel']}")
            print()

        ok  = sum(1 for r in results if r["status"] == "ok")
        dup = sum(1 for r in results if r["status"] == "duplikat")
        err = sum(1 for r in results if r["status"] == "fehler")

        print("-" * 68)
        print(f"  ✅  Neu importiert    : {ok}")
        print(f"  ⏭️   Bereits vorhanden : {dup}")
        print(f"  ❌  Fehler            : {err}")
        print("=" * 68)

    print()
    input("  Drücke ENTER zum Beenden…")
