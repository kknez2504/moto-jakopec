"""
DKS.si Kawasaki cjenik scraper
================================
Scrape: https://www.dks.si/html_levo/cenik/Cenik_motorji_SLO.html
Output: src/data/models.json  (kompatibilno s Next.js projektom)

Instalacija:
    pip install requests beautifulsoup4 lxml

Pokretanje:
    python scripts/dks_scraper.py
    python scripts/dks_scraper.py --merge   # spaja s postojećim models.json
"""

import json
import re
import argparse
from pathlib import Path
import requests
from bs4 import BeautifulSoup

PRICE_LIST_URL = "https://www.dks.si/html_levo/cenik/Cenik_motorji_SLO.html"
DATA_FILE      = Path(__file__).parent.parent / "src" / "data" / "models.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

CATEGORY_MAP = {
    "supersport":        "Sport",
    "street & tourer":   "Touring",
    "supernaked":        "Naked",
    "modern classic":    "Classic",
    "urban cruiser":     "Cruiser",
    "adventure tourer":  "Adventure",
    "enduro":            "Offroad",
    "motocross":         "Offroad",
}


def clean_price(raw: str) -> str:
    raw = raw.strip().replace("\xa0", " ").replace("\n", "").replace("\r", "")
    if not raw or raw == "-":
        return "Cijena na upit"
    digits = re.sub(r"[^\d.,]", "", raw)
    if not digits:
        return "Cijena na upit"
    return digits + " €"


def detect_category(text: str) -> str | None:
    lower = text.lower().strip()
    for key, cat in CATEGORY_MAP.items():
        if key in lower:
            return cat
    return None


def scrape() -> list[dict]:
    print(f"Dohvaćam: {PRICE_LIST_URL}")
    try:
        r = requests.get(PRICE_LIST_URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except requests.RequestException as e:
        print(f"GREŠKA: {e}")
        return []

    print(f"Status: {r.status_code} | Veličina: {len(r.text)} znakova")

    soup = BeautifulSoup(r.text, "lxml")
    models: list[dict] = []
    current_category = "Ostalo"
    model_id = 1

    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue

            first_text = cells[0].get_text(strip=True)

            # Provjeri je li zaglavlje kategorije
            cat = detect_category(first_text)
            if cat:
                current_category = cat
                continue

            # Preskoči redove s manje od 3 ćelije i zaglavlja
            if len(cells) < 3 or not first_text or first_text.lower() in ("model", "naziv", "tip", ""):
                continue

            # Cijene: zadnje 3 ćelije su 2024, 2025, 2026
            price_cells = [cells[i].get_text(strip=True) for i in range(-3, 0) if len(cells) >= abs(i)]
            price_2024 = clean_price(price_cells[0]) if len(price_cells) > 0 else "Cijena na upit"
            price_2025 = clean_price(price_cells[1]) if len(price_cells) > 1 else "Cijena na upit"
            price_2026 = clean_price(price_cells[2]) if len(price_cells) > 2 else "Cijena na upit"

            # Koristi najnoviju dostupnu cijenu
            price = next(
                (p for p in [price_2026, price_2025, price_2024] if p != "Cijena na upit"),
                "Cijena na upit",
            )

            # Licencna kategorija iz naziva
            license_cat = ""
            for lc in ("A1", "A2"):
                if lc in first_text:
                    license_cat = lc
                    break

            # Novi model = zelena boja u stilu
            is_new = bool(
                row.find(style=re.compile(r"color\s*:\s*(green|#0+|lime)", re.I))
            )

            models.append({
                "id":               model_id,
                "name":             f"Kawasaki {first_text}",
                "brand":            "Kawasaki",
                "category":         current_category,
                "purpose":          current_category,
                "license_category": license_cat,
                "is_new":           is_new,
                "description":      f"Kawasaki {first_text} — {current_category}",
                "price":            price,
                "price_2024":       price_2024,
                "price_2025":       price_2025,
                "price_2026":       price_2026,
                "images":           [],
                "specs":            {},
            })
            model_id += 1

    return models


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def merge_into_existing(scraped: list[dict]) -> list[dict]:
    """Ažurira cijene u postojećem models.json, čuva sve ostale podatke."""
    if not DATA_FILE.exists():
        print("models.json ne postoji — kreiram novi.")
        return scraped

    with open(DATA_FILE, encoding="utf-8") as f:
        existing = json.load(f)

    lookup = {normalize(s["name"]): s for s in scraped}
    updated = 0

    for m in existing:
        key = normalize(m["name"])
        match = lookup.get(key)

        if not match:
            # Pokušaj partial match
            for k, v in lookup.items():
                if key in k or k in key:
                    match = v
                    break

        if match:
            if m.get("price") in ("", "Cijena na upit", None):
                m["price"] = match["price"]
            m["price_2024"] = match.get("price_2024", "")
            m["price_2025"] = match.get("price_2025", "")
            m["price_2026"] = match.get("price_2026", "")
            updated += 1

    print(f"Ažurirano cijena: {updated}/{len(existing)}")
    return existing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--merge", action="store_true",
        help="Spoji scraped podatke s postojećim models.json (čuva slike i specs)"
    )
    args = parser.parse_args()

    scraped = scrape()

    if not scraped:
        print("\nNisu pronađeni modeli.")
        debug = Path("dks_debug.html")
        print(f"Provjeri {debug} za detalje.")
        return

    print(f"\nPronađeno modela: {len(scraped)}")

    if args.merge:
        result = merge_into_existing(scraped)
    else:
        result = scraped

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Spremljeno u: {DATA_FILE}")
    print("\nPreview (prvih 3):")
    for m in result[:3]:
        print(f"  [{m['category']:10}] {m['name']:40} {m['price']}")


if __name__ == "__main__":
    main()
