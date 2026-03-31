"""
Dodaje sheetove Brendovi_Oprema i Brendovi_Dijelovi u proizvodi.xlsx.
Ako xlsx ne postoji, kreira ga sa praznim Proizvodima.
Dodaje stupac 'brand' u sheet Proizvodi ako već ne postoji.

Pokreni JEDNOM za inicijalizaciju:
    py -X utf8 scripts/kreiraj_excel_predlozak.py
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.join(SCRIPT_DIR, "..")
EXCEL_PATH = os.path.join(ROOT_DIR, "proizvodi.xlsx")

# ── Podaci brendova ─────────────────────────────────────────────────────────
BRENDOVI_OPREMA = [
    ("wind",     "WIND Raceware",      "wind",     "wind-raceware.com",  True),
    ("airoh",    "Airoh",              "airoh",    "airoh.com",          True),
    ("progrip",  "Progrip",            "progrip",  "progrip.it",         True),
    ("mitas",    "Mitas",              "mitas",    "mitas-moto.com",     True),
    ("motul",    "Motul",              "motul",    "motul.com",          True),
    ("valvoline","Valvoline",          "valvoline","valvoline.com",      True),
]

BRENDOVI_DIJELOVI = [
    ("prox",    "Pro-X Racing Parts",  "prox",    "pro-x.com",          True),
    ("wiseco",  "Wiseco",              "wiseco",  "wiseco.com",         True),
    ("wrp",     "WRP",                 "wrp",     "wrp-racing.com",     True),
    ("cht",     "CHT Sprockets",       "cht",     "cht-sprockets.com",  True),
    ("rk",      "RK Chains",           "rk",      "rk-chain.com",       True),
    ("trw",     "TRW Lucas",           "trw",     "trwaftermarket.com", True),
    ("denso",   "Denso",               "denso",   "denso.com",          True),
]

BRAND_HEADERS = ["brand_id", "name", "logo_folder", "website", "active"]

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

# ── Kreira / puni sheet brendova ─────────────────────────────────────────────
def write_brand_sheet(wb, sheet_name, brendovi, header_color):
    # Ukloni stari sheet ako postoji
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]

    ws = wb.create_sheet(sheet_name)
    fill, font, center, border = header_style(header_color)
    db = data_border()

    # Zaglavlje
    for ci, col in enumerate(BRAND_HEADERS, start=1):
        cell = ws.cell(row=1, column=ci, value=col)
        cell.font = font
        cell.fill = fill
        cell.alignment = center
        cell.border = border

    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 28

    # Podaci
    col_widths = {"brand_id": 14, "name": 25, "logo_folder": 16, "website": 28, "active": 10}
    for ri, row_data in enumerate(brendovi, start=2):
        row_fill = FILLS[ri % 2]
        for ci, val in enumerate(row_data, start=1):
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.fill = row_fill
            cell.border = db
            cell.alignment = Alignment(vertical="center")
        ws.row_dimensions[ri].height = 18

    for ci, col in enumerate(BRAND_HEADERS, start=1):
        ws.column_dimensions[get_column_letter(ci)].width = col_widths[col]

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
    cell.font = font
    cell.fill = fill
    cell.alignment = center
    cell.border = border

    db = data_border()
    for ri in range(2, ws.max_row + 1):
        cell = ws.cell(row=ri, column=next_col, value="")
        cell.border = db
        cell.alignment = Alignment(vertical="center")

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
        from openpyxl.utils import get_column_letter
        for ci, col in enumerate(PROD_HEADERS, start=1):
            ws.column_dimensions[get_column_letter(ci)].width = col_widths.get(col, 15)
        print(f"Kreiran novi: {EXCEL_PATH}")
    return wb

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    wb = ensure_workbook()

    # Dodaj stupac brand u Proizvodi
    if "Proizvodi" in wb.sheetnames:
        ensure_brand_column(wb["Proizvodi"])

    # Dodaj/zamijeni brand sheetove
    write_brand_sheet(wb, "Brendovi_Oprema",   BRENDOVI_OPREMA,   "E65100")
    write_brand_sheet(wb, "Brendovi_Dijelovi", BRENDOVI_DIJELOVI, "1565C0")

    # Dodaj/ažuriraj Upute sheet
    if "Upute" not in wb.sheetnames:
        ws_u = wb.create_sheet("Upute")
    else:
        ws_u = wb["Upute"]

    upute_extra = [
        ("", ""),
        ("BRENDOVI", ""),
        ("brand",         "brand_id iz sheeta Brendovi_Oprema ili Brendovi_Dijelovi (npr. airoh, motul)"),
        ("Brendovi_Oprema",   "→ Lista brendova za kategoriju Oprema"),
        ("Brendovi_Dijelovi", "→ Lista brendova za kategoriju Dijelovi"),
        ("logo_folder",   "Mapa za logo: public/images/brendovi/{logo_folder}.png"),
        ("", ""),
        ("BRENDOVI STRANICE", ""),
        ("/oprema/{brand_id}",   "→ Prikazuje sve Oprema proizvode tog brenda"),
        ("/dijelovi/{brand_id}", "→ Prikazuje sve Dijelovi proizvode tog brenda"),
    ]

    # Dodaj na kraj Uputa
    start_row = ws_u.max_row + 1
    for r, (a, b) in enumerate(upute_extra, start=start_row):
        ws_u.cell(row=r, column=1, value=a).font = Font(bold=bool(a and a.isupper()))
        ws_u.cell(row=r, column=2, value=b)

    import tempfile, shutil
    tmp = EXCEL_PATH + ".tmp"
    wb.save(tmp)
    shutil.move(tmp, EXCEL_PATH)
    print(f"\nSačuvano: {EXCEL_PATH}")
    print("\nSljedeći korak:")
    print("  py -X utf8 scripts/proizvodi_excel_to_json.py")


if __name__ == "__main__":
    main()
