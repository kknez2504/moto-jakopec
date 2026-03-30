# Moto Jakopec — Setup upute

## Stack
- **Next.js 14** (React framework, SSR/SSG)
- **TypeScript** (type safety)
- **Tailwind CSS** (stilizacija)
- **Vercel** (besplatni hosting)

---

## 1. Preduvjeti

Instaliraj ako već nemaš:
- [Node.js](https://nodejs.org/) — preuzmi LTS verziju (18+)
- [Git](https://git-scm.com/)
- [VS Code](https://code.visualstudio.com/) (preporučeno)

Provjeri instalaciju:
```bash
node --version   # treba biti 18+
npm --version
git --version
```

---

## 2. GitHub repozitorij

1. Idi na [github.com](https://github.com) → **New repository**
2. Naziv: `moto-jakopec` (ili što god želiš)
3. Vidljivost: **Private** (dok ne bude gotovo) ili **Public**
4. NE dodavaj README, .gitignore niti license (već ih imamo)
5. Klikni **Create repository**
6. Kopiraj URL repozitorija (npr. `https://github.com/TVOJE_IME/moto-jakopec.git`)

---

## 3. Inicijalizacija projekta

Otvori terminal u folderu projekta (`moto-jakopec-novo`):

```bash
# Inicijaliziraj git
git init
git add .
git commit -m "Initial commit — Moto Jakopec website"

# Poveži s GitHubom (zalijepite URL koji ste kopirali u koraku 2)
git remote add origin https://github.com/TVOJE_IME/moto-jakopec.git
git branch -M main
git push -u origin main
```

---

## 4. Instaliraj dependencies i pokreni lokalno

```bash
npm install
npm run dev
```

Otvori browser: **http://localhost:3000**

---

## 5. Deploy na Vercel (besplatno)

1. Idi na [vercel.com](https://vercel.com) → **Sign up with GitHub**
2. Klikni **Add New Project**
3. Odaberi tvoj `moto-jakopec` repozitorij
4. Framework: **Next.js** (automatski detektira)
5. Klikni **Deploy**

Tvoja stranica će biti live za ~2 minute na URL-u poput:
`https://moto-jakopec.vercel.app`

Svaki `git push` automatski deployjira novu verziju!

---

## 6. Ažuriranje podataka s dks.si

```bash
# Instaliraj Python dependencies (samo prvi put)
pip install requests beautifulsoup4 lxml

# Scrape i napiši novi models.json
python scripts/dks_scraper.py

# Ili spoji s postojećim (čuva slike i specs)
python scripts/dks_scraper.py --merge

# Commitaj promjene
git add src/data/models.json
git commit -m "Update Kawasaki prices from dks.si"
git push
```

---

## 7. Što trebaš prilagoditi

Otvori ove datoteke i zamijeni placeholder podatke:

| Datoteka | Što promijeniti |
|----------|-----------------|
| `src/components/Header.tsx` | Telefon: `+385 49 123 456` |
| `src/components/Footer.tsx` | Adresa, telefon, email |
| `src/app/kontakt/page.tsx` | Adresa, telefon, email |
| `src/app/layout.tsx` | SEO description, keywords |

---

## 8. Dodavanje slika

Slike spremi u `public/images/` i referenciraj ih u `models.json`:

```json
{
  "images": [
    "/images/kawasaki-z900-1.jpg",
    "/images/kawasaki-z900-2.jpg"
  ]
}
```

---

## Struktura projekta

```
moto-jakopec/
├── src/
│   ├── app/
│   │   ├── layout.tsx          ← HTML shell, Header, Footer
│   │   ├── page.tsx            ← Početna stranica
│   │   ├── globals.css         ← Globalni stilovi
│   │   ├── motocikli/
│   │   │   ├── page.tsx        ← Lista svih motocikala
│   │   │   └── [id]/page.tsx   ← Detalji pojedinog modela
│   │   └── kontakt/page.tsx    ← Kontakt stranica
│   ├── components/
│   │   ├── Header.tsx          ← Navigacija
│   │   ├── Footer.tsx          ← Footer
│   │   ├── MotorcycleCard.tsx  ← Kartica motocikla
│   │   └── FilterBar.tsx       ← Filter + search
│   ├── data/
│   │   └── models.json         ← SVI podaci o motociklima
│   └── types/
│       └── motorcycle.ts       ← TypeScript tipovi
├── scripts/
│   └── dks_scraper.py          ← Scraper za dks.si cijene
└── public/
    └── images/                 ← Slike motocikala
```
