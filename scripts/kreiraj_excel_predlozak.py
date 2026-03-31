"""
Dodaje sheetove Brendovi_Oprema, Brendovi_Dijelovi i Šifrarnik u proizvodi.xlsx.
Šifrarnik definira padajuće izbornike za category, subcategory i brand.
Ako xlsx ne postoji, kreira ga sa praznim Proizvodima.
Dodaje stupac 'brand' u sheet Proizvodi ako već ne postoji.

Pokreni JEDNOM za inicijalizaciju (i svaki put kad dodaješ nove opcije):
    py -X utf8 scripts/kreiraj_excel_predlozak.py
"""

import os, shutil, tempfile
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.workbook.defined_name import DefinedName

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.join(SCRIPT_DIR, "..")
EXCEL_PATH = os.path.join(ROOT_DIR, "proizvodi.xlsx")

# ── Podaci brendova ─────────────────────────────────────────────────────────
BRENDOVI_OPREMA = [
    ("wind",      "WIND Raceware", "wind",      "wind-raceware.com",  True),
    ("airoh",     "Airoh",         "airoh",      "airoh.com",          True),
    ("progrip",   "Progrip",       "progrip",    "progrip.it",         True),
    ("mitas",     "Mitas",         "mitas",      "mitas-moto.com",     True),
    ("motul",     "Motul",         "motul",      "motul.com",          True),
    ("valvoline", "Valvoline",     "valvoline",  "valvoline.com",      True),
]

BRENDOVI_DIJELOVI = [
    ("prox",   "Pro-X Racing Parts", "prox",   "pro-x.com",          True),
    ("wiseco", "Wiseco",             "wiseco",  "wiseco.com",         True),
    ("wrp",    "WRP",                "wrp",     "wrp-racing.com",     True),
    ("cht",    "CHT Sprockets",      "cht",     "cht-sprockets.com",  True),
    ("rk",     "RK Chains",          "rk",      "rk-chain.com",       True),
    ("trw",    "TRW Lucas",          "trw",     "trwaftermarket.com", True),
    ("denso",  "Denso",              "denso",   "denso.com",          True),
]

BRAND_HEADERS = ["brand_id", "name", "logo_folder", "website", "active"]

# ── Šifrarnik — slobodno uredi ove liste ─────────────────────────────────────
KATEGORIJE = ["Oprema", "Dijelovi"]

PODKATEGORIJE_OPREMA = [
    "Kacige", "Jakne", "Hlače", "Rukavice", "Čizme",
    "Odijela", "Zaštita", "Prsluk", "Termo rublje", "Ostalo",
]

PODKATEGORIJE_DIJELOVI = [
    "Filteri", "Ulja i maziva", "Lanci", "Zupčanici", "Gume",
    "Kočnice", "Svjećice", "Amortizeri", "Ovjesi", "Električni dijelovi",
    "Motor", "Ostalo",
]

# ── Stilovi ─────────────────────────────────────────────────────────────────
def header_style(color="1B5E20"):
    fill   = PatternFill("solid", fgColor=color)
    font   = Font(color="FFFFFF", bold=True, size=10)
    center = Alignment(horizontal="center", vertical="center")
    border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC"),
    )
    return fill, font, center, border

def data_border():
    return Border(
        left=Side(style="thin", color="EEEEEE"),
        right=Side(style="thin", color="EEEEEE"),
        bottom=Side(style="thin", color="EEEEEE"),
    )

FILLS = [
    PatternFill("solid", fgColor="F9FBF9"),
    PatternFill("solid", fgColor="E8F5E9"),
]

