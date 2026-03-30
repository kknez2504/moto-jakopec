"""
Scraper koji koristi dks.si kao izvor slika i specifikacija.
Logika: MODEL linkovi dolaze PRIJE SPEC linka koji ih grupira.

Pokreni: py -X utf8 scripts/build_from_dks.py
"""

import json, re, urllib.request, urllib.parse, os, time

BASE = "https://www.dks.si"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.join(SCRIPT_DIR, "..")
JSON_PATH  = os.path.join(ROOT_DIR, "src", "data", "models.json")
IMG_DIR    = os.path.join(ROOT_DIR, "public", "images")

# Sve kategorije: (dks_path, base_dir)
CATEGORY_PAGES = [
    ("html_motorji/Super_sport.html",      "html_motorji"),
    ("html_motorji/Sport_Naked.html",      "html_motorji"),
    ("html_motorji/Modern_Classic.html",   "html_motorji"),
    ("html_motorji/Urban_Cruiser.html",    "html_motorji"),
    ("html_motorji/Adventure_Tourer.html", "html_motorji"),
    ("html_motorji/Enduro.html",           "html_motorji"),
    ("html_motorji/Moto_Cross.html",       "html_motorji"),
]

# spec_url_basename -> (category, license, is_new, price, description)
# Koristimo spec URL kao stabilan kljuc za svaki model
MODELS_DATA = {
    "H2R":              ("Sport",     "",   False, "59.438 €",       "Najmoćniji serijski motocikl na svijetu. Supercharged motor od 310 KS, karbon karoserija i aerodinamički paketi za stazu."),
    "ZX-10RR_26":       ("Sport",     "",   False, "30.609 €",       "Homologirani superbike za stazu i cestu. WorldSBK iskustvo, Ohlins ovjes i Brembo kocnice."),
    "ZX-10R_26":        ("Sport",     "",   False, "20.510 €",       "Legendarni supersport s 200 KS. Bogata elektronika, IMU platforma i WorldSBK DNA."),
    "ZX-6R_24":         ("Sport",     "",   False, "13.689 €",       "Ikonični 636cc supersport — agilan i snažan. Savršen balans između staze i ceste."),
    "ZX-4RR_24":        ("Sport",     "A2", True,  "10.234 €",       "4-cilindrični 400cc motor u A2 paketu. Maksimalan sport osjećaj uz A2 ograničenje snage."),
    "ZX-4R_24":         ("Sport",     "A2", True,  "9.462 €",        "Pristupačniji ulaz u 4-cilindrični sport segment. Pravi Ninja karakter u A2 paketu."),
    "Ninja_H2SX_SE_22": ("Touring",   "",   False, "30.386 €",       "Supercharged sport-tourer s 200 KS. Elektronski ovjes, adaptivni farovi i vrhunska touring oprema."),
    "Ninja_H2SX_22":    ("Touring",   "",   False, "27.511 €",       "Supercharged touring s kompresiranim motorom za dugopružne ture."),
    "Ninja1100SXSE_25": ("Touring",   "",   True,  "16.409 €",       "Sport-tourer sljedeće generacije. Elektronski ovjes i sve što trebate za veliku turu."),
    "Ninja1100SX-25":   ("Touring",   "",   True,  "14.750 €",       "Moćan 1100cc sport-tourer s bogatom elektronikom i sportskim karakterom."),
    "Ninja7hybrid_24":  ("Electric",  "",   False, "Cijena na upit", "Revolucionarni hibridni motocikl — kombinacija 451cc benzinskog i električnog motora."),
    "Ninja650_20":      ("Sport",     "",   False, "8.449 €",        "Klasična Ninja formula — dostupna cijena, jak karakter i svakodnevna upotrebljivost."),
    "Ninja500SE_24":    ("Sport",     "A2", True,  "7.378 €",        "Novi 500cc parallel-twin u modernom Ninja ruhu. Idealan za A2 kategoriju."),
    "Ninja500_24":      ("Sport",     "A2", True,  "6.857 €",        "Pristupačni ulaz u Ninja seriju za A2 vozače. Moderan dizajn i pouzdan motor."),
    "Ninja125":         ("Sport",     "A1", False, "5.549 €",        "125cc Ninja za početnike — pravi dizajn velikog brata uz pristupačnu kategoriju."),
    "Ninja_e-1":        ("Electric",  "A2", False, "9.095 €",        "Električni Ninja za urbanu vožnju. Nulta emisija uz prepoznatljiv Ninja dizajn."),
    "ZH2_SE":           ("Naked",     "",   False, "21.940 €",       "Supercharged naked — 200 KS bez karoserije. Najsnažniji naked Kawasaki s elektronskim ovjesom."),
    "ZH2":              ("Naked",     "",   False, "19.391 €",       "Supercharged naked s kompresiranim motorom. Brutalna snaga u street paketu."),
    "Z1100SE_26":       ("Naked",     "",   True,  "13.533 €",       "Novi flagship naked s 1100cc motorom. Agresivan dizajn i bogata elektronika nove generacije."),
    "Z1100-26":         ("Naked",     "",   True,  "11.863 €",       "Moćan 1100cc naked street fighter. Nasljednik Z1000 s novim motorom i modernom elektronikom."),
    "Z900SE_25":        ("Naked",     "",   False, "12.532 €",       "Premium naked s elektronskim ovjesom. Z900 na najvišoj razini opreme."),
    "Z900_25":          ("Naked",     "",   False, "10.451 €",       "Ikonični naked street fighter. Agresivan dizajn, 948cc motor i bogata elektronika."),
    "Z650S_26":         ("Naked",     "",   True,  "7.910 €",        "Novi Z650S s Sport paketom. Sportskiji položaj i osvježen dizajn za urbanu vožnju."),
    "Z650_20":          ("Naked",     "",   False, "7.812 €",        "Lagan, agilni i pristupačni naked. Savršen za grad i vikend izlete."),
    "Z500SE_24":        ("Naked",     "A2", True,  "7.184 €",        "Novi Z500SE za A2 kategoriju. Naked karakter uz pristupačno ograničenje snage."),
    "Z500_24":          ("Naked",     "A2", True,  "6.785 €",        "Naked motocikl za A2 kategoriju. Odlican za grad i svakodnevnu vožnju."),
    "Z125":             ("Naked",     "A1", False, "5.187 €",        "Kompaktni Z naked za A1 kategoriju. Pravi Z karakter u urbanom 125cc paketu."),
    "Z_e-1":            ("Electric",  "A2", False, "8.492 €",        "Električni Z naked za grad. Tiha i cista vožnja s prepoznatljivim Z karakterom."),
    "Z7hybrid_24":      ("Electric",  "",   False, "Cijena na upit", "Hibridni Z naked — kombinacija benzinskog i električnog motora za urbanu vožnju."),
    "Z900RS":           ("Classic",   "",   False, "14.055 €",       "Premium retro s elektronskim ovjesom i zlatnim Ohlins amortizerom."),
    "Z650RS_22":        ("Classic",   "",   False, "8.441 €",        "Retro dizajn inspiriran klasičnim Z-serijom iz 70-ih uz modernu tehnologiju."),
    "W800_20":          ("Classic",   "",   False, "9.868 €",        "Prava retro ikona s paralel-twin motorom. Za ljubitelje klasike."),
    "Meguro_25":        ("Classic",   "A2", True,  "5.795 €",        "Oživljeni Meguro brend u modernom paketu. Elegantni klasik s Kawasaki pouzdanošću."),
    "W230_25":          ("Classic",   "A2", True,  "5.168 €",        "Moderan retro u pristupačnom 230cc paketu. Savršen za A2 vozace koji vole klasičan stil."),
    "VulcanS_17":       ("Cruiser",   "",   False, "8.916 €",        "Moderni cruiser s ergonomski prilagodljivom pozicijom vožnje. Stil, udobnost i karakter."),
    "Eliminator_500_SE_24": ("Cruiser","A2", True, "7.184 €",        "Novi Eliminator u A2 paketu s SE opremom. Low-seat cruiser za svaki dan."),
    "Eliminator_500_24":("Cruiser",   "A2", True,  "6.785 €",        "Moderni low-seat cruiser za A2 kategoriju."),
    "Versys_1100SE_25": ("Adventure", "",   False, "16.827 €",       "Ultimativni adventure-tourer s elektronskim ovjesom i kompletnom touring opremom."),
    "Versys_1100S_25":  ("Adventure", "",   False, "15.263 €",       "Moćan 1100cc adventure-tourer. Sportski karakter i touring udobnost u jednom."),
    "Versys_1100_25":   ("Adventure", "",   False, "13.556 €",       "Klasični Versys recept uz 1100cc snagu. Svestran, udoban i pouzdan za duge ture."),
    "Versys_650_22":    ("Adventure", "",   True,  "8.937 €",        "Najpristupačniji adventure-tourer. Udoban, svestran i ekonomičan za svakodnevnu vožnju."),
    "KLE500SE_26":      ("Adventure", "A2", True,  "7.442 €",        "Novi KLE500 SE — pravi mali adventure u A2 paketu s bogatom opremom."),
    "KLE500_26":        ("Adventure", "A2", True,  "6.664 €",        "Ulazni adventure motocikl za A2 kategoriju. Robusni dizajn i pouzdan motor."),
    "KX450X_24":        ("Offroad",   "",   False, "Cijena na upit", "Cross-country enduro verzija KX450 za dugotrajne off-road utrke i avanturu."),
    "KX250X_25":        ("Offroad",   "",   False, "Cijena na upit", "Cross-country enduro na bazi KX250 za dugotrajne off-road avanture."),
    "KLX230RS_25":      ("Offroad",   "A2", False, "Cijena na upit", "Enduro za cestu i blato. Pouzdan i lagan — savršen za A2 off-road entuzijaste."),
    "KLX140R":          ("Offroad",   "",   False, "Cijena na upit", "Off-road za mlade i odrasle vozace. Pouzdan, lak za upravljanje i zabavan."),
    "KLX110":           ("Offroad",   "",   False, "Cijena na upit", "Mini off-road za najmlađe. Automatski mjenjač i niska sjedala."),
    "KX450_24":         ("Offroad",   "",   False, "Cijena na upit", "Vrhunski motocross natjecatelj. Razvijen za pobjedu na stazi."),
    "KX250_25":         ("Offroad",   "",   False, "Cijena na upit", "Profesionalni 250cc motocross. Lagan, brz i agresivan."),
    "KX112_26":         ("Offroad",   "",   False, "Cijena na upit", "2-taktni motocross za mlake natjecatelje. Lagani i precizni."),
    "KX85_26":          ("Offroad",   "",   False, "Cijena na upit", "2-taktni junior motocross za mlade natjecatelje."),
    "KX85L_26":         ("Offroad",   "",   False, "Cijena na upit", "2-taktni junior motocross Large verzija — za više vozace."),
    "KX65":             ("Offroad",   "",   False, "Cijena na upit", "Motocross za najmlađe natjecatelje. Idealan ulaz u motocross sport."),
    "KLX450R_24":       ("Offroad",   "",   False, "Cijena na upit", "Enduro/cross-country 450cc. Svestrani off-road natjecatelj za teški teren."),
    "Elektrode_20":     ("Electric",  "",   False, "Cijena na upit", "Električni motocross za djecu. Tiha i ekološki prihvatljiva zabava na terenu."),
}

