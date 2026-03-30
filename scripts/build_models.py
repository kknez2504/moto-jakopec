"""
Generira kompletan models.json:
- Svi modeli i cijene s dks.si cjenika
- Slike povučene s kawasaki.eu

Pokreni: python scripts/build_models.py
"""

import json
import re
import urllib.request
import time
import os

BASE_EU = "https://www.kawasaki.eu"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# ─── Svi modeli s dks.si cjenika ────────────────────────────────────────────
# Format: (id, name, category_hr, category_en, license, is_new, price_2026, opis, kawasaki_eu_path)

MODELS = [
    # SUPERSPORT
    (1,  "Ninja H2R",        "Sport",     "Sport",    "",   False, "59.438 €",
     "Najmoćniji serijski motocikl na svijetu. Supercharged motor od 310 KS, karbon karoserija i aerodinamički paketi za stazu.",
     "/en/Motorcycles/Hypersport/Ninja_H2R_2026.html"),

    (2,  "Ninja ZX-10RR",    "Sport",     "Sport",    "",   False, "30.609 €",
     "Homologirani superbike za stazu i cestu. Razvijen direktno iz WorldSBK iskustva s Öhlins ovjesom i Brembo kočnicama.",
     "/en/Motorcycles/Supersport_Sport/Ninja_ZX-10RR_2026.html"),

    (3,  "Ninja ZX-10R",     "Sport",     "Sport",    "",   False, "20.510 €",
     "Legendarni supersport s 200 KS. Bogata elektronika, IMU platforma i WorldSBK DNA u svakom detalju.",
     "/en/Motorcycles/Supersport_Sport/Ninja_ZX-10R_2026.html"),

    (4,  "Ninja ZX-6R",      "Sport",     "Sport",    "",   False, "13.689 €",
     "Ikonični 636cc supersport — agilan, zabavan i snažan. Savršen balans između staze i ceste.",
     "/en/Motorcycles/Supersport_Sport/Ninja_zx-6r_2026.html"),

    (5,  "Ninja ZX-4RR",     "Sport",     "Sport",    "A2", True,  "10.234 €",
     "4-cilindrični 400cc motor u A2 paketu. Maksimalan sport osjećaj uz ograničenje snage za A2 kategoriju.",
     "/en/Motorcycles/Supersport_Sport/Ninja_zx-4rr_2026.html"),

    (6,  "Ninja ZX-4R",      "Sport",     "Sport",    "A2", True,  "9.462 €",
     "Pristupačniji ulaz u 4-cilindrični sport segment. Pravi Ninja karakter u A2 paketu.",
     "/en/Motorcycles/Supersport_Sport/Ninja_zx-4r_2026.html"),

    # STREET & TOURER (Ninja)
    (7,  "Ninja H2SX SE",    "Touring",   "Touring",  "",   False, "30.386 €",
     "Supercharged sport-tourer s 200 KS. Elektronski ovjes, adaptivni farovi i touring oprema na najvišoj razini.",
     "/en/Motorcycles/Sport_Tourer/Ninja_H2_SX_SE_2026.html"),

    (8,  "Ninja H2SX",       "Touring",   "Touring",  "",   False, "27.511 €",
     "Supercharged touring s kompresiranim motorom i izvanrednim performansama za dugopružne ture.",
     "/en/Motorcycles/Sport_Tourer/Ninja_H2_SX_2026.html"),

    (9,  "Ninja 1100SX SE",  "Touring",   "Touring",  "",   True,  "16.409 €",
     "Sport-tourer sljedeće generacije. Electronski ovjes, navigacija i sve što trebate za veliku turu.",
     "/en/Motorcycles/Sport_Tourer/Ninja_1100_SX_SE_2026.html"),

    (10, "Ninja 1100SX",     "Touring",   "Touring",  "",   True,  "14.750 €",
     "Moćan 1100cc sport-tourer s bogatom elektronikom i sportskim karakterom na dugim rutama.",
     "/en/Motorcycles/Sport_Tourer/Ninja_1100SX_2026.html"),

    (11, "Ninja 650 SE",     "Sport",     "Sport",    "",   False, "8.634 €",
     "Najpopularniji Kawasaki za početnike i iskusne vozače. Uravnotežen, zabavan i praktičan za svaki dan.",
     "/en/Motorcycles/Supersport_Sport/Ninja_650_2026.html"),

    (12, "Ninja 650",        "Sport",     "Sport",    "",   False, "8.449 €",
     "Klasična Ninja formula — dostupna cijena, jak karakter i svakodnevna upotrebljivost.",
     "/en/Motorcycles/Supersport_Sport/Ninja_650_2026.html"),

    (13, "Ninja 500 SE",     "Sport",     "Sport",    "A2", True,  "7.378 €",
     "Novi 500cc parallel-twin u modernom Ninja ruhu. Idealan za A2 kategoriju uz pravi sport izgled.",
     "/en/Motorcycles/Supersport_Sport/Ninja_500_se_2026.html"),

    (14, "Ninja 500",        "Sport",     "Sport",    "A2", True,  "6.857 €",
     "Pristupačni ulaz u Ninja seriju za A2 vozače. Moderan dizajn i pouzdan motor.",
     "/en/Motorcycles/Supersport_Sport/Ninja_500_2026.html"),

    (15, "Ninja 125 SE",     "Sport",     "Sport",    "A1", False, "5.665 €",
     "Pravi Ninja karakter u 125cc paketu. Za A1 kategoriju uz punokrvni sport izgled.",
     "/en/Motorcycles/Supersport_Sport/Ninja_125_2026.html"),

    (16, "Ninja 125",        "Sport",     "Sport",    "A1", False, "5.549 €",
     "125cc Ninja za početnike — pravi dizajn velikog brata uz pristupačnu kategoriju.",
     "/en/Motorcycles/Supersport_Sport/Ninja_125_2026.html"),

    # SUPERNAKED
    (17, "Z H2 SE",          "Naked",     "Naked",    "",   False, "21.940 €",
     "Supercharged naked — 200 KS bez karoserije. Najsnažniji naked Kawasaki s elektronskim ovjesom.",
     "/en/Motorcycles/Supernaked/Zh2_se_2026.html"),

    (18, "Z H2",             "Naked",     "Naked",    "",   False, "19.391 €",
     "Supercharged naked s kompresiranim motorom. Brutalna snaga u street paketu.",
     "/en/Motorcycles/Supernaked/Zh2_2026.html"),

    (19, "Z 1100 SE",        "Naked",     "Naked",    "",   True,  "13.533 €",
     "Novi flagship naked s 1100cc motorom. Agresivan dizajn i bogata elektronika nove generacije.",
     "/en/Motorcycles/Supernaked/Z1100_SE_2026.html"),

    (20, "Z 1100",           "Naked",     "Naked",    "",   True,  "11.863 €",
     "Moćan 1100cc naked street fighter. Nasljednik Z1000 s novim motorom i modernom elektronikom.",
     "/en/Motorcycles/Supernaked/z1100_2026.html"),

    (21, "Z 900 SE",         "Naked",     "Naked",    "",   False, "12.532 €",
     "Premium naked s elektronskim ovjesom i punom elektronikom. Z900 na najvišoj razini opreme.",
     "/en/Motorcycles/Supernaked/Z900_se_2026.html"),

    (22, "Z 900",            "Naked",     "Naked",    "",   False, "10.451 €",
     "Ikonični naked street fighter. Agresivan dizajn, 948cc motor i bogata elektronika.",
     "/en/Motorcycles/Supernaked/Z900_2026.html"),

    (23, "Z 650 S",          "Naked",     "Naked",    "",   True,  "7.910 €",
     "Novi Z650S s Sport paketom. Sportskiji položaj i osvježen dizajn za urbanu vožnju.",
     "/en/Motorcycles/Supernaked/Z650_S_2026.html"),

    (24, "Z 650",            "Naked",     "Naked",    "",   False, "7.812 €",
     "Lagan, agilni i pristupačni naked. Savršen za grad i vikend izlete.",
     "/en/Motorcycles/Supernaked/Z650_2026.html"),

    (25, "Z 125",            "Naked",     "Naked",    "A1", False, "5.187 €",
     "Kompaktni Z naked za A1 kategoriju. Pravi Z karakter u urbanom 125cc paketu.",
     "/en/Motorcycles/Supernaked/Z125_2026.html"),

    # MODERN CLASSIC
    (26, "Z 900RS SE",       "Classic",   "Classic",  "",   False, "14.055 €",
     "Premium retro s elektronskim ovjesom i zlatnim Öhlins amortizerom. Najluđi retro Kawasaki.",
     "/en/Motorcycles/Retro_Sport/Z900RS_SE_2026.html"),

    (27, "Z 650RS SE",       "Classic",   "Classic",  "",   False, "8.441 €",
     "Retro dizajn inspiriran klasičnim Z-serijom iz 70-ih uz modernu tehnologiju i pouzdanost.",
     "/en/Motorcycles/Retro_Sport/Z650RS_2026.html"),

    (28, "W 800",            "Classic",   "Classic",  "",   False, "9.868 €",
     "Prava retro ikona s paralel-twin motorom i vremenski provjerenim dizajnom. Za ljubitelje klasike.",
     "/en/Motorcycles/Classic/w800_2025.html"),

    (29, "Meguro S1",        "Classic",   "Classic",  "A2", True,  "5.795 €",
     "Oživljeni Meguro brend u modernom paketu. Elegantni 125cc klasik s Kawasaki pouzdanošću.",
     "/en/Motorcycles/Classic/Meguro_s1_2026.html"),

    (30, "W 230",            "Classic",   "Classic",  "A2", True,  "5.168 €",
     "Moderan retro u pristupačnom 230cc paketu. Savršen za A2 vozače koji vole klasičan stil.",
     "/en/Motorcycles/Classic/W230_2026.html"),

    # URBAN CRUISER
    (31, "Vulcan S SE",      "Cruiser",   "Cruiser",  "",   False, "8.916 €",
     "Premium cruiser s ergonomski prilagodljivom pozicijom vožnje. Stil, udobnost i karakter.",
     "/en/Motorcycles/Urban_Cruiser/vulcan_s_2026.html"),

    (32, "Vulcan S",         "Cruiser",   "Cruiser",  "",   False, "8.593 €",
     "Moderni cruiser s adjustable ergonomijom. Za sve koji žele slobodu ceste uz komfor.",
     "/en/Motorcycles/Urban_Cruiser/vulcan_s_2026.html"),

    (33, "Eliminator 500 SE","Cruiser",   "Cruiser",  "A2", True,  "7.184 €",
     "Novi Eliminator u A2 paketu s SE opremom. Low-seat cruiser za svaki dan.",
     "/en/Motorcycles/Urban_Cruiser/eliminator_500_se_2026.html"),

    (34, "Eliminator 500",   "Cruiser",   "Cruiser",  "A2", True,  "6.785 €",
     "Moderni low-seat cruiser za A2 kategoriju. Pristupačan ulaz u cruiser segment.",
     "/en/Motorcycles/Urban_Cruiser/eliminator_500_2026.html"),

    # ADVENTURE TOURER
    (35, "Versys 1100 SE",   "Adventure", "Adventure","",   False, "16.827 €",
     "Ultimativni adventure-tourer s elektronskim ovjesom i kompletnom touring opremom.",
     "/en/Motorcycles/Adventure_Tourer/Versys_1100_se_2026.html"),

    (36, "Versys 1100 S",    "Adventure", "Adventure","",   False, "15.263 €",
     "Moćan 1100cc adventure-tourer. Sportski karakter i touring udobnost u jednom.",
     "/en/Motorcycles/Adventure_Tourer/Versys_1100_s_2026.html"),

    (37, "Versys 1100",      "Adventure", "Adventure","",   False, "13.556 €",
     "Klasični Versys recept uz 1100cc snagu. Svestran, udoban i pouzdan za duge ture.",
     "/en/Motorcycles/Adventure_Tourer/versys-1100---2026.html"),

    (38, "Versys 650",       "Adventure", "Adventure","",   True,  "8.937 €",
     "Najpristupačniji adventure-tourer. Udoban, svestran i ekonomičan za svakodnevnu vožnju.",
     "/en/Motorcycles/Adventure_Tourer/Versys_650_2026.html"),

    (39, "KLE 500 SE",       "Adventure", "Adventure","A2", True,  "7.442 €",
     "Novi KLE500 SE — pravi mali adventure u A2 paketu s bogatom opremom.",
     "/en/Motorcycles/Adventure/KLE500_SE_2026.html"),

    (40, "KLE 500",          "Adventure", "Adventure","A2", True,  "6.664 €",
     "Ulazni adventure motocikl za A2 kategoriju. Robusni dizajn i pouzdan motor.",
     "/en/Motorcycles/Adventure/KLE500_2026.html"),

    # CityEBike
    (41, "Ninja e-1",        "Electric",  "Electric", "A2", False, "9.095 €",
     "Električni Ninja za urbanu vožnju. Nulta emisija uz prepoznatljiv Ninja dizajn i A2 pristupačnost.",
     "/en/Motorcycles/EV_HEV/ninja_e-1.html"),

    (42, "Z e-1",            "Electric",  "Electric", "A2", False, "8.492 €",
     "Električni Z naked za grad. Tiha i čista vožnja s prepoznatljivim Z karakterom.",
     "/en/Motorcycles/EV_HEV/ze1.html"),
]


