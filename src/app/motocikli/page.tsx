"use client";

import { useState, useMemo, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import MotorcycleCard from "@/components/MotorcycleCard";
import FilterBar from "@/components/FilterBar";
import type { Motorcycle, Category } from "@/types/motorcycle";
import modelsData from "@/data/models.json";

const models = modelsData as unknown as Motorcycle[];

// Kategorije koje se prikazuju kada nema URL parametra (samo motocikli)
const MOTO_CATEGORIES: Category[] = [
  "Sport", "Naked", "Adventure", "Touring", "Classic", "Cruiser", "Offroad", "Električni", "Quad"
];

function MotocikliContent() {
  const searchParams = useSearchParams();
  const urlCategory = searchParams.get("category") as Category | null;

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState<Category>(urlCategory ?? "Sve");

  useEffect(() => {
    const cat = searchParams.get("category") as Category | null;
    setCategory(cat ?? "Sve");
  }, [searchParams]);

  // Ako je kategorija Mule ili Jet Ski — prikaži samo tu kategoriju
  // Ako je "Sve" bez URL parametra — prikaži samo motocikle (ne Mule/Jet Ski)
  const filtered = useMemo(() => {
    return models.filter((m) => {
      const isSpecial = m.category === "Mule" || m.category === "Jet Ski";

      let matchesCategory: boolean;
      if (category === "Mule" || category === "Jet Ski") {
        // Direktna kategorija iz nav linka
        matchesCategory = m.category === category;
      } else if (category === "Sve") {
        // "Sve" u motocikli sekciji = samo moto kategorije
        matchesCategory = urlCategory
          ? !isSpecial  // ako je dosao s URL-om ali category=Sve, ne prikazuj Mule/JetSki
          : MOTO_CATEGORIES.includes(m.category as Category);
      } else {
        matchesCategory = m.category === category;
      }

      const q = search.toLowerCase();
      const matchesSearch =
        !q ||
        m.name.toLowerCase().includes(q) ||
        m.category.toLowerCase().includes(q) ||
        m.description.toLowerCase().includes(q);

      return matchesCategory && matchesSearch;
    });
  }, [category, search, urlCategory]);

  // Naslov i podnaslov ovisno o odabranoj kategoriji
  const pageTitle =
    category === "Mule" ? "Kawasaki Mule" :
    category === "Jet Ski" ? "Kawasaki Jet Ski" :
    "Motocikli u ponudi";

  const pageSubtitle =
    category === "Mule" ? "Radna i višenamjenska vozila" :
    category === "Jet Ski" ? "Osobni plovni skuteri" :
    `Kawasaki motocikli i ATV — ${new Date().getFullYear()}`;

  // Kategorije za FilterBar — ovisno o kontekstu
  const visibleCategories: Category[] = (category === "Mule" || category === "Jet Ski")
    ? ["Sve", category]
    : ["Sve", ...MOTO_CATEGORIES];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-10">
        <h1 className="section-title">{pageTitle}</h1>
        <p className="section-subtitle">{pageSubtitle}</p>
      </div>

      {/* Filters */}
      <div className="mb-8">
        <FilterBar
          active={category}
          search={search}
          onCategory={setCategory}
          onSearch={setSearch}
          total={filtered.length}
          availableCategories={visibleCategories}
        />
      </div>

      {/* Grid */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {filtered.map((bike) => (
            <MotorcycleCard key={bike.id} bike={bike} />
          ))}
        </div>
      ) : (
        <div className="text-center py-24">
          <svg className="w-16 h-16 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{color:"var(--muted)"}}>
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-lg" style={{color:"var(--muted)"}}>Nema rezultata{search ? ` za "${search}"` : ""}</p>
          <button
            onClick={() => { setSearch(""); setCategory("Sve"); }}
            className="mt-4 text-sm hover:underline"
            style={{color:"var(--green-dk)"}}
          >
            Resetiraj filtre
          </button>
        </div>
      )}
    </div>
  );
}

export default function MotocikliPage() {
  return (
    <Suspense fallback={<div className="max-w-7xl mx-auto px-4 py-12" style={{color:"var(--muted)"}}>Učitavanje...</div>}>
      <MotocikliContent />
    </Suspense>
  );
}
