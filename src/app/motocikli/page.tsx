"use client";

import { useState, useMemo, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import MotorcycleCard from "@/components/MotorcycleCard";
import FilterBar from "@/components/FilterBar";
import type { Motorcycle, Category } from "@/types/motorcycle";
import modelsData from "@/data/models.json";

const models = modelsData as unknown as Motorcycle[];

// Kategorije koje se prikazuju kada nema URL parametra (samo motocikli, bez Quad/Mule/Jet Ski)
const MOTO_CATEGORIES: Category[] = [
  "Sport", "Naked", "Adventure", "Touring", "Classic", "Cruiser", "Offroad", "Električni"
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
  // Posebne kategorije koje imaju vlastiti nav link (ne prikazuju se pod "Motocikli")
  const SPECIAL_CATEGORIES = ["Quad", "Mule", "Jet Ski"];

  const filtered = useMemo(() => {
    return models.filter((m) => {
      let matchesCategory: boolean;
      if (SPECIAL_CATEGORIES.includes(category)) {
        // Direktna posebna kategorija iz nav linka
        matchesCategory = m.category === category;
      } else if (category === "Sve") {
        // "Sve" u motocikli sekciji = samo moto kategorije (bez Quad/Mule/Jet Ski)
        matchesCategory = MOTO_CATEGORIES.includes(m.category as Category);
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
  }, [category, search]);

  // Naslov i podnaslov ovisno o odabranoj kategoriji
  const pageTitle =
    category === "Quad"    ? "Kawasaki Quad" :
    category === "Mule"    ? "Kawasaki Mule" :
    category === "Jet Ski" ? "Kawasaki Jet Ski" :
    "Motocikli u ponudi";

  const pageSubtitle =
    category === "Quad"    ? "ATV četverocikli za sport i teren" :
    category === "Mule"    ? "Radna i višenamjenska vozila" :
    category === "Jet Ski" ? "Osobni plovni skuteri" :
    `Kawasaki motocikli — ${new Date().getFullYear()}`;

  // Kategorije za FilterBar — ovisno o kontekstu
  const visibleCategories: Category[] = SPECIAL_CATEGORIES.includes(category)
    ? ["Sve", category as Category]
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