# ── Kreira "Šifrarnik" sheet ─────────────────────────────────────────────────
def write_sifrarnik(wb):
    if "Šifrarnik" in wb.sheetnames:
        del wb["Šifrarnik"]
    ws = wb.create_sheet("Šifrarnik")

    # Boje zaglavlja po kolonama
    colors = {
        "A": ("Kategorija",             KATEGORIJE,                 "1B5E20"),
        "B": ("Podkategorija - Oprema",  PODKATEGORIJE_OPREMA,      "E65100"),
        "C": ("Podkategorija - Dijelovi",PODKATEGORIJE_DIJELOVI,    "1565C0"),
        "D": ("Brand - Oprema",          [b[0] for b in BRENDOVI_OPREMA],    "7B1FA2"),
        "E": ("Brand - Dijelovi",        [b[0] for b in BRENDOVI_DIJELOVI],  "00838F"),
    }

    for col_letter, (title, values, color) in colors.items():
        fill, font, center, border = header_style(color)
        cell = ws[f"{col_letter}1"]
        cell.value = title
        cell.font = font
        cell.fill = fill
        cell.alignment = center
        cell.border = border
        ws.row_dimensions[1].height = 26

        for ri, val in enumerate(values, start=2):
            c = ws[f"{col_letter}{ri}"]
            c.value = val
            c.alignment = Alignment(vertical="center")
            c.border = data_border()
            ws.row_dimensions[ri].height = 17

        ws.column_dimensions[col_letter].width = 26

    ws.freeze_panes = "A2"
    print(f"  Sheet 'Šifrarnik': {len(KATEGORIJE)} kategorija, "
          f"{len(PODKATEGORIJE_OPREMA)} opr. podkat., "
          f"{len(PODKATEGORIJE_DIJELOVI)} dij. podkat.")

    # ── Definirani imenici (Named Ranges) za dropdown reference ──────────────
    #    Excel zahtijeva named range kad je izvor na drugom sheetu
    max_rows = max(
        len(KATEGORIJE),
        len(PODKATEGORIJE_OPREMA),
        len(PODKATEGORIJE_DIJELOVI),
        len(BRENDOVI_OPREMA),
        len(BRENDOVI_DIJELOVI),
    ) + 1  # +1 za zaglavlje

    named = {
        "NR_Kategorija":          f"Šifrarnik!$A$2:$A${len(KATEGORIJE)+1}",
        "NR_Podkat_Oprema":       f"Šifrarnik!$B$2:$B${len(PODKATEGORIJE_OPREMA)+1}",
        "NR_Podkat_Dijelovi":     f"Šifrarnik!$C$2:$C${len(PODKATEGORIJE_DIJELOVI)+1}",
        "NR_Brand_Oprema":        f"Šifrarnik!$D$2:$D${len(BRENDOVI_OPREMA)+1}",
        "NR_Brand_Dijelovi":      f"Šifrarnik!$E$2:$E${len(BRENDOVI_DIJELOVI)+1}",
    }

    # Obriši stare ako postoje, pa dodaj nove
    for name in list(named.keys()):
        if name in wb.defined_names:
            del wb.defined_names[name]
    for name, ref in named.items():
        wb.defined_names[name] = DefinedName(name, attr_text=ref)

    return named

# ── Dodaj padajuće izbornike u Proizvodi sheet ───────────────────────────────
def add_dropdowns(ws, named_ranges):
    MAX_ROW = 10000

    col_map = {}
    for ci in range(1, ws.max_column + 1):
        val = ws.cell(row=1, column=ci).value
        if val:
            col_map[str(val).strip()] = get_column_letter(ci)

    def make_dv(formula, prompt_title, prompt_body, error_msg):
        dv = DataValidation(
            type="list",
            formula1=formula,
            allow_blank=True,
            showDropDown=False,       # False = prikaži strelicu
            showInputMessage=True,
            promptTitle=prompt_title,
            prompt=prompt_body,
            showErrorMessage=True,
            errorTitle="Neispravna vrijednost",
            error=error_msg,
        )
        ws.add_data_validation(dv)
        return dv

    # category → Kategorija
    if "category" in col_map:
        col = col_map["category"]
        dv = make_dv(
            formula="NR_Kategorija",
            prompt_title="Kategorija",
            prompt_body="Odaberi: Oprema ili Dijelovi",
            error_msg='Mora biti "Oprema" ili "Dijelovi".',
        )
        dv.sqref = f"{col}2:{col}{MAX_ROW}"

    # subcategory → kombinirane podkategorije (Oprema + Dijelovi zajedno)
    # Napomena: da bi Excel imao sve u jednom dropdownu, stavljamo oba popisa
    # na Šifrarnik i referenciramo oba. Koristimo OFFSET trik ili jednostavno
    # pišemo sve vrijednosti direktno u formulu (max 255 znakova).
    all_subs = PODKATEGORIJE_OPREMA + [s for s in PODKATEGORIJE_DIJELOVI if s not in PODKATEGORIJE_OPREMA]
    if "subcategory" in col_map:
        col = col_map["subcategory"]
        # Ako ukupno znakova > 255, koristimo named range (samo Oprema+Dijelovi zajedno)
        inline = '"' + ",".join(all_subs) + '"'
        if len(inline) <= 255:
            formula = inline
        else:
            # Fallback: referenciramo Šifrarnik kolonu B (Oprema podkat.)
            # Korisnik može ručno odabrati i vrijednosti iz Dijelovi podkat.
            formula = "NR_Podkat_Oprema"

        dv = make_dv(
            formula=formula,
            prompt_title="Podkategorija",
            prompt_body="Odaberi podkategoriju ili upiši vlastitu",
            error_msg="",
        )
        dv.showErrorMessage = False
        dv.sqref = f"{col}2:{col}{MAX_ROW}"

    # brand → brand_id vrijednosti (svi brendovi)
    all_brands = [b[0] for b in BRENDOVI_OPREMA] + [b[0] for b in BRENDOVI_DIJELOVI]
    if "brand" in col_map:
        col = col_map["brand"]
        inline_b = '"' + ",".join(all_brands) + '"'
        formula_b = inline_b if len(inline_b) <= 255 else "NR_Brand_Oprema"
        dv_b = make_dv(
            formula=formula_b,
            prompt_title="Brand",
            prompt_body="Odaberi brand_id ili ostavi prazno",
            error_msg="",
        )
        dv_b.showErrorMessage = False
        dv_b.sqref = f"{col}2:{col}{MAX_ROW}"

    print(f"  Padajući izbornici dodani za: {', '.join(k for k in col_map if k in ('category','subcategory','brand'))}")

