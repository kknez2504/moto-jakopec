"""
Generira kompletan models.json:
- Svi modeli i cijene s dks.si cjenika + offroad
- Slike i specifikacije povucene s kawasaki.eu

Pokreni: py -X utf8 scripts/build_models.py
"""

import json
import re
import urllib.request
import time
import os

BASE_EU = "https://www.kawasaki.eu"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Format: (id, name, category, license, is_new, price, opis, kawasaki_eu_path)
MODELS = [
    # SUPERSPORT
    (1,  "Ninja H2R",        "Sport",     "",   False, "59.438 €",
     "Najmoćniji serijski motocikl na svijetu. Supercharged motor od 310 KS, karbon karoserija i aerodinamički paketi za stazu.",
     "/en/Motorcycles/Hypersport/Ninja_H2R_2026.html"),
    (2,  "Ninja ZX-10RR",    "Sport",     "",   False, "30.609 €",
     "Homologirani superbike za stazu i cestu. Razvijen direktno iz WorldSBK iskustva s Ohlins ovjesom i Brembo kocnicama.",
     "/en/Motorcycles/Supersport_Sport/Ninja_ZX-10RR_2026.html"),
    (3,  "Ninja ZX-10R",     "Sport",     "",   False, "20.510 €",
     "Legendarni supersport s 200 KS. Bogata elektronika, IMU platforma i WorldSBK DNA u svakom detalju.",
     "/en/Motorcycles/Supersport_Sport/Ninja_ZX-10R_2026.html"),
    (4,  "Ninja ZX-6R",      "Sport",     "",   False, "13.689 €",
     "Ikonični 636cc supersport — agilan, zabavan i snažan. Savršen balans između staze i ceste.",
     "/en/Motorcycles/Supersport_Sport/Ninja_zx-6r_2026.html"),
    (5,  "Ninja ZX-4RR",     "Sport",     "A2", True,  "10.234 €",
     "4-cilindrični 400cc motor u A2 paketu. Maksimalan sport osjećaj uz ograničenje snage za A2 kategoriju.",
     "/en/Motorcycles/Supersport_Sport/Ninja_zx-4rr_2026.html"),
    (6,  "Ninja ZX-4R",      "Sport",     "A2", True,  "9.462 €",
     "Pristupačniji ulaz u 4-cilindrični sport segment. Pravi Ninja karakter u A2 paketu.",
     "/en/Motorcycles/Supersport_Sport/Ninja_zx-4r_2026.html"),

    # STREET & TOURER
    (7,  "Ninja H2SX SE",    "Touring",   "",   False, "30.386 €",
     "Supercharged sport-tourer s 200 KS. Elektronski ovjes, adaptivni farovi i touring oprema na najvišoj razini.",
     "/en/Motorcycles/Sport_Tourer/Ninja_H2_SX_SE_2026.html"),
    (8,  "Ninja H2SX",       "Touring",   "",   False, "27.511 €",
     "Supercharged touring s kompresiranim motorom i izvanrednim performansama za dugopružne ture.",
     "/en/Motorcycles/Sport_Tourer/Ninja_H2_SX_2026.html"),
    (9,  "Ninja 1100SX SE",  "Touring",   "",   True,  "16.409 €",
     "Sport-tourer sljedeće generacije. Elektronski ovjes, navigacija i sve što trebate za veliku turu.",
     "/en/Motorcycles/Sport_Tourer/Ninja_1100_SX_SE_2026.html"),
    (10, "Ninja 1100SX",     "Touring",   "",   True,  "14.750 €",
     "Moćan 1100cc sport-tourer s bogatom elektronikom i sportskim karakterom na dugim rutama.",
     "/en/Motorcycles/Sport_Tourer/Ninja_1100SX_2026.html"),
    (11, "Ninja 650 SE",     "Sport",     "",   False, "8.634 €",
     "Najpopularniji Kawasaki za svaki dan. Uravnotežen, zabavan i praktičan za početnike i iskusne vozače.",
     "/en/Motorcycles/Supersport_Sport/Ninja_650_2026.html"),
    (12, "Ninja 650",        "Sport",     "",   False, "8.449 €",
     "Klasična Ninja formula — dostupna cijena, jak karakter i svakodnevna upotrebljivost.",
     "/en/Motorcycles/Supersport_Sport/Ninja_650_2026.html"),
    (13, "Ninja 500 SE",     "Sport",     "A2", True,  "7.378 €",
     "Novi 500cc parallel-twin u modernom Ninja ruhu. Idealan za A2 kategoriju uz pravi sport izgled.",
     "/en/Motorcycles/Supersport_Sport/Ninja_500_se_2026.html"),
    (14, "Ninja 500",        "Sport",     "A2", True,  "6.857 €",
     "Pristupačni ulaz u Ninja seriju za A2 vozače. Moderan dizajn i pouzdan motor.",
     "/en/Motorcycles/Supersport_Sport/Ninja_500_2026.html"),
    (15, "Ninja 125 SE",     "Sport",     "A1", False, "5.665 €",
     "Pravi Ninja karakter u 125cc paketu za A1 kategoriju.",
     "/en/Motorcycles/Supersport_Sport/Ninja_125_2026.html"),
    (16, "Ninja 125",        "Sport",     "A1", False, "5.549 €",
     "125cc Ninja za početnike — pravi dizajn velikog brata uz pristupačnu kategoriju.",
     "/en/Motorcycles/Supersport_Sport/Ninja_125_2026.html"),

    # SUPERNAKED
    (17, "Z H2 SE",          "Naked",     "",   False, "21.940 €",
     "Supercharged naked — 200 KS bez karoserije. Najsnažniji naked Kawasaki s elektronskim ovjesom.",
     "/en/Motorcycles/Supernaked/Zh2_se_2026.html"),
    (18, "Z H2",             "Naked",     "",   False, "19.391 €",
     "Supercharged naked s kompresiranim motorom. Brutalna snaga u street paketu.",
     "/en/Motorcycles/Supernaked/Zh2_2026.html"),
    (19, "Z 1100 SE",        "Naked",     "",   True,  "13.533 €",
     "Novi flagship naked s 1100cc motorom. Agresivan dizajn i bogata elektronika nove generacije.",
     "/en/Motorcycles/Supernaked/Z1100_SE_2026.html"),
    (20, "Z 1100",           "Naked",     "",   True,  "11.863 €",
     "Mocan 1100cc naked street fighter. Nasljednik Z1000 s novim motorom i modernom elektronikom.",
     "/en/Motorcycles/Supernaked/z1100_2026.html"),
    (21, "Z 900 SE",         "Naked",     "",   False, "12.532 €",
     "Premium naked s elektronskim ovjesom i punom elektronikom. Z900 na najvišoj razini opreme.",
     "/en/Motorcycles/Supernaked/Z900_se_2026.html"),
    (22, "Z 900",            "Naked",     "",   False, "10.451 €",
     "Ikonični naked street fighter. Agresivan dizajn, 948cc motor i bogata elektronika.",
     "/en/Motorcycles/Supernaked/Z900_2026.html"),
    (23, "Z 650 S",          "Naked",     "",   True,  "7.910 €",
     "Novi Z650S s Sport paketom. Sportskiji položaj i osvježen dizajn za urbanu vožnju.",
     "/en/Motorcycles/Supernaked/Z650_S_2026.html"),
    (24, "Z 650",            "Naked",     "",   False, "7.812 €",
     "Lagan, agilni i pristupačni naked. Savršen za grad i vikend izlete.",
     "/en/Motorcycles/Supernaked/Z650_2026.html"),
    (25, "Z 125",            "Naked",     "A1", False, "5.187 €",
     "Kompaktni Z naked za A1 kategoriju. Pravi Z karakter u urbanom 125cc paketu.",
     "/en/Motorcycles/Supernaked/Z125_2026.html"),

    # MODERN CLASSIC
    (26, "Z 900RS SE",       "Classic",   "",   False, "14.055 €",
     "Premium retro s elektronskim ovjesom i zlatnim Ohlins amortizerom. Najluksuzniji retro Kawasaki.",
     "/en/Motorcycles/Retro_Sport/Z900RS_SE_2026.html"),
    (27, "Z 650RS SE",       "Classic",   "",   False, "8.441 €",
     "Retro dizajn inspiriran klasičnim Z-serijom iz 70-ih uz modernu tehnologiju i pouzdanost.",
     "/en/Motorcycles/Retro_Sport/Z650RS_2026.html"),
    (28, "W 800",            "Classic",   "",   False, "9.868 €",
     "Prava retro ikona s paralel-twin motorom i vremenski provjerenim dizajnom. Za ljubitelje klasike.",
     "/en/Motorcycles/Classic/w800_2025.html"),
    (29, "Meguro S1",        "Classic",   "A2", True,  "5.795 €",
     "Oživljeni Meguro brend u modernom paketu. Elegantni klasik s Kawasaki pouzdanošću.",
     "/en/Motorcycles/Classic/Meguro_s1_2026.html"),
    (30, "W 230",            "Classic",   "A2", True,  "5.168 €",
     "Moderan retro u pristupačnom 230cc paketu. Savršen za A2 vozace koji vole klasičan stil.",
     "/en/Motorcycles/Classic/W230_2026.html"),

    # URBAN CRUISER
    (31, "Vulcan S SE",      "Cruiser",   "",   False, "8.916 €",
     "Premium cruiser s ergonomski prilagodljivom pozicijom vožnje. Stil, udobnost i karakter.",
     "/en/Motorcycles/Urban_Cruiser/vulcan_s_2026.html"),
    (32, "Vulcan S",         "Cruiser",   "",   False, "8.593 €",
     "Moderni cruiser s adjustable ergonomijom. Za sve koji žele slobodu ceste uz komfor.",
     "/en/Motorcycles/Urban_Cruiser/vulcan_s_2026.html"),
    (33, "Eliminator 500 SE","Cruiser",   "A2", True,  "7.184 €",
     "Novi Eliminator u A2 paketu s SE opremom. Low-seat cruiser za svaki dan.",
     "/en/Motorcycles/Urban_Cruiser/eliminator_500_se_2026.html"),
    (34, "Eliminator 500",   "Cruiser",   "A2", True,  "6.785 €",
     "Moderni low-seat cruiser za A2 kategoriju. Pristupačan ulaz u cruiser segment.",
     "/en/Motorcycles/Urban_Cruiser/eliminator_500_2026.html"),

    # ADVENTURE TOURER
    (35, "Versys 1100 SE",   "Adventure", "",   False, "16.827 €",
     "Ultimativni adventure-tourer s elektronskim ovjesom i kompletnom touring opremom.",
     "/en/Motorcycles/Adventure_Tourer/Versys_1100_se_2026.html"),
    (36, "Versys 1100 S",    "Adventure", "",   False, "15.263 €",
     "Mocan 1100cc adventure-tourer. Sportski karakter i touring udobnost u jednom.",
     "/en/Motorcycles/Adventure_Tourer/Versys_1100_s_2026.html"),
    (37, "Versys 1100",      "Adventure", "",   False, "13.556 €",
     "Klasični Versys recept uz 1100cc snagu. Svestran, udoban i pouzdan za duge ture.",
     "/en/Motorcycles/Adventure_Tourer/versys-1100---2026.html"),
    (38, "Versys 650",       "Adventure", "",   True,  "8.937 €",
     "Najpristupačniji adventure-tourer. Udoban, svestran i ekonomičan za svakodnevnu vožnju.",
     "/en/Motorcycles/Adventure_Tourer/Versys_650_2026.html"),
    (39, "KLE 500 SE",       "Adventure", "A2", True,  "7.442 €",
     "Novi KLE500 SE — pravi mali adventure u A2 paketu s bogatom opremom.",
     "/en/Motorcycles/Adventure/KLE500_SE_2026.html"),
    (40, "KLE 500",          "Adventure", "A2", True,  "6.664 €",
     "Ulazni adventure motocikl za A2 kategoriju. Robusni dizajn i pouzdan motor.",
     "/en/Motorcycles/Adventure/KLE500_2026.html"),

    # OFFROAD / MOTOCROSS
    (41, "KX 450",           "Offroad",   "",   False, "Cijena na upit",
     "Vrhunski motocross natjecatelj. Razvijen za pobjedu na stazi s najnaprednijom tehnologijom.",
     "/en/Motorcycles/Motocross-Enduro/KX450_2026.html"),
    (42, "KX 450X",          "Offroad",   "",   False, "Cijena na upit",
     "Cross-country enduro verzija KX450 za dugotrajne off-road utrke i avanturu.",
     "/en/Motorcycles/Motocross-Enduro/KX450X_2026.html"),
    (43, "KX 250",           "Offroad",   "",   False, "Cijena na upit",
     "Profesionalni 250cc motocross. Lagan, brz i agresivan — za ozbiljne natjecatelje.",
     "/en/Motorcycles/Motocross-Enduro/KX250_2026.html"),
    (44, "KX 250X",          "Offroad",   "",   False, "Cijena na upit",
     "Cross-country enduro na bazi KX250. Za dugotrajne off-road avanture i natjecanja.",
     "/en/Motorcycles/Motocross-Enduro/KX250X_2026.html"),
    (45, "KX 112",           "Offroad",   "",   False, "Cijena na upit",
     "Novi 2-taktni motocross za mlake natjecatelje. Lagani i precizni — savršen za razvoj vještina.",
     "/en/Motorcycles/Motocross-Enduro/KX112_2026.html"),
    (46, "KX 85",            "Offroad",   "",   False, "Cijena na upit",
     "2-taktni junior motocross za mlade natjecatelje. Proven dizajn i pouzdanost za stazu.",
     "/en/Motorcycles/Motocross-Enduro/KX85_I_2026.html"),
    (47, "KX 65",            "Offroad",   "",   False, "Cijena na upit",
     "Motocross za najmlađe natjecatelje. Idealan ulaz u motocross sport za djecu.",
     "/en/Motorcycles/Motocross-Enduro/KX65_2026.html"),
    (48, "KLX 450R",         "Offroad",   "",   False, "Cijena na upit",
     "Enduro/cross-country 450cc. Svestrani off-road natjecatelj za teški teren.",
     "/en/Motorcycles/Motocross-Enduro/KLX450R_2024.html"),
    (49, "KLX 230R S",       "Offroad",   "A2", False, "Cijena na upit",
     "Enduro za cestu i blato. Pouzdan i lagan — savršen za A2 off-road entuzijaste.",
     "/en/Motorcycles/Motocross-Enduro/KLX230R_S_2026.html"),
    (50, "KLX 140R F",       "Offroad",   "",   False, "Cijena na upit",
     "Junior off-road motocikl s 140cc motorom. Odlican za mlade vozace koji uče off-road.",
     "/en/Motorcycles/Motocross-Enduro/KLX140R_F_2026.html"),
    (51, "KLX 140R",         "Offroad",   "",   False, "Cijena na upit",
     "Kompaktni off-road za mlade i odrasle vozace. Pouzdan, lak za upravljanje i zabavan.",
     "/en/Motorcycles/Motocross-Enduro/KLX140R_2026.html"),
    (52, "KLX 110R",         "Offroad",   "",   False, "Cijena na upit",
     "Mini off-road za najmlađe. Automatski mjenjač i niska sjedala — idealan pocetni motocikl.",
     "/en/Motorcycles/Motocross-Enduro/KLX110R_2026.html"),

    # ELECTRIC
    (53, "Ninja e-1",        "Electric",  "A2", False, "9.095 €",
     "Električni Ninja za urbanu vožnju. Nulta emisija uz prepoznatljiv Ninja dizajn i A2 pristupačnost.",
     "/en/Motorcycles/EV_HEV/ninja_e-1.html"),
    (54, "Z e-1",            "Electric",  "A2", False, "8.492 €",
     "Električni Z naked za grad. Tiha i cista vožnja s prepoznatljivim Z karakterom.",
     "/en/Motorcycles/EV_HEV/ze1.html"),
]


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.join(SCRIPT_DIR, "..")
JSON_PATH  = os.path.join(ROOT_DIR, "src", "data", "models.json")
IMG_DIR    = os.path.join(ROOT_DIR, "public", "images")


