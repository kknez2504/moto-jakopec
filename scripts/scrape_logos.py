"""
Scrapa logoe s official web stranica brendova i sprema ih u:
    public/images/brendovi/{brand_id}.svg  (ili .png)

Pokreni jednom:
    py -X utf8 scripts/scrape_logos.py
"""

import os, re, time, urllib.parse, urllib.request
import requests
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.join(SCRIPT_DIR, "..")
OUT_DIR    = os.path.join(ROOT_DIR, "public", "images", "brendovi")
os.makedirs(OUT_DIR, exist_ok=True)

BRANDS = [
    ("wind",      "https://www.wind-raceware.com"),
    ("airoh",     "https://www.airoh.com"),
    ("progrip",   "https://www.progrip.it"),
    ("mitas",     "https://www.mitas-moto.com"),
    ("motul",     "https://www.motul.com"),
    ("valvoline", "https://www.valvoline.com"),
    ("prox",      "https://www.pro-x.com"),
    ("wiseco",    "https://www.wiseco.com"),
    ("wrp",       "https://www.wrp-racing.com"),
    ("cht",       "https://www.cht-sprockets.com"),
    ("rk",        "https://www.rk-chain.com"),
    ("trw",       "https://www.trwaftermarket.com"),
    ("denso",     "https://www.denso.com"),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

IMG_EXTS = {".svg", ".png", ".jpg", ".jpeg", ".webp"}

# ── Pomočne funkcije ─────────────────────────────────────────────────────────

def is_image_url(url: str) -> bool:
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    return ext in IMG_EXTS

def is_svg_content(content: bytes) -> bool:
    return content.strip().startswith(b"<svg") or b"<svg " in content[:500]

def make_abs(url: str, base: str) -> str:
    return urllib.parse.urljoin(base, url)

def download(url: str, session: requests.Session) -> bytes | None:
    try:
        r = session.get(url, timeout=15, headers=HEADERS, allow_redirects=True)
        if r.status_code == 200:
            return r.content
    except Exception as e:
        print(f"    ↳ download error {url}: {e}")
    return None

def ext_for(url: str, content: bytes) -> str:
    """Vrati ispravnu ekstenziju za sadržaj."""
    if is_svg_content(content):
        return ".svg"
    url_ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    return url_ext if url_ext in IMG_EXTS else ".png"

def save(brand_id: str, ext: str, content: bytes) -> str:
    """Spremi fajl, vrati putanju."""
    # Ukloni stare verzije
    for old_ext in IMG_EXTS:
        old = os.path.join(OUT_DIR, f"{brand_id}{old_ext}")
        if os.path.exists(old):
            os.remove(old)
    path = os.path.join(OUT_DIR, f"{brand_id}{ext}")
    with open(path, "wb") as f:
        f.write(content)
    return path

# ── Strategije pronalaska loga ────────────────────────────────────────────────

def find_logo_candidates(soup: BeautifulSoup, base_url: str) -> list[str]:
    """Vrati listu URL-ova kandidata za logo, sortirano po prioritetu."""
    candidates = []

    # 1. <img> ili <a> koji SADRŽE 'logo' u src/href/class/id unutar <header> ili <nav>
    for tag in soup.find_all(["header", "nav", "div"], limit=10):
        cls = " ".join(tag.get("class", []))
        if not any(k in cls.lower() for k in ("header", "nav", "top", "brand", "logo", "site")):
            continue
        for img in tag.find_all("img"):
            src = img.get("src", "") or img.get("data-src", "")
            alt = img.get("alt", "")
            cl  = " ".join(img.get("class", []))
            if any(k in (src + alt + cl).lower() for k in ("logo", "brand", "identity")):
                if src:
                    candidates.append(make_abs(src, base_url))

    # 2. Bilo koji <img> s 'logo' u src/alt/class na stranici
    for img in soup.find_all("img"):
        src = img.get("src", "") or img.get("data-src", "")
        alt = img.get("alt", "")
        cl  = " ".join(img.get("class", []))
        if src and any(k in (src + alt + cl).lower() for k in ("logo", "brand")):
            url = make_abs(src, base_url)
            if url not in candidates:
                candidates.append(url)

    # 3. <link rel="apple-touch-icon"> — bolja rezolucija od favicona
    for link in soup.find_all("link", rel=lambda r: r and "apple-touch-icon" in r):
        href = link.get("href")
        if href:
            candidates.append(make_abs(href, base_url))

    # 4. Favicon kao zadnji fallback
    for link in soup.find_all("link", rel=lambda r: r and any(x in r for x in ("icon", "shortcut"))):
        href = link.get("href")
        if href and "favicon" in href.lower():
            candidates.append(make_abs(href, base_url))

    # Filtriraj na samo slike
    return [c for c in candidates if is_image_url(c)]

# ── Scraping po brendu ────────────────────────────────────────────────────────

def scrape_brand(brand_id: str, base_url: str, session: requests.Session) -> bool:
    print(f"\n[{brand_id}] {base_url}")
    try:
        r = session.get(base_url, timeout=20, headers=HEADERS, allow_redirects=True)
        r.raise_for_status()
    except Exception as e:
        print(f"  GREŠKA dohvat stranice: {e}")
        return False

    soup = BeautifulSoup(r.text, "lxml")
    candidates = find_logo_candidates(soup, r.url)

    if not candidates:
        print(f"  Nema kandidata — ostaje placeholder SVG")
        return False

    print(f"  Kandidati ({len(candidates)}):")
    for c in candidates[:6]:
        print(f"    {c}")

    for url in candidates[:6]:
        content = download(url, session)
        if not content:
            continue
        # Preskoči premale fajlove (favicon <1 KB)
        if len(content) < 500:
            continue
        ext = ext_for(url, content)
        path = save(brand_id, ext, content)
        size_kb = len(content) / 1024
        print(f"  ✓ Spremenjen: {os.path.basename(path)} ({size_kb:.1f} KB)")
        return True

    print(f"  Nema upotrebljivog loga — ostaje placeholder SVG")
    return False

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    session = requests.Session()
    session.max_redirects = 5

    ok, failed = [], []
    for brand_id, url in BRANDS:
        success = scrape_brand(brand_id, url, session)
        (ok if success else failed).append(brand_id)
        time.sleep(1.5)   # pauza između zahtjeva

    print("\n" + "="*50)
    print(f"Uspješno:  {len(ok)} — {', '.join(ok)}")
    print(f"Neuspješno:{len(failed)} — {', '.join(failed)}")
    print(f"\nSvi fajlovi u: {OUT_DIR}")
    if failed:
        print("\nZa neuspješne brendove:")
        print("  Ručno preuzmi logo s web stranice i spremi kao:")
        for b in failed:
            print(f"    public/images/brendovi/{b}.svg  (ili .png)")

if __name__ == "__main__":
    main()
