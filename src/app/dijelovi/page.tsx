"use client";

import { useState, useMemo } from "react";
import ProductCard from "@/components/ProductCard";
import BrandsGrid from "@/components/BrandsGrid";
import type { Product } from "@/types/product";
import productsData from "@/data/products.json";

const allProducts = productsData as unknown as Product[];
const products = allProducts.filter(p => p.category === "Dijelovi");

// Prikupi sve podkategorije
const ALL_SUBS = ["Sve", ...Array.from(new Set(products.map(p => p.subcategory).filter(Boolean)))];

export default function DijeloviPage() {
  const [search, setSearch]   = useState("");
  const [sub, setSub]         = useState("Sve");

  const filtered = useMemo(() => {
    return products.filter(p => {
      const matchesSub    = sub === "Sve" || p.subcategory === sub;
      const q             = search.toLowerCase();
      const matchesSearch = !q || p.name.toLowerCase().includes(q) || p.description.toLowerCase().includes(q);
      return matchesSub && matchesSearch;
    });
  }, [sub, search]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-10">
        <h1 className="section-title">Dijelovi</h1>
        <p className="section-subtitle">Originalni Kawasaki dijelovi i potrošni materijal</p>
      </div>

      {/* Brendovi */}
      <BrandsGrid category="dijelovi" />

      {/* Filters */}
      <div className="mb-8 space-y-4">
        {/* Search */}
        <div className="relative">
          <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style={{ color: "var(--muted)" }}
            fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Pretraži dijelove..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full rounded-lg pl-10 pr-4 py-3 text-sm focus:outline-none"
            style={{ background: "var(--surface)", border: "1px solid var(--line)", color: "var(--text)" }}
          />
        </div>
        {/* Subcategory chips */}
        {ALL_SUBS.length > 1 && (
          <div className="flex flex-wrap gap-2">
            {ALL_SUBS.map(s => (
              <button key={s} onClick={() => setSub(s)}
                className="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
                style={sub === s
                  ? { background: "var(--green)", color: "white", boxShadow: "0 4px 12px rgba(55,182,58,.3)" }
                  : { background: "var(--surface)", border: "1px solid var(--line)", color: "var(--muted)" }
                }>
                {s}
              </button>
            ))}
          </div>
        )}
        <p className="text-sm" style={{ color: "var(--muted)" }}>
          Pronađeno <span className="font-semibold" style={{ color: "var(--green-dk)" }}>{filtered.length}</span> proizvoda
        </p>
      </div>

      {/* Grid */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {filtered.map(p => <ProductCard key={p.id} product={p} />)}
        </div>
      ) : (
        <div className="text-center py-24">
          <p className="text-lg" style={{ color: "var(--muted)" }}>
            {products.length === 0
              ? "Dijelovi uskoro dostupni. Kontaktirajte nas za informacije."
              : `Nema rezultata${search ? ` za "${search}"` : ""}`}
          </p>
          {products.length === 0 && (
            <a href="/kontakt" className="btn-primary inline-flex mt-6">
              Kontaktirajte nas
            </a>
          )}
        </div>
      )}
    </div>
  );
}