def fetch_page(path):
    url = BASE_EU + path
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"    GRESKA fetch: {e}")
        return None


def extract_all_images(html):
    """Vraca listu unikatnih remote URL-ova (1280px, bez duplikata jcr/_jcr)."""
    if not html:
        return []
    imgs = re.findall(r'/content/dam/products/pim/studio/[^\s"\'<>]+\.(?:jpg|jpeg|png)', html)
    imgs_1280 = [i for i in imgs if "1280.1280" in i]
    seen_bases = set()
    unique = []
    for img in imgs_1280:
        m = re.search(r'(/content/dam/products/pim/studio/.*?\.(?:jpg|jpeg|png))', img)
        if m:
            base = m.group(1)
            if base not in seen_bases:
                seen_bases.add(base)
                unique.append(BASE_EU + base + "/jcr:content/renditions/cq5dam.web.1280.1280.png")
    # Fallback ako nema 1280
    if not unique:
        all_imgs = re.findall(r'/content/dam/products/pim/studio/[^\s"\'<>]+\.(?:jpg|jpeg|png)', html)
        seen = set()
        for img in all_imgs:
            m = re.search(r'(/content/dam/products/pim/studio/.*?\.(?:jpg|jpeg|png))', img)
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                unique.append(BASE_EU + m.group(1))

    # Sortiraj: _A.jpg (glavni snimak) dolazi prvi, zatim B, C...
    def sort_key(url):
        m = re.search(r'_([A-Z])\.(?:jpg|jpeg|png)', url, re.IGNORECASE)
        return m.group(1).upper() if m else "Z"

    unique.sort(key=sort_key)
    return unique