def fetch_og_image(path):
    url = BASE_EU + path
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # Trazi product/pim studio sliku u 1280x1280
        imgs = re.findall(r'/content/dam/products/pim/studio/[^\s"\'<>]+\.(?:jpg|jpeg|png)', html)
        unique = list(dict.fromkeys(imgs))

        # Preferiraj 1280 rezoluciju
        for img in unique:
            if "1280.1280" in img:
                return BASE_EU + img

        # Fallback: uzmi prvu koja nije thumbnail
        for img in unique:
            if "thumbnail" not in img and "320" not in img:
                return BASE_EU + img

        # Posljednji fallback: prva dostupna
        if unique:
            return BASE_EU + unique[0]

        return None
    except Exception as e:
        print(f"    GRESKA ({url}): {e}")
        return None


def build_model(row, image_url):
    (mid, name, category, purpose, license_cat, is_new, price, description, _) = row
    return {
        "id": mid,
        "name": f"Kawasaki {name}",
        "brand": "Kawasaki",
        "category": category,
        "purpose": purpose,
        "license_category": license_cat,
        "is_new": is_new,
        "description": description,
        "price": price,
        "images": [image_url] if image_url else [],
        "specs": {}
    }


def main():
    print(f"Povlačim slike za {len(MODELS)} modela...\n")

    results = []
    seen_paths = {}  # cache da ne fetcha isti URL dvaput

    for row in MODELS:
        name = row[1]
        path = row[8]
        print(f"[{row[0]:02d}/{len(MODELS)}] Kawasaki {name}")

        if path in seen_paths:
            image_url = seen_paths[path]
            print(f"    (cache) {(image_url or 'nema slike')[:80]}")
        else:
            image_url = fetch_og_image(path)
            seen_paths[path] = image_url
            if image_url:
                print(f"    ✓ {image_url[:80]}")
            else:
                print(f"    ✗ slika nije pronađena")
            time.sleep(0.4)

        results.append(build_model(row, image_url))

    # Spremi
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "..", "src", "data", "models.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    found = sum(1 for m in results if m["images"])
    print(f"\n✓ Gotovo! {found}/{len(results)} modela ima sliku.")
    print(f"  Datoteka: {out_path}")
    print(f"\n  Sljedeći korak:")
    print(f"  git add . && git commit -m 'Add all 42 models with images' && git push")


if __name__ == "__main__":
    main()
