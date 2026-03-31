# Moto Jakopec — Claude kontekst

Kawasaki dealerstvo Samobor, Hrvatska. Katalog motocikala, opreme i dijelova.

## Tehnologije

- **Next.js 14** App Router, TypeScript, Tailwind CSS
- **Vercel** hosting, automatski deploy iz GitHub (`kknez2504/moto-jakopec`)
- **Python + openpyxl** za upravljanje podacima (lokalno, ne deployaju se)

## Struktura podataka

```
src/data/
  models.json     ← sva vozila (78 Kawasaki modela)
  products.json   ← oprema i dijelovi (prazno dok se ne popuni)
  brands.json     ← brendovi { "oprema": [...], "dijelovi": [...] }

public/images/
  vozila/{model-folder}/   ← slike vozila
  oprema/{item-folder}/    ← slike opreme
  dijelovi/{item-folder}/  ← slike dijelova
  brendovi/{brand_id}.png  ← logoti brendova
```

## Python skripte (u scripts/)

| Skripta | Opis |
|---------|------|
| `vozila_scraper_dks.py` | Scrapa vozila s dks.si → models.json |
| `vozila_json_to_excel.py` | models.json → vozila.xlsx (inicijalizacija) |
| `vozila_excel_to_json.py` | vozila.xlsx → models.json (nakon izmjena) |
| `vozila_sync_slike.py` | Sinkronizira putanje slika disk ↔ models.json |
| `kreiraj_excel_predlozak.py` | Dodaje sheetove Brendovi u proizvodi.xlsx |
| `proizvodi_json_to_excel.py` | products.json → proizvodi.xlsx (inicijalizacija) |
| `proizvodi_excel_to_json.py` | proizvodi.xlsx → products.json + brands.json |

## Excel datoteke (.gitignore)

- `vozila.xlsx` — upravljanje vozilima
- `proizvodi.xlsx` — upravljanje opremom, dijelovima i brendovima

### Struktura proizvodi.xlsx

**Sheet "Proizvodi"** stupci:
`id | name | category | subcategory | price | description | image_folder | is_new | brand`

- `category`: mora biti točno `Oprema` ili `Dijelovi`
- `brand`: brand_id iz sheeta Brendovi_Oprema / Brendovi_Dijelovi (npr. `airoh`, `motul`)

**Sheet "Brendovi_Oprema"** stupci:
`brand_id | name | logo_folder | website | active`

**Sheet "Brendovi_Dijelovi"** stupci:
`brand_id | name | logo_folder | website | active`

## Brendovi

### Oprema
| brand_id | Naziv |
|----------|-------|
| wind | WIND Raceware |
| airoh | Airoh |
| progrip | Progrip |
| mitas | Mitas |
| motul | Motul |
| valvoline | Valvoline |

### Dijelovi
| brand_id | Naziv |
|----------|-------|
| prox | Pro-X Racing Parts |
| wiseco | Wiseco |
| wrp | WRP |
| cht | CHT Sprockets |
| rk | RK Chains |
| trw | TRW Lucas |
| denso | Denso |

## Navigacija (Header.tsx)

```
Početna | Motocikli | Quad | Mule | Jet Ski | Oprema | Dijelovi | Kontakt
```

- `Quad`, `Mule`, `Jet Ski` → `/motocikli?category=X` (SPECIAL_CATEGORIES u motocikli/page.tsx)
- `/oprema` → lista s BrandsGrid + filter
- `/oprema/{brand_id}` → proizvodi jednog brenda grupirani po subcategory
- `/dijelovi/{brand_id}` → isto za dijelove

## Tijek rada — dodavanje proizvoda

1. Otvori `proizvodi.xlsx`
2. Popuni red u sheetu "Proizvodi" (category mora biti `Oprema` ili `Dijelovi`)
3. Stavi slike u `public/images/oprema/{image_folder}/` ili `public/images/dijelovi/{image_folder}/`
4. Stavi logo brenda u `public/images/brendovi/{brand_id}.png`
5. Pokreni: `py -X utf8 scripts/proizvodi_excel_to_json.py`
6. `git add . && git commit -m "Dodan proizvod" && git push`

## Tijek rada — ažuriranje vozila

1. `py -X utf8 scripts/vozila_json_to_excel.py` (samo jednom za inicijalizaciju)
2. Uredi `vozila.xlsx`
3. `py -X utf8 scripts/vozila_excel_to_json.py`
4. `git add src/data/models.json && git commit -m "Ažurirana vozila" && git push`

## Dizajn sistem (globals.css)

```css
--bg:       #edf3ed   /* pozadina */
--surface:  #ffffff   /* kartice */
--text:     #111611
--muted:    #5b655d
--green:    #37b63a   /* primarna boja */
--green-dk: #218e28
--radius:   26px
```

Amber (`#f59e0b`) se koristi za hover efekte na brendovima.

## Važne napomene

- Website čita SAMO `models.json`, `products.json` i `brands.json` — Excel i Python su lokalni alati
- `vozila.xlsx` i `proizvodi.xlsx` su u `.gitignore` — ne commitaju se
- Slike moraju biti u `public/images/` da bi Next.js Image ih servirao
- `SPECIAL_CATEGORIES = ["Quad", "Mule", "Jet Ski"]` — ove kategorije idu u posebne nav linkove, ne pod "Motocikli"
- Scraper `vozila_scraper_dks.py` koristi HR prijevode iz SL_HR rječnika — jednom u JSON-u, sve je na hrvatskom
