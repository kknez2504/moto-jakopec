"use client";

import { CATEGORIES, type Category } from "@/types/motorcycle";

interface Props {
  active: Category;
  search: string;
  onCategory: (c: Category) => void;
  onSearch: (v: string) => void;
  total: number;
}

export default function FilterBar({ active, search, onCategory, onSearch, total }: Props) {
  return (
    <div className="space-y-4">
      {/* Search */}
      <div className="relative">
        <svg
          className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500"
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          placeholder="Pretraži modele..."
          value={search}
          onChange={(e) => onSearch(e.target.value)}
          className="w-full bg-[#161616] border border-[#2a2a2a] rounded-lg pl-10 pr-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-orange-500 transition-colors text-sm"
        />
        {search && (
          <button
            onClick={() => onSearch("")}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* Category chips */}
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => onCategory(cat)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
              active === cat
                ? "bg-orange-500 text-white shadow-lg shadow-orange-500/25"
                : "bg-[#161616] border border-[#2a2a2a] text-gray-400 hover:border-orange-500/50 hover:text-white"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Result count */}
      <p className="text-gray-500 text-sm">
        Pronađeno{" "}
        <span className="text-orange-500 font-semibold">{total}</span>{" "}
        {total === 1 ? "model" : "modela"}
      </p>
    </div>
  );
}
