#!/usr/bin/env python3
"""
Kassenbon-Analyse-App
Analysiert und klassifiziert Kassenbons aus PDF-Dateien
"""

import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import PyPDF2
from dataclasses import dataclass, asdict
import json

# Robustes Datum-Parsing (installieren: pip install dateparser)
try:
    import dateparser
    DATEPARSER_AVAILABLE = True
except ImportError:
    DATEPARSER_AVAILABLE = False
    print("⚠️ dateparser nicht installiert - Fallback auf Regex. Installiere mit: pip install dateparser")


@dataclass
class ReceiptItem:
    """Einzelner Artikel auf einem Kassenbon"""
    name: str
    unit_price: float
    quantity: int
    total_price: float
    tax_category: str  # A (7%) oder B (19%)
    category: str  # Getränke, Obst, etc.
    receipt_id: int = None
    item_id: int = None


@dataclass
class Receipt:
    """Kompletter Kassenbon"""
    receipt_id: int = None
    store_name: str = ""
    store_address: str = ""
    date: datetime = None
    total_amount: float = 0.0
    payment_method: str = ""
    items: List[ReceiptItem] = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []


class CategoryClassifier:
    """Klassifiziert Artikel in Kategorien mit Unterkategorien"""
    
    CATEGORIES = {
        # ═══ Garten & Pflanzen ═══ (ZUERST prüfen, damit nicht als Wein klassifiziert!)
        'Garten & Pflanzen': [
            r'rosen\b|rose\b|pflanze|blume|tulpe|nelke|chrysantheme',
            r'moos.*rose|stauden|gewaechs|gewächs|topf.*pflanzen',
            r'samen|saat|blumen.*erde|pflanzen.*erde',
        ],
        
        # ═══ Getränke ═══
        'Getränke - Wein': [
            # EINDEUTIGE Weintypen (mit Wortgrenzen!)
            r'\bwein\b|rotwein|weisswein|weißwein|rosewein|\brosé\b|\brosè\b',
            r'sekt\b|prosecco|champagner|cava\b',
            r'portwein|\bport\swein|dessertwein|eiswein|perlwein',
            # Weinvarianten / Restlinien (kein "wein"-Wort, trotzdem Wein)
            r'rotling|hausschopp|spätlese|spaetlese|auslese|kabinett',
            r'\bblut\b',  # "Franziskaner Blut" = Rotwein
            # Rebsorten
            r'riesling|silvaner|rivaner|dornfelder|chardonnay|merlot|cabernet',
            r'spätburg|spaetburg|grauburg|pinot\s|pinot\b',
            r'sauvignon|traminer|regent\b|auxerrois|kerner|bacchus|elbling|lemberger|trollinger',
            r'primitivo|tempranillo|sangiovese',  # Italienische/Spanische Sorten
            r'domina\b',  # Deutsche Rotweinsorte
            # Weinhersteller-Abkürzungen (sehr spezifisch)
            r'asth\.scheu|auxe\.rrois|mueller.*thurg|müller.*thurg',
            r'\bscheu\s|scheu\.|scheu\b',  # Scheurebe (nur wenn isoliert)
            # Wein-Brands (abgekürzt)
            r'augustiner.*silv|aug\..*silv',  # Augustiner Silvaner
            r'doppas',  # Doppas Weine
            # Wein-spezifische Zusätze (nur mit Wein-Kontext)
            r'barrique|cuvee|cuvée|trocken.*l\b|halbtrocken.*l\b',
            r'\blabel\s|\slabel\b|\.label',  # Label als Weinmarke (mit Kontext)
            # Weinregionen (NUR wenn + "wein" dabei)
            r'mosel.*wein|pfalz.*wein|rheingau.*wein',
        ],
        'Getränke - Bier': [
            r'bier|pils|weizen|loesch|lösch|export|alkoholfrei.*bier',
            r'hefeweizen|hefeweiss|weissbier|weißbier',  # Hefe-Bier nur explizit
            r'\bhell\b',  # Hell-Bier (z.B. Benediktiner Hell)
            r'radl|radler|rad\.',          # rad. = Radler-Abkürzung auf Kassenbons
            r'zwerg\s+rad',                # "ZWERG RAD." = Zwerg Radler
            # Bekannte Bier-Brands (abgekürzt auf Kassenbons)
            r'benediktiner|bened\.',
            r'gösser|goess|goell',  # Gösser = österreichisches Bier
            r'franziskaner.*weiss',  # Franziskaner Weißbier
        ],
        'Getränke - Softdrinks': [
            r'cola|limo|sprite|fanta|energy|limonade|mate|eistee',
            r'saft|schorle|nektar|fruchtsaft|multi|vitamin|trauben.*saft',
            r'tonic|bitter\s*lemon',  # Tonic Water, Bitter Lemon
            r'zitr|zitrone',  # Zitronenlimonade
            r'schweppes|schw\.',  # Schweppes (Brand)
        ],
        'Getränke - Wasser': [
            r'wasser|miwa|rhoen|rhön|mineral|naturtr|dest\.wasser|moen|medium|still|sprudel',
            r'gerolstein|volvic|vittel|evian|alasia',  # Alasia = Mineralwasser
        ],
        'Getränke - Sonstiges': [
            r'getraenk|getränk',  # Fallback für generische Getränke
        ],
        
        # ═══ Kaffee & Tee ═══
        'Kaffee & Tee - Kaffee': [
            r'kaffee|cafe|café|caffe|espresso|cappuccino|latte|mokka|moevenpick|mövenpick',
            r'bohnen.*kaffee|kaffee.*bohnen|kaffeepulver|instant.*kaffee',
            # Bekannte Kaffee-Brands (auch abgekürzt wie auf Kassenbons)
            r'lavaz|dallmayr|dalmayer|jacobs|tchibo|paulig|illycaffé|illy\b',
            r'prodomo|prodor|crema\s*crema|quali.*rossa',
        ],
        'Kaffee & Tee - Tee': [
            r'tee|earl.*grey|rooibos|kamille|pfefferminz|gruener.*tee|grüner.*tee',
            r'schwarztee|kraeuter.*tee|kräuter.*tee',
        ],
        
        # ═══ Obst & Gemüse ═══
        'Obst & Gemüse - Obst': [
            # Einzelne Obstsorten (MIT optionalem 'n' am Ende: orange/orangen)
            r'\borangen?\b|\baepfel\b|\bäpfel\b|\bapfel\b|\bbirnen?\b|\bbananen?\b',
            r'\btrauben?\b|\bweintrauben?\b|\bbrombeeren?\b|\bhimbeeren?\b|\berdbeeren?\b|\bbeeren?\b',
            r'\bkirschen?\b|\bpflaumen?\b|\bpfirsiche?\b|\baprikosen?\b',
            r'\bzitronen?\b|\bmandarinen?\b|\bclementinen?\b|\bkiwis?\b|\bmango',
            r'obst\b|frucht\b|bio.*obst',
        ],
        'Obst & Gemüse - Gemüse': [
            r'moehren|möhren|zwiebeln?|salat|gurken?|paprika|champignons?',
            r'kraeuter|kräuter|kartoffeln?|karotten|zucchini|aubergine',
            r'tomat|rispen|cherry|strauch|fleisch.*tomat|roma.*tomat',
            r'brokkoli|blumenkohl|rosenkohl|spinat|mangold|porree|lauch',
            r'gemuese|gemüse\b|bio.*gemuese|bio.*gemüse',
        ],
        'Obst & Gemüse - Sonstiges': [
            r'bio\s+frisch|regional\s+frisch',  # Nur mit Bio/Regional
            # "frisch" alleine wird absichtlich NICHT mehr gematcht – zu unspezifisch
        ],
        
        # ═══ Milchprodukte ═══
        'Milchprodukte - Milch': [
            r'\bmilch\b|vollmilch|fettarm.*milch|h-milch|frisch.*milch',
        ],
        'Milchprodukte - Joghurt & Quark': [
            r'joghurt|jogurt|jog\.halbfett|quark|skyr',
        ],
        'Milchprodukte - Käse': [
            r'kaese|käse|mozzarella|feta|gouda|emmentaler|camembert|frischkaese|frischkäse',
            r'scheiben.*kaese|scheiben.*käse|reibekaese|reibekäse',
            r'maasdamer|maasdam|edamer|tilsiter|appenzeller',  # Weitere Sorten
        ],
        'Milchprodukte - Butter & Sahne': [
            r'butter|sahne|creme|schmand|créme',
        ],
        
        # ═══ Fleisch & Wurst ═══
        'Fleisch & Wurst - Fleisch': [
            r'fleisch|steak|schnitzel|braten|filet|hackfleisch|hack\.?fleisch',
            r'geflügel|hähnchen|huhn|pute|rind|schwein|lamm',
        ],
        'Fleisch & Wurst - Wurst': [
            r'wurst|schinken|salami|leberwurst|mortadella|lyoner',
            r'kabanossi|kabanos',  # Polnische Wurst
            r'jausenstangerl|jausenwurst',  # Österreichische Wurst
        ],
        
        # ═══ Brot & Backwaren ═══
        'Brot & Backwaren - Brot': [
            r'\bbrot\b|vollkorn.*brot|weizen.*brot|roggen.*brot|toast|baguette',
        ],
        'Brot & Backwaren - Brötchen': [
            r'broetchen|brötchen|semmel|schrippe|weck',
        ],
        'Brot & Backwaren - Kuchen': [
            r'kuchen|torte|croissant|plaetzchen|plätzchen|keks',
        ],
        
        # ═══ Tiefkühl ═══
        'Tiefkühl - Fertiggerichte': [
            r'pizza.*tk|tk.*pizza|lasagne.*tk|tk.*lasagne',
        ],
        'Tiefkühl - Gemüse': [
            r'tk.*gemuese|tk.*gemüse|tiefk.*gemuese|tiefk.*gemüse',
        ],
        'Tiefkühl - Sonstiges': [
            r'pomm|frites|tiefk|tk-|tk\s|gefroren|eis\s',
            r'mccain',  # McCain = TK-Pommes Brand
        ],
        
        # ═══ Haushalt ═══
        'Haushalt & Reinigung - Reinigung': [
            r'reiniger|topfreiniger|spuelmittel|spülmittel|waschmittel',
            r'klarspueler|klarspül|geschirr.*tab|geschirr.*pulv|schwamm|tuecher|tücher',
            # Bekannte Haushalt-Brands
            r'softlan|persil|ariel|fairy|meister|domestos|cillit',
        ],
        'Haushalt & Reinigung - Papier': [
            r'papier|rolle|kuechen.*rolle|küchen.*rolle|toiletten.*papier|klopapier',
            r'taschentuecher|taschentücher|serviette',
        ],
        'Haushalt & Reinigung - Sonstiges': [
            r'auftausalz|backpapier|alufolie|frischhalte',
            r'co2\s*zylinder|co2.*patrone|filterkartu',   # CO2-Zylinder, Filterkartusche
        ],
        
        # ═══ Körperpflege & Pflege ═══
        'Körperpflege': [
            # Bekannte Pflege-Brands
            r'wellaflex|wella\b|head.*shoulders|pantene|garnier|schwarzkopf',
            r'frankens|nivea|beiersdorf|sebapharma',
            # Produkttypen
            r'haarspr|haarspray|shampoo|conditioner|schaum.*haar|haar.*schaum',
            r'duschgel|badewann|körperlotion|handcreme',
            r'zahnpasta|zahnbuerste|zahnbürste|mundspulung|mundspülung',
            r'parfüm|parfum|parfuem|cologne|eau\s+de',
            r'rasier|rasierer|rasierklinge',
            r'deodorant|deo\b',
        ],
        
        # ═══ Pasta & Nudeln ═══
        'Pasta & Nudeln': [
            # Produkttypen
            r'fusilli|penne|spaghetti|linguini|farfalle|rigatoni|girandole|tagliatelle',
            r'nudel|pasta\b|makkaroni|lasagne.*blätter|lasagne.*blatter',
            # Bekannte Pasta-Brands
            r'barilla|de\s*cecco|rana|müller.*ecke',
        ],
        
        # ═══ Küche & Kochen ═══
        'Küche & Kochen': [
            # Öle
            r'oel\b|öl\b|olivenöl|olivenoel|sonnenbl.*oel|sonnenbl.*öl|rapsöl|rapsoel',
            # Gewürze & Condiments
            r'gewürz|salz\b|pfeffer\b|paprika.*gewürz|curry|oregano|basilikum',
            r'ketchup|senf\b|mayonnaise|mayo\b|essig\b',
            # Mehl & Backzutaten
            r'mehl\b|zucker\b|vanille|backpulver|hefe\b',
            # Sauce & Tomatenprod.
            r'sosse|sauce\b|tomatensauce|passierte.*tom|tom.*passierten',
        ],
        
        # ═══ Konserven & Haltbares ═══
        'Konserven & Haltbares': [
            r'mais|konserve|dose|büchse|eingel|glas\b',
        ],
        
        # ═══ Sonstiges ═══
        'Sonstiges': [],
    }
    
    @classmethod
    def classify(cls, item_name: str) -> str:
        """Klassifiziert einen Artikel anhand des Namens"""
        item_lower = item_name.lower()
        
        # Pfand und Leergut ignorieren
        if any(keyword in item_lower for keyword in ['pfand', 'leergut', 'coupon']):
            return 'System'
        
        # NEGATIV-FILTER: Essig und Spirituosen sind KEIN Wein!
        # ABER: "Weintrauben" ist Obst, nicht Essig!
        essig_spirituosen = ['essig', 'cognac', 'whisky', 'rum', 'vodka', 'gin\b', 'tequila']
        # Weinbrand/Brandy nur wenn nicht "weintraube"
        if 'weintraube' not in item_lower and ('brandy' in item_lower or 'weinbrand' in item_lower):
            essig_spirituosen.append('match')
        
        if any(keyword in item_lower for keyword in essig_spirituosen):
            # Prüfe ob es trotzdem in andere Kategorien passt
            for category, patterns in cls.CATEGORIES.items():
                if 'Wein' in category or category == 'Sonstiges':
                    continue  # Überspringe Wein-Kategorien
                for pattern in patterns:
                    if re.search(pattern, item_lower):
                        return category
            return 'Sonstiges'
        
        # WICHTIG: Reihenfolge wird beibehalten (dict in Python 3.7+)
        for category, patterns in cls.CATEGORIES.items():
            if category == 'Sonstiges':
                continue
            for pattern in patterns:
                if re.search(pattern, item_lower):
                    return category
        
        return 'Sonstiges'