# ── AutoFilter na sheet ───────────────────────────────────────────────────────
def add_autofilter(ws):
    last_col = get_column_letter(ws.max_column)
    ws.auto_filter.ref = f"A1:{last_col}1"

# ── Kreira / puni sheet brendova ─────────────────────────────────────────────
def write_brand_sheet(wb, sheet_name, brendovi, header_color):
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    ws = wb.create_sheet(sheet_name)
    fill, font, center, border = header_style(header_color)
    db = data_border()

    for ci, col in enumerate(BRAND_HEADERS, start=1):
        cell = ws.cell(row=1, column=ci, value=col)
        cell.font = font; cell.fill = fill
        cell.alignment = center; cell.border = border

    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 28

    col_widths = {"brand_id": 14, "name": 25, "logo_folder": 16, "website": 28, "active": 10}
    for ri, row_data in enumerate(brendovi, start=2):
        row_fill = FILLS[ri % 2]
        for ci, val in enumerate(row_data, start=1):
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.fill = row_fill; cell.border = db
            cell.alignment = Alignment(vertical="center")
        ws.row_dimensions[ri].height = 18

    for ci, col in enumerate(BRAND_HEADERS, start=1):
        ws.column_dimensions[get_column_letter(ci)].width = col_widths[col]

    add_autofilter(ws)
    print(f"  Sheet '{sheet_name}': {len(brendovi)} brendova")

# ── Dodaj stupac 'brand' u Proizvodi sheet ───────────────────────────────────
def ensure_brand_column(ws):
    headers = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    if "brand" in headers:
        print("  Stupac 'brand' već postoji u sheetu Proizvodi")
        return
    next_col = ws.max_column + 1
    fill, font, center, border = header_style("1B5E20")
    cell = ws.cell(row=1, column=next_col, value="brand")
    cell.font = font; cell.fill = fill
    cell.alignment = center; cell.border = border
    db = data_border()
    for ri in range(2, ws.max_row + 1):
        c = ws.cell(row=ri, column=next_col, value="")
        c.border = db; c.alignment = Alignment(vertical="center")
    ws.column_dimensions[get_column_letter(next_col)].width = 14
    print(f"  Stupac 'brand' dodan u Proizvodi (kolona {get_column_letter(next_col)})")

# ── Kreira prazni Proizvodi sheet ako xlsx ne postoji ────────────────────────
def ensure_workbook():
    if os.path.exists(EXCEL_PATH):
        wb = openpyxl.load_workbook(EXCEL_PATH)
        print(f"Učitan: {EXCEL_PATH}")
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Proizvodi"
        PROD_HEADERS = ["id", "name", "category", "subcategory", "price",
                        "description", "image_folder", "is_new", "brand"]
        fill, font, center, border = header_style("1B5E20")
        for ci, col in enumerate(PROD_HEADERS, start=1):
            cell = ws.cell(row=1, column=ci, value=col)
            cell.font = font; cell.fill = fill
            cell.alignment = center; cell.border = border
        ws.freeze_panes = "A2"
        ws.row_dimensions[1].height = 30
        col_widths = {"id":5,"name":35,"category":12,"subcategory":18,
                      "price":16,"description":55,"image_folder":25,"is_new":8,"brand":14}
        for ci, col in enumerate(PROD_HEADERS, start=1):
            ws.column_dimensions[get_column_letter(ci)].width = col_widths.get(col, 15)
        print(f"Kreiran novi: {EXCEL_PATH}")
    return wb