# Izvuci ime modela iz spec URL-a za prikaz
SPEC_DISPLAY_NAMES = {
    "H2R":              "Ninja H2R",
    "ZX-10RR_26":       "Ninja ZX-10RR",
    "ZX-10R_26":        "Ninja ZX-10R",
    "ZX-6R_24":         "Ninja ZX-6R",
    "ZX-4RR_24":        "Ninja ZX-4RR",
    "ZX-4R_24":         "Ninja ZX-4R",
    "Ninja_H2SX_SE_22": "Ninja H2SX SE",
    "Ninja_H2SX_22":    "Ninja H2SX",
    "Ninja1100SXSE_25": "Ninja 1100SX SE",
    "Ninja1100SX-25":   "Ninja 1100SX",
    "Ninja7hybrid_24":  "Ninja 7 Hybrid",
    "Ninja650_20":      "Ninja 650",
    "Ninja500SE_24":    "Ninja 500 SE",
    "Ninja500_24":      "Ninja 500",
    "Ninja125":         "Ninja 125",
    "Ninja_e-1":        "Ninja e-1",
    "ZH2_SE":           "Z H2 SE",
    "ZH2":              "Z H2",
    "Z1100SE_26":       "Z 1100 SE",
    "Z1100-26":         "Z 1100",
    "Z900SE_25":        "Z 900 SE",
    "Z900_25":          "Z 900",
    "Z650S_26":         "Z 650 S",
    "Z650_20":          "Z 650",
    "Z500SE_24":        "Z 500 SE",
    "Z500_24":          "Z 500",
    "Z125":             "Z 125",
    "Z_e-1":            "Z e-1",
    "Z7hybrid_24":      "Z 7 Hybrid",
    "Z900RS":           "Z 900RS SE",
    "Z650RS_22":        "Z 650RS",
    "W800_20":          "W 800",
    "Meguro_25":        "Meguro S1",
    "W230_25":          "W 230",
    "VulcanS_17":       "Vulcan S",
    "Eliminator_500_SE_24": "Eliminator 500 SE",
    "Eliminator_500_24":"Eliminator 500",
    "Versys_1100SE_25": "Versys 1100 SE",
    "Versys_1100S_25":  "Versys 1100 S",
    "Versys_1100_25":   "Versys 1100",
    "Versys_650_22":    "Versys 650",
    "KLE500SE_26":      "KLE 500 SE",
    "KLE500_26":        "KLE 500",
    "KX450X_24":        "KX 450X",
    "KX250X_25":        "KX 250X",
    "KLX230RS_25":      "KLX 230R S",
    "KLX140R":          "KLX 140R",
    "KLX110":           "KLX 110R",
    "KX450_24":         "KX 450",
    "KX250_25":         "KX 250",
    "KX112_26":         "KX 112",
    "KX85_26":          "KX 85",
    "KX85L_26":         "KX 85L",
    "KX65":             "KX 65",
    "KLX450R_24":       "KLX 450R",
    "Elektrode_20":     "Elektrode 20",
}