def download_image(url, dest_path):
    if os.path.exists(dest_path):
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        with open(dest_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"    GRESKA download: {e}")
        return False


def extract_specs(html):
    if not html:
        return {}
    headers_raw = re.findall(r'class="prodspecs__header[^"]*"[^>]*>\s*(.*?)\s*</th>', html, re.DOTALL)
    values_raw  = re.findall(r'class="prodspecs__data[^"]*"[^>]*>\s*(.*?)\s*</td>', html, re.DOTALL)
    specs = {}
    for h, v in zip(headers_raw, values_raw):
        key = re.sub(r'<[^>]+>', '', h).strip()
        val = re.sub(r'<[^>]+>', '', v).strip()
        val = re.sub(r'\s+', ' ', val)
        if key and val:
            specs[key] = val
    return specs


def slug(name):
    n = name.replace("Kawasaki ", "")
    n = re.sub(r'[^\w\s-]', '', n)
    n = re.sub(r'\s+', '-', n.strip())
    return n.lower()


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    print(f"Povlacim podatke za {len(MODELS)} modela...\n")

    results = []
    cache = {}
    total_imgs = 0

    for row in MODELS:
        (mid, name, category, license_cat, is_new, price, description, path) = row
        full_name = f"Kawasaki {name}"
        print(f"[{mid:02d}/{len(MODELS)}] {full_name}")

        if path in cache:
            html = cache[path]
        else:
            html = fetch_page(path)
            cache[path] = html
            time.sleep(0.4)

        # Specs
        specs = extract_specs(html)

        # Slike — preuzmi lokalno
        remote_urls = extract_all_images(html)
        folder = f"{mid:02d}-{slug(full_name)}"
        model_dir = os.path.join(IMG_DIR, folder)
        os.makedirs(model_dir, exist_ok=True)

        local_paths = []
        for i, url in enumerate(remote_urls, 1):
            filename = f"img_{i:02d}.png"
            dest = os.path.join(model_dir, filename)
            if download_image(url, dest):
                local_paths.append(f"/images/{folder}/{filename}")
                total_imgs += 1
                time.sleep(0.15)

        print(f"    slike: {len(local_paths)} | specs: {len(specs)}")

        results.append({
            "id": mid,
            "name": full_name,
            "brand": "Kawasaki",
            "category": category,
            "license_category": license_cat,
            "is_new": is_new,
            "description": description,
            "price": price,
            "images": local_paths,
            "specs": specs,
        })

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    found_img   = sum(1 for m in results if m["images"])
    found_specs = sum(1 for m in results if m["specs"])
    print(f"\nGotovo!")
    print(f"  Modela:       {len(results)}")
    print(f"  S slikama:    {found_img}/{len(results)}")
    print(f"  Sa specs:     {found_specs}/{len(results)}")
    print(f"  Ukupno slika: {total_imgs}")
    print(f"\nSljedeci korak:")
    print(f"  git add . && git commit -m 'Add all models with local images and specs' && git push")


if __name__ == "__main__":
    main()
