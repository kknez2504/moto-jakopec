"""
Scraper koji povlači slike motocikala s kawasaki.eu i updatea models.json
Pokreni: python scripts/fetch_images.py
"""

import json
import re
import urllib.request
import urllib.error
import time
import os

# Mapa: ime modela (iz models.json) -> URL stranice na kawasaki.eu
MODEL_URLS = {
    "Kawasaki Ninja ZX-10R":    "https://www.kawasaki.eu/en/Motorcycles/Supersport_Sport/Ninja_ZX-10R_2026.html",
    "Kawasaki Z900":            "https://www.kawasaki.eu/en/Motorcycles/Supernaked/Z900_2026.html",
    "Kawasaki Versys 1000 SE":  "https://www.kawasaki.eu/en/Motorcycles/Adventure_Tourer/Versys_1100_se_2026.html",
    "Kawasaki Z650RS":          "https://www.kawasaki.eu/en/Motorcycles/Retro_Sport/Z650RS_2026.html",
    "Kawasaki KLX 300":         "https://www.kawasaki.eu/en/Motorcycles/Motocross-Enduro/KLX300R_2026.html",
    "Kawasaki Ninja 400":       "https://www.kawasaki.eu/en/Motorcycles/Supersport_Sport/Ninja_500_2026.html",
    "Kawasaki Z400":            "https://www.kawasaki.eu/en/Motorcycles/Supernaked/Z500_2026.html",
    "Kawasaki Versys 650":      "https://www.kawasaki.eu/en/Motorcycles/Adventure_Tourer/Versys_650_2026.html",
    "Kawasaki Vulcan S":        "https://www.kawasaki.eu/en/Motorcycles/Urban_Cruiser/vulcan_s_2026.html",
    "Kawasaki Ninja H2 SX SE":  "https://www.kawasaki.eu/en/Motorcycles/Sport_Tourer/Ninja_H2_SX_SE_2026.html",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_og_image(url):
    """Povlači og:image meta tag s Kawasaki stranice."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # Traži og:image
        match = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
        if match:
            return match.group(1)

        # Fallback: traži prvu /content/dam/ sliku
        match = re.search(r'(https://www\.kawasaki\.eu/content/dam/[^\s"\']+\.(?:jpg|jpeg|png|webp))', html)
        if match:
            return match.group(1)

        return None
    except Exception as e:
        print(f"  GREŠKA: {e}")
        return None


def main():
    # Učitaj models.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "..", "src", "data", "models.json")

    with open(json_path, "r", encoding="utf-8") as f:
        models = json.load(f)

    updated = 0
    for model in models:
        name = model["name"]
        url = MODEL_URLS.get(name)

        if not url:
            print(f"[PRESKAČEM] {name} — nema URL u mapi")
            continue

        print(f"[FETCH] {name}")
        print(f"        {url}")

        image_url = fetch_og_image(url)

        if image_url:
            model["images"] = [image_url]
            print(f"  ✓ Slika: {image_url[:80]}...")
            updated += 1
        else:
            print(f"  ✗ Slika nije pronađena")

        time.sleep(0.5)  # pauza između zahtjeva

    # Spremi ažurirani models.json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(models, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Gotovo! Ažurirano {updated}/{len(models)} modela.")
    print(f"  Spremi promjene: git add . && git commit -m 'Add motorcycle images' && git push")


if __name__ == "__main__":
    main()
