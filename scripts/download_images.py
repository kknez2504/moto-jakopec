"""
Preuzima sve slike s kawasaki.eu lokalno u /public/images/[id]/
i updatea models.json s lokalnim putanjama.

Pokreni: py -X utf8 scripts/download_images.py
"""

import json
import re
import urllib.request
import urllib.parse
import os
import time

BASE_EU = "https://www.kawasaki.eu"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.join(SCRIPT_DIR, "..")
JSON_PATH  = os.path.join(ROOT_DIR, "src", "data", "models.json")
IMG_DIR    = os.path.join(ROOT_DIR, "public", "images")


def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"    GRESKA fetch: {e}")
        return None


def extract_all_images(html):
    """Vraca listu unikatnih 1280x1280 URL-ova (bez duplikata jcr/_jcr)."""
    if not html:
        return []
    imgs = re.findall(r'/content/dam/products/pim/studio/[^\s"\'<>]+\.(?:jpg|jpeg|png)', html)
    # Filtriraj samo 1280 rezoluciju
    imgs_1280 = [i for i in imgs if "1280.1280" in i]
    # Deduplikacija po base resource imenu (Resource_XXXXX_...)
    seen_bases = set()
    unique = []
    for img in imgs_1280:
        # Izvuci base ime (npr. Resource_320196_26ZR900S_40TGY1DRF3CG_A.jpg)
        match = re.search(r'(/content/dam/products/pim/studio/[^/]+\.(?:jpg|jpeg|png))', img)
        if match:
            base = match.group(1)
            if base not in seen_bases:
                seen_bases.add(base)
                # Koristi jcr:content varijantu (bez podcrte)
                unique.append(BASE_EU + base + "/jcr:content/renditions/cq5dam.web.1280.1280.png")
    return unique


def download_image(url, dest_path):
    """Preuzima sliku na dest_path. Vraca True ako uspije."""
    if os.path.exists(dest_path):
        return True  # Vec preuzeto
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        with open(dest_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"    GRESKA download ({os.path.basename(dest_path)}): {e}")
        return False


def safe_folder_name(model_name):
    """Pretvara ime modela u sigurno ime foldera."""
    name = model_name.replace("Kawasaki ", "")
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '-', name.strip())
    return name.lower()


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        models = json.load(f)

    os.makedirs(IMG_DIR, exist_ok=True)

    page_cache = {}  # kawasaki.eu path -> html
    total_downloaded = 0

    for model in models:
        mid = model["id"]
        name = model["name"]
        print(f"\n[{mid:02d}/{len(models)}] {name}")

        # Treba nam kawasaki.eu URL - procitaj iz postojecih images ili ga izgradi
        # Koristimo stare remote URL-ove ako postoje
        remote_images = [img for img in model.get("images", []) if img.startswith("http")]

        if not remote_images:
            print("    Nema remote URL-ova, preskacemo")
            continue

        # Izvuci path iz prvog remote URL-a da dobijemo stranicu modela
        # npr. https://www.kawasaki.eu/content/dam/... -> trebamo page URL
        # Koristimo folder name za lokalnu pohranu
        folder_name = f"{mid:02d}-{safe_folder_name(name)}"
        model_img_dir = os.path.join(IMG_DIR, folder_name)
        os.makedirs(model_img_dir, exist_ok=True)

        # Pokusaj naci page URL iz build_models.py podataka u models.json
        # Ako ne moze, koristi samo onu jednu sliku koju vec imamo
        page_url = None
        for img_url in remote_images:
            # Resource URL pattern: /content/dam/products/pim/studio/Resource_XXXXX_YYZZZZZZ...
            # Iz koda znacajke modela mozemo rekonstruirati page URL
            pass

        # Pokusaj dohvatiti stranicu za vise slika
        # Provjeri je li vec u cachou
        # Inace, skini HTML i izvuci sve slike
        first_remote = remote_images[0]

        # Izvuci resource ime iz URL-a
        resource_match = re.search(r'Resource_\d+_(\w+)_', first_remote)
        if not resource_match:
            # Fallback: preuzmi samo onu jednu sliku
            local_images = []
            filename = f"image_01.png"
            dest = os.path.join(model_img_dir, filename)
            if download_image(first_remote, dest):
                local_images.append(f"/images/{folder_name}/{filename}")
                total_downloaded += 1
            model["images"] = local_images
            print(f"    1 slika preuzeta (fallback)")
            continue

        # Dohvati HTML stranice za ovaj model da nadjemo sve slike
        # Koristimo page_cache s kljucem = resource prefix
        resource_prefix = resource_match.group(1)[:6]  # npr. "26ZR90"

        # Nadji stranicu modela - procitaj iz build_models.py MODELS liste
        # Jednostavnije: direktno dohvati HTML i trazi sve slike
        # Koristimo URL koji smo vec imali: iz remote images path izvucemo page URL

        # Alternativno: fetch page na temelju remote image URL-a
        # Svaka slika ima formu: /content/dam/products/pim/studio/Resource_XXXXXX_YYMMMM...
        # Mapiramo YYMM na page URL - ovo je komplicirano
        # Najlakse: sacuvaj page URL u models.json tokom build_models.py

        # Privremeno rjesenje: preuzmi sliku direktno iz remote_images
        local_images = []
        for i, img_url in enumerate(remote_images[:6], 1):
            filename = f"image_{i:02d}.png"
            dest = os.path.join(model_img_dir, filename)
            if download_image(img_url, dest):
                local_images.append(f"/images/{folder_name}/{filename}")
                total_downloaded += 1
                time.sleep(0.1)

        model["images"] = local_images
        print(f"    {len(local_images)} slika preuzeto")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(models, f, ensure_ascii=False, indent=2)

    print(f"\nGotovo! Preuzeto {total_downloaded} slika ukupno.")
    print("Sljedeci korak: git add . && git commit -m 'Download images locally' && git push")


if __name__ == "__main__":
    main()