def fetch(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None


def parse_groups(cat_html, base_dir):
    """Parsira kategorijsku stranicu i vraca listu: [(model_pages[], spec_url)]"""
    links = re.findall(r'href=["\']([^"\']+\.html)["\']', cat_html)
    groups = []
    current_pages = []
    for link in links:
        if 'youtube' in link or 'kawasaki.eu' in link:
            continue
        if 'Teh_podatki' in link:
            if current_pages:
                spec_url = urllib.parse.urljoin(f"{BASE}/{base_dir}/", link)
                groups.append((list(current_pages), spec_url))
                current_pages = []
        else:
            page_url = urllib.parse.urljoin(f"{BASE}/{base_dir}/", link)
            current_pages.append(page_url)
    return groups


def extract_images(html, page_url):
    """Izvuce URL-ove slika s model stranice — samo HD, bez thumbnailova i ikona."""
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png))["\']', html, re.IGNORECASE)
    result = []
    for img in imgs:
        skip_patterns = ['new%20green', 'new green', 'logo', 'favicon', 'banner', '_m.jpg', '_m.png', 'K-CARE', 'SLO-flag']
        if any(p.lower() in img.lower() for p in skip_patterns):
            continue
        if re.match(r'^\d+\.\.(png|jpg)$', img, re.IGNORECASE):
            continue
        full = img if img.startswith('http') else urllib.parse.urljoin(page_url, img)
        result.append(full)
    return list(dict.fromkeys(result))


def extract_specs(html):
    specs = {}
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
    for row in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        cleaned = [re.sub(r'<[^>]+>', '', c).replace("&nbsp;", " ").replace("&#966;", "φ")
                   .replace("&sup3;", "³").replace("&sup2;", "²").strip() for c in cells]
        cleaned = [re.sub(r'\s+', ' ', c) for c in cleaned]
        if len(cleaned) >= 2 and cleaned[0] and cleaned[1] and len(cleaned[0]) < 60:
            specs[cleaned[0]] = cleaned[1]
    return specs


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
    except:
        return False


def slug(name):
    n = re.sub(r'[^\w\s-]', '', name)
    return re.sub(r'\s+', '-', n.strip()).lower()


def main():
    os.makedirs(IMG_DIR, exist_ok=True)

    # Skupi sve grupe iz svih kategorija (dedupliciraj po spec_url)
    all_groups = {}  # spec_url -> [model_pages...]
    print("Skeniram kategorije...")
    for (cat_path, base_dir) in CATEGORY_PAGES:
        cat_html = fetch(f"{BASE}/{cat_path}")
        if not cat_html:
            continue
        groups = parse_groups(cat_html, base_dir)
        for (pages, spec_url) in groups:
            if spec_url not in all_groups:
                all_groups[spec_url] = pages
            else:
                # Dodaj nove stranice (nove boje)
                for p in pages:
                    if p not in all_groups[spec_url]:
                        all_groups[spec_url].append(p)

    print(f"  Pronasao {len(all_groups)} modela\n")

    results = []
    mid = 1

    for spec_url, model_pages in all_groups.items():
        spec_key = os.path.basename(spec_url).replace('.html', '')

        data = MODELS_DATA.get(spec_key)
        display_name = SPEC_DISPLAY_NAMES.get(spec_key)

        if not data or not display_name:
            print(f"  PRESKACAM: {spec_key}")
            continue

        category, license_cat, is_new, price, description = data
        full_name = f"Kawasaki {display_name}"
        print(f"[{mid:02d}] {full_name}")

        # Skupi slike sa SVIH boja
        all_images = []
        for page_url in model_pages:
            html = fetch(page_url)
            if html:
                imgs = extract_images(html, page_url)
                for img in imgs:
                    if img not in all_images:
                        all_images.append(img)
            time.sleep(0.2)

        # Sortiraj: _A studio slike prve
        def img_sort(u):
            fname = os.path.basename(u).lower()
            if re.search(r'_a[._]', fname): return "0_" + fname
            if re.search(r'_b[._]', fname): return "1_" + fname
            return "9_" + fname
        all_images.sort(key=img_sort)

        # Preuzmi lokalno
        folder = f"{mid:02d}-{slug(display_name)}"
        model_dir = os.path.join(IMG_DIR, folder)
        os.makedirs(model_dir, exist_ok=True)

        local_paths = []
        for i, img_url in enumerate(all_images, 1):
            ext = os.path.splitext(img_url.split("?")[0])[1].lower() or ".jpg"
            if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                ext = '.jpg'
            fname = f"img_{i:02d}{ext}"
            dest = os.path.join(model_dir, fname)
            if download_image(img_url, dest):
                local_paths.append(f"/images/{folder}/{fname}")
            time.sleep(0.1)

        # Specs
        spec_html = fetch(spec_url)
        specs = extract_specs(spec_html) if spec_html else {}
        time.sleep(0.2)

        print(f"     slike: {len(local_paths)} | specs: {len(specs)}")

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
        mid += 1
        time.sleep(0.2)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    found_img   = sum(1 for m in results if m["images"])
    found_specs = sum(1 for m in results if m["specs"])
    total_imgs  = sum(len(m["images"]) for m in results)
    print(f"\nGotovo!")
    print(f"  Modela:       {len(results)}")
    print(f"  S slikama:    {found_img}/{len(results)}")
    print(f"  Sa specs:     {found_specs}/{len(results)}")
    print(f"  Ukupno slika: {total_imgs}")
    print(f"\n  git add . && git commit -m 'Rebuild from dks.si - all images and specs' && git push")


if __name__ == "__main__":
    main()
