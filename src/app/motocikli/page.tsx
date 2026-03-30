"use client";

import { useState, useMemo, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import MotorcycleCard from "@/components/MotorcycleCard";
import FilterBar from "@/components/FilterBar";
import type { Motorcycle, Category } from "@/types/motorcycle";
import modelsData from "@/data/models.json";

const models = modelsData as Motorcycle[];

export default function MotocikliPage() {
  const searchParams = useSearchParams();
  const initialCategory = (searchParams.get("category") as Category) ?? "Sve";

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState<Category>(initialCategory);

  useEffect(() => {
    const cat = searchParams.get("category") as Category;
    if (cat) setCategory(cat);
  }, [searchParams]);

  const filtered = useMemo(() => {
    return models.filter((m) => {
      const matchesCategory = category === "Sve" || m.category === category;
      const q = search.toLowerCase();
      const matchesSearch =
        !q ||
        m.name.toLowerCase().includes(q) ||
        m.category.toLowerCase().includes(q) ||
        m.description.toLowerCase().includes(q);
      return matchesCategory && matchesSearch;
    });
  }, [category, search]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-10">
        <h1 className="section-title">Motocikli u ponudi</h1>
        <p className="section-subtitle">
          Kawasaki novi modeli — cijene za {new Date().getFullYear()}
        </p>
      </div>

      {/* Filters */}
      <div className="mb-8">
        <FilterBar
          active={category}
          search={search}
          onCategory={setCategory}
          onSearch={setSearch}
          total={filtered.length}
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
          <svg className="w-16 h-16 text-gray-700 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-gray-500 text-lg">Nema rezultata za &quot;{search}&quot;</p>
          <button
            onClick={() => { setSearch(""); setCategory("Sve"); }}
            className="mt-4 text-orange-500 hover:text-orange-400 text-sm"
          >
            Resetiraj filtre
          </button>
        </div>
      )}
    </div>
  );
}