class ReceiptParser:
    """Parser für Kassenbon-PDFs"""
    
    def __init__(self):
        self.current_receipt = None
    
    def classify_item(self, item_name: str, categories: dict = None) -> str:
        """Klassifiziert einen Artikel mit den gegebenen Kategorien"""
        if categories is None:
            return CategoryClassifier.classify(item_name)
        
        item_lower = item_name.lower()
        
        # Pfand und Leergut ignorieren
        if any(keyword in item_lower for keyword in ['pfand', 'leergut', 'coupon']):
            return 'System'
        
        # Durchsuche alle Kategorien
        for category, keywords in categories.items():
            if not keywords:  # Leere Liste
                continue
                
            for keyword in keywords:
                if not keyword:  # Leerer String
                    continue
                    
                keyword_lower = keyword.lower()
                
                # EINFACHE SUBSTRING-SUCHE (funktioniert für 95% der Fälle)
                if keyword_lower in item_lower:
                    return category
        
        return 'Sonstiges'
    
    def parse_pdf(self, pdf_path: Path) -> Receipt:
        """Parst eine PDF-Datei und extrahiert Kassenbondaten"""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        return self._parse_text(text)
    
    def _parse_text(self, text: str) -> Receipt:
        """Extrahiert strukturierte Daten aus dem Kassenbon-Text"""
        receipt = Receipt()
        lines = text.split('\n')
        
        # Store-Info extrahieren
        receipt.store_name = self._extract_store_name(lines)
        receipt.store_address = self._extract_address(lines)
        
        # Datum extrahieren
        receipt.date = self._extract_date(text)
        
        # Artikel extrahieren
        receipt.items = self._extract_items(lines)
        
        # Gesamtbetrag extrahieren
        receipt.total_amount = self._extract_total(text)
        
        # Zahlungsmethode
        receipt.payment_method = self._extract_payment_method(text)
        
        return receipt
    
    # ── Bekannte Geschäfte: (Keyword im Text, Rückgabewert) ──
    KNOWN_STORES = [
        ('Kaufland',        'Kaufland'),
        ('KAUFLAND',        'Kaufland'),
        ('EDEKA',           'EDEKA'),
        ('FFFrische',       'FFFrische-Center'),
        ('Lidl',            'Lidl'),
        ('LIDL',            'Lidl'),
        ('Aldi',            'Aldi'),
        ('ALDI',            'Aldi'),
        ('DM ',             'dm'),
        ('dm-drogerie',     'dm'),
        ('DM-DROGERIE',     'dm'),
        ('Müller',          'Müller'),
        ('MUELLER',         'Müller'),
        ('REWE',            'REWE'),
        ('Rewe',            'REWE'),
        ('Penny',           'Penny'),
        ('PENNY',           'Penny'),
        ('Netto',           'Netto'),
        ('NETTO',           'Netto'),
        ('Norma',           'Norma'),
        ('NORMA',           'Norma'),
        ('Rossmann',        'Rossmann'),
        ('ROSSMANN',        'Rossmann'),
    ]

    # ── Zeilen die KEIN Geschäftsname sind ──
    SKIP_PATTERNS = [
        r'treuepunkte',
        r'du\s+hast',
        r'willkommen',
        r'thank',
        r'danke',
        r'^$',                          # Leerzeile
        r'^\s*$',                       # nur Leerzeichen
        r'preis\s+eur',                 # "Preis EUR" Spaltenheader
        r'tel\.',                       # Telefonnummer
        r'^\d{5}',                      # PLZ am Anfang
        r'straße\s+\d|str\.\s+\d',      # Straßenname mit Hausnummer (z.B. "Hauptbahnhofstraße 4")
        r'\d+\s+\w+straße',             # Variante: "4 Hauptbahnhofstraße"
        r'platz\s+\d',                  # Platzname mit Nummer
    ]

    def _extract_store_name(self, lines: List[str]) -> str:
        """Extrahiert den Geschäftsnamen – prüft bekannte Stores, filtert Treuepunkte etc."""
        # PASS 1 – bekannte Geschäftsnamen in den ersten 15 Zeilen suchen
        for line in lines[:15]:
            for keyword, name in self.KNOWN_STORES:
                if keyword in line:
                    return name

        # PASS 2 – Fallback: erste Zeile die kein Skip-Pattern ist
        for line in lines[:10]:
            stripped = line.strip()
            if not stripped:
                continue
            skip = False
            for pat in self.SKIP_PATTERNS:
                if re.search(pat, stripped, re.IGNORECASE):
                    skip = True
                    break
            if not skip:
                return stripped

        return "Unbekannt"
    
    def _extract_address(self, lines: List[str]) -> str:
        """Extrahiert die Adresse"""
        address_lines = []
        for line in lines[1:5]:
            if re.search(r'\d{5}|straße|str\.|platz', line, re.IGNORECASE):
                address_lines.append(line.strip())
        return ', '.join(address_lines) if address_lines else ""
    
    def _extract_date(self, text: str) -> Optional[datetime]:
        """Extrahiert das Datum - robust mit dateparser + Regex-Fallback"""
        
        # PASS 1: dateparser (falls installiert) - erkennt viele Formate automatisch
        if DATEPARSER_AVAILABLE:
            # Extrahiere Datum-ähnliche Zeilen (z.B. "29.1.2026 · 16:59")
            date_candidates = re.findall(r'\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4}[^\n]{0,20}', text)
            
            for candidate in date_candidates:
                parsed = dateparser.parse(
                    candidate,
                    languages=['de', 'en'],
                    settings={
                        'PREFER_DAY_OF_MONTH': 'first',  # DD.MM.YYYY nicht MM.DD.YYYY
                        'PREFER_DATES_FROM': 'past',      # Kassenbons sind meist vergangene Daten
                        'RELATIVE_BASE': datetime.now(),
                    }
                )
                if parsed:
                    return parsed
        
        # PASS 2: Regex-Fallback (wie vorher) - DD.MM.YY HH:MM
        date_pattern = r'(\d{2})\.(\d{2})\.(\d{2})\s+(\d{2}):(\d{2})'
        match = re.search(date_pattern, text)
        if match:
            day, month, year, hour, minute = match.groups()
            year = f"20{year}"  # 26 -> 2026
            return datetime(int(year), int(month), int(day), int(hour), int(minute))
        
        # PASS 3: Noch flexibler - DD.MM.YYYY (ohne Zeit)
        date_pattern_no_time = r'(\d{2})\.(\d{2})\.(\d{4})'
        match = re.search(date_pattern_no_time, text)
        if match:
            day, month, year = match.groups()
            return datetime(int(year), int(month), int(day), 12, 0)  # Mittag als Default
        
        return None
    
    def _extract_items(self, lines: List[str]) -> List[ReceiptItem]:
        """Extrahiert alle Artikel"""
        items = []
        
        # Pattern für Artikel: NAME PREIS [€ x MENGE] GESAMT KATEGORIE
        # Flexibles Pattern das verschiedene Formate unterstützt:
        # - "ARTIKEL 1,23 B" (einfach)
        # - "ARTIKEL 1,23*B" (nicht rabattberechtigt)
        # - "ARTIKEL 1,23 € x 2 2,46 B" (mit Menge)
        # - "LEERGUT -1,75*B" (negativ)
        
        item_pattern = r'^([A-Z][A-ZÄÖÜ&\.\s\-\d,X]*?)\s+(-?\d+,\d{2})\s*(?:€\s*x\s*(\d+)\s+(-?\d+,\d{2}))?\s*\*?[AB]W?$'
        
        for line in lines:
            line = line.strip()
            
            # Ignoriere System-Zeilen
            if any(keyword in line for keyword in ['SUMME', 'MwSt', 'PAYBACK', 'Datum', 
                                                     'Posten:', '----', 'Coupon:', 
                                                     'Beleg', 'Es bediente']):
                continue
            
            match = re.match(item_pattern, line)
            if match:
                name, unit_price_str, quantity_str, total_price_str = match.groups()
                
                unit_price = float(unit_price_str.replace(',', '.'))
                total_price = float(total_price_str.replace(',', '.')) if total_price_str else unit_price
                quantity = int(quantity_str) if quantity_str else 1
                
                # Tax category aus der Zeile extrahieren (A oder B)
                tax_category = 'B'  # Default
                if ' A' in line or 'AW' in line:
                    tax_category = 'A'
                
                # Klassifiziere Artikel
                category = CategoryClassifier.classify(name)
                
                item = ReceiptItem(
                    name=name.strip(),
                    unit_price=unit_price,
                    quantity=quantity,
                    total_price=total_price,
                    tax_category=tax_category,
                    category=category
                )
                items.append(item)
        
        return items
    
    def _extract_total(self, text: str) -> float:
        """Extrahiert den Gesamtbetrag"""
        # Pattern-Varianten für verschiedene Kassenbon-Formate:
        # 1. "SUMME € 21,83"
        # 2. "Summe                   21,83"  (viel Leerzeichen, kein €)
        # 3. "SUMME EUR 21,83"
        # 4. "Kartenzahlung           21,83"  (Fallback für manche Läden)
        
        patterns = [
            r'summe\s+€?\s*(\d+,\d{2})',           # SUMME € 21,83 oder SUMME 21,83
            r'summe\s+eur\s+(\d+,\d{2})',          # SUMME EUR 21,83
            r'kartenzahlung\s+(\d+,\d{2})',        # Kartenzahlung 21,83
            r'gesamt\s*:?\s*(\d+,\d{2})',          # GESAMT: 21,83
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1).replace(',', '.'))
        
        return 0.0
    
    def _extract_payment_method(self, text: str) -> str:
        """Extrahiert die Zahlungsmethode"""
        if 'Mastercard' in text:
            return 'Mastercard'
        elif 'VISA' in text:
            return 'VISA'
        elif 'EC-Karte' in text or 'Girocard' in text:
            return 'EC-Karte'
        elif 'PAYBACK Kundenkarte' in text:
            return 'PAYBACK Punkte'
        elif 'BAR' in text or 'Bargeld' in text:
            return 'Bargeld'
        return 'Unbekannt'


