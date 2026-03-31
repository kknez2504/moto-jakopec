"""
Sinkronizira models.json s stvarnim slikama na disku.

Pokreni: py -X utf8 scripts/sync_images.py

Što radi:
  - Za svaki model u models.json čita stvarne slike iz public/images/vozila/{folder}/
  - Sortira ih numerički (img_01, img_02, ... = već ispravan redoslijed)
  - Ažurira images[] polje u models.json
  - Ispisuje što je promijenjeno
"""

import json, os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.join(SCRIPT_DIR, "..")
JSON_PATH  = os.path.join(ROOT_DIR, "src", "data", "models.json")
IMG_DIR    = os.path.join(ROOT_DIR, "public", "images", "vozila")

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def natural_sort_key(s):
    """Sortira img_01, img_02, ..., img_10 numerički (ne leksikografski)."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]


def get_images_from_disk(folder: str) -> list:
    if not folder:
        return []
    folder_path = os.path.join(IMG_DIR, folder)
    if not os.path.isdir(folder_path):
        return []
    files = [f for f in os.listdir(folder_path)
             if os.path.splitext(f)[1].lower() in IMG_EXTS]
    files.sort(key=natural_sort_key)
    return [f"/images/vozila/{folder}/{f}" for f in files]


def main():
    with open(JSON_PATH, encoding="utf-8") as f:
        models = json.load(f)

    changed = 0
    missing_folders = []

    for m in models:
        # Izvuci folder iz postojećih slika
        # Nova struktura: /images/vozila/01-ninja-h2r/img_01.jpg → parts[3]
        folder = ""
        existing = m.get("images", [])
        if existing:
            parts = existing[0].split("/")
            # /images/vozila/FOLDER/file.jpg → index 3
            if len(parts) >= 4 and parts[2] == "vozila":
                folder = parts[3]
            # Stara struktura /images/FOLDER/file.jpg → index 2
            elif len(parts) >= 3:
                folder = parts[2]

        if not folder:
            missing_folders.append(m.get("name", "???"))
            continue

        new_images = get_images_from_disk(folder)

        if not os.path.isdir(os.path.join(IMG_DIR, folder)):
            print(f"  NEMA MAPE: {m['name']} -> {folder}")
            missing_folders.append(m.get("name", "???"))
            continue

        if new_images != existing:
            diff = len(new_images) - len(existing)
            sign = f"+{diff}" if diff > 0 else str(diff)
            print(f"  Ažurirano: {m['name']:<45} {len(existing):>3} → {len(new_images):>3} slika ({sign})")
            m["images"] = new_images
            changed += 1

    # Spremi
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(models, f, ensure_ascii=False, indent=2)

    print()
    print(f"Ažurirano modela: {changed}")
    print(f"Ukupno vozila:    {len(models)}")

    if missing_folders:
        print(f"\nBez mape ({len(missing_folders)}):")
        for name in missing_folders:
            print(f"  - {name}")

    # Provjeri nekorištene mape
    # Nova struktura: /images/vozila/FOLDER/file.jpg → parts[3]
    used_folders = set()
    for m in models:
        for img in m.get("images", []):
            parts = img.split("/")
            if len(parts) >= 4 and parts[2] == "vozila":
                used_folders.add(parts[3])
            elif len(parts) >= 3:
                used_folders.add(parts[2])

    all_folders = set(os.listdir(IMG_DIR))
    unused = sorted(all_folders - used_folders)
    if unused:
        print(f"\nNekorištene mape ({len(unused)}) — možeš obrisati ručno:")
        for u in unused:
            path = os.path.join(IMG_DIR, u)
            num_files = len(os.listdir(path))
            print(f"  - {u}  ({num_files} slika)")

    print("\nZavršeno. Ažuriraj Excel: py -X utf8 scripts/vozila_json_to_excel.py")


if __name__ == "__main__":
    main()