# ── Upute sheet ───────────────────────────────────────────────────────────────
def ensure_upute(wb):
    if "Upute" not in wb.sheetnames:
        ws_u = wb.create_sheet("Upute")
    else:
        ws_u = wb["Upute"]

    upute = [
        ("UPUTE ZA UPRAVLJANJE OPREMOM I DIJELOVIMA", ""),
        ("", ""),
        ("STUPCI", ""),
        ("id",           "Redni broj — ne mijenjaj!"),
        ("name",         "Naziv proizvoda (npr. Kawasaki kaciga KRT)"),
        ("category",     "Padajući izbornik: Oprema   ili   Dijelovi"),
        ("subcategory",  "Padajući izbornik — ili upiši vlastito (Kacige / Jakne / Filteri…)"),
        ("price",        "Cijena npr: 149,90 € ili: Cijena na upit"),
        ("description",  "Kratki opis (1-2 rečenice)"),
        ("image_folder", "Naziv mape (npr. kaciga-krt) — slike idu u public/images/oprema/ ili public/images/dijelovi/"),
        ("is_new",       "TRUE = prikazuje se badge NOVO, FALSE = ne"),
        ("brand",        "Padajući izbornik — brand_id iz sheeta Brendovi_Oprema / Brendovi_Dijelovi"),
        ("", ""),
        ("ŠIFRARNIK SHEET", ""),
        ("Šifrarnik",    "Ovdje definiraš sve moguće kategorije, podkategorije i brendove za padajuće izbornike"),
        ("", ""),
        ("DODAVANJE PROIZVODA", ""),
        ("1.", "Dodaj novi red u Excel"),
        ("2.", "Ispuni stupce — category i brand odaberi iz padajućeg izbornika"),
        ("3.", "Napravi mapu public/images/oprema/{naziv-mape}/ i stavi slike"),
        ("4.", "Pokreni: py -X utf8 scripts/proizvodi_excel_to_json.py"),
        ("5.", "git add . && git commit -m 'Dodan proizvod' && git push"),
        ("", ""),
        ("NAPOMENA",     "Filter (strelice u zaglavlju) omogućava sortiranje i filtriranje unutar Excela"),
    ]

    ws_u.delete_rows(1, ws_u.max_row)
    for r, (a, b) in enumerate(upute, start=1):
        bold = bool(a and (a.isupper() or a.endswith(".")))
        ws_u.cell(row=r, column=1, value=a).font = Font(bold=bold, size=10 if a == upute[0][0] else 9)
        ws_u.cell(row=r, column=2, value=b)
    ws_u["A1"].font = Font(bold=True, size=13, color="1B5E20")
    ws_u.column_dimensions["A"].width = 22
    ws_u.column_dimensions["B"].width = 72

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    wb = ensure_workbook()

    # Proizvodi sheet
    if "Proizvodi" in wb.sheetnames:
        ws_prod = wb["Proizvodi"]
        ensure_brand_column(ws_prod)
        add_autofilter(ws_prod)
    else:
        print("  UPOZORENJE: Sheet 'Proizvodi' ne postoji — kreiranje preskočeno")
        ws_prod = None

    # Šifrarnik
    named_ranges = write_sifrarnik(wb)

    # Padajući izbornici
    if ws_prod is not None:
        add_dropdowns(ws_prod, named_ranges)

    # Brand sheetovi
    write_brand_sheet(wb, "Brendovi_Oprema",   BRENDOVI_OPREMA,   "E65100")
    write_brand_sheet(wb, "Brendovi_Dijelovi", BRENDOVI_DIJELOVI, "1565C0")

    # Upute
    ensure_upute(wb)

    # Spremi — pokušaj direktno, pa fallback na tmp
    tmp = EXCEL_PATH + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    try:
        wb.save(EXCEL_PATH)
        print(f"\nSačuvano: {EXCEL_PATH}")
    except PermissionError:
        wb.save(tmp)
        try:
            os.replace(tmp, EXCEL_PATH)
            print(f"\nSačuvano: {EXCEL_PATH}")
        except PermissionError:
            print(f"\nZATVORI Excel pa ručno zamijeni: {tmp} → {EXCEL_PATH}")
            return
    print("\nOtvori Excel — vidjet ćeš strelice filtera i padajuće izbornike.")


if __name__ == "__main__":
    main()