class ReceiptDatabase:
    """Datenbank für Kassenbons und Preisverlauf"""
    
    def __init__(self, db_path: str = "receipts.db"):
        self.db_path = db_path
        self.conn = None
        self._init_database()
    
    def _init_database(self):
        """Erstellt die Datenbankstruktur"""
        # check_same_thread=False erlaubt Thread-übergreifende Nutzung
        # In Kombination mit Flask's g-Objekt ist dies sicher
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.conn.cursor()
        
        # ═══ PERFORMANCE: WAL-Mode aktivieren ═══
        # Write-Ahead Logging: schneller + parallele Lesezugriffe möglich
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")  # NORMAL ist schneller als FULL, aber sicher genug
        
        # Tabelle für Kassenbons
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT,
                store_address TEXT,
                date TIMESTAMP,
                total_amount REAL,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabelle für Artikel
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
        
        # Tabelle für Preisverlauf
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
        
        # Index für schnellere Suche
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_items_name 
            ON items(name)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_price_history_name 
            ON price_history(item_name)
        ''')
        
        # ═══ PERFORMANCE: Zusätzliche Indizes ═══
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_receipts_date ON receipts(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_category ON items(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_receipts_store ON receipts(store_name)')
        
        self.conn.commit()
    
    def save_receipt(self, receipt: Receipt) -> int:
        """Speichert einen Kassenbon in der Datenbank"""
        cursor = self.conn.cursor()
        
        # Speichere Kassenbon
        cursor.execute('''
            INSERT INTO receipts (store_name, store_address, date, total_amount, payment_method)
            VALUES (?, ?, ?, ?, ?)
        ''', (receipt.store_name, receipt.store_address, receipt.date, 
              receipt.total_amount, receipt.payment_method))
        
        receipt_id = cursor.lastrowid
        
        # Speichere Artikel
        for item in receipt.items:
            cursor.execute('''
                INSERT INTO items (receipt_id, name, unit_price, quantity, total_price, 
                                  tax_category, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (receipt_id, item.name, item.unit_price, item.quantity, 
                  item.total_price, item.tax_category, item.category))
            
            # Aktualisiere Preisverlauf
            try:
                cursor.execute('''
                    INSERT INTO price_history (item_name, price, date, store_name)
                    VALUES (?, ?, ?, ?)
                ''', (item.name, item.unit_price, receipt.date, receipt.store_name))
            except sqlite3.IntegrityError:
                # Eintrag existiert bereits
                pass
        
        self.conn.commit()
        return receipt_id
    
    def get_price_history(self, item_name: str) -> List[Dict]:
        """Ruft den Preisverlauf eines Artikels ab"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT item_name, price, date, store_name
            FROM price_history
            WHERE item_name LIKE ?
            ORDER BY date
        ''', (f'%{item_name}%',))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'item_name': row[0],
                'price': row[1],
                'date': row[2],
                'store_name': row[3]
            })
        return results
    
    def get_category_statistics(self) -> Dict[str, Dict]:
        """Statistiken pro Kategorie"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT category, 
                   COUNT(*) as count,
                   SUM(total_price) as total_spent,
                   AVG(unit_price) as avg_price
            FROM items
            WHERE category != 'System'
            GROUP BY category
            ORDER BY total_spent DESC
        ''')
        
        stats = {}
        for row in cursor.fetchall():
            stats[row[0]] = {
                'count': row[1],
                'total_spent': round(row[2], 2),
                'avg_price': round(row[3], 2)
            }
        return stats
    
    def get_shopping_history(self, limit: int = 10) -> List[Dict]:
        """Letzte Einkäufe"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT receipt_id, store_name, date, total_amount, payment_method
            FROM receipts
            ORDER BY date DESC
            LIMIT ?
        ''', (limit,))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'receipt_id': row[0],
                'store_name': row[1],
                'date': row[2],
                'total_amount': row[3],
                'payment_method': row[4]
            })
        return history
    
    def search_items(self, search_term: str) -> List[Dict]:
        """Sucht nach Artikeln"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT i.name, i.category, 
                   AVG(i.unit_price) as avg_price,
                   COUNT(*) as purchase_count
            FROM items i
            WHERE i.name LIKE ? AND i.category != 'System'
            GROUP BY i.name, i.category
            ORDER BY purchase_count DESC
        ''', (f'%{search_term}%',))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'name': row[0],
                'category': row[1],
                'avg_price': round(row[2], 2),
                'purchase_count': row[3]
            })
        return results
    
    def close(self):
        """Schließt die Datenbankverbindung"""
        if self.conn:
            self.conn.close()


class ReceiptAnalyzer:
    """Hauptklasse für die Kassenbon-Analyse"""
    
    def __init__(self, db_path: str = "receipts.db"):
        self.parser = ReceiptParser()
        self.db = ReceiptDatabase(db_path)
    
    def process_directory(self, directory: Path) -> int:
        """Verarbeitet alle PDFs in einem Verzeichnis"""
        pdf_files = list(directory.glob("*.pdf"))
        processed = 0
        
        for pdf_file in pdf_files:
            try:
                print(f"Verarbeite: {pdf_file.name}")
                receipt = self.parser.parse_pdf(pdf_file)
                self.db.save_receipt(receipt)
                processed += 1
                print(f"  ✓ {len(receipt.items)} Artikel gespeichert")
            except Exception as e:
                print(f"  ✗ Fehler: {e}")
        
        return processed
    
    def analyze(self):
        """Führt Analysen durch und zeigt Ergebnisse"""
        print("\n" + "="*60)
        print("KASSENBON-ANALYSE")
        print("="*60)
        
        # Kategoriestatistiken
        print("\n📊 Ausgaben nach Kategorie:")
        print("-" * 60)
        stats = self.db.get_category_statistics()
        for category, data in stats.items():
            print(f"{category:25s} {data['total_spent']:8.2f} € "
                  f"({data['count']} Artikel, ⌀ {data['avg_price']:.2f} €)")
        
        # Einkaufshistorie
        print("\n🛒 Letzte Einkäufe:")
        print("-" * 60)
        history = self.db.get_shopping_history(5)
        for h in history:
            date_str = h['date'][:16] if h['date'] else 'N/A'
            print(f"{date_str} | {h['store_name']:30s} | {h['total_amount']:7.2f} € | {h['payment_method']}")
    
    def show_price_trends(self, item_name: str):
        """Zeigt Preisentwicklung eines Artikels"""
        history = self.db.get_price_history(item_name)
        
        if not history:
            print(f"Keine Preisdaten für '{item_name}' gefunden.")
            return
        
        print(f"\n💰 Preisverlauf: {history[0]['item_name']}")
        print("-" * 60)
        
        for entry in history:
            date_str = entry['date'][:10] if entry['date'] else 'N/A'
            print(f"{date_str} | {entry['store_name']:30s} | {entry['price']:6.2f} €")
        
        # Preisänderung
        if len(history) > 1:
            first_price = history[0]['price']
            last_price = history[-1]['price']
            change = last_price - first_price
            change_pct = (change / first_price) * 100
            
            arrow = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            print(f"\n{arrow} Änderung: {change:+.2f} € ({change_pct:+.1f}%)")
    
    def close(self):
        """Schließt Ressourcen"""
        self.db.close()


def main():
    """Hauptfunktion"""
    import sys
    
    analyzer = ReceiptAnalyzer()
    
    # Verarbeite Verzeichnis wenn angegeben
    if len(sys.argv) > 1:
        directory = Path(sys.argv[1])
        if directory.exists():
            count = analyzer.process_directory(directory)
            print(f"\n✓ {count} Kassenbons erfolgreich verarbeitet!")
        else:
            print(f"Verzeichnis nicht gefunden: {directory}")
            sys.exit(1)
    
    # Zeige Analyse
    analyzer.analyze()
    
    # Beispiel: Preisverlauf
    print("\n" + "="*60)
    results = analyzer.db.search_items("SALAT")
    if results:
        analyzer.show_price_trends(results[0]['name'])
    
    analyzer.close()


if __name__ == "__main__":
    main()
