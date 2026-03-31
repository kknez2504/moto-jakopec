"use client";

import { CATEGORIES, type Category } from "@/types/motorcycle";

interface Props {
  active: Category;
  search: string;
  onCategory: (c: Category) => void;
  onSearch: (v: string) => void;
  total: number;
  availableCategories?: Category[];
}

export default function FilterBar({ active, search, onCategory, onSearch, total, availableCategories }: Props) {
  const cats = availableCategories ?? CATEGORIES;

  return (
    <div className="space-y-4">
      {/* Search */}
      <div className="relative">
        <svg
          className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4"
          style={{ color: "var(--muted)" }}
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
          className="w-full rounded-lg pl-10 pr-4 py-3 text-sm focus:outline-none transition-colors"
          style={{
            background: "var(--surface)",
            border: "1px solid var(--line)",
            color: "var(--text)",
          }}
        />
        {search && (
          <button
            onClick={() => onSearch("")}
            className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors"
            style={{ color: "var(--muted)" }}
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* Category chips */}
      <div className="flex flex-wrap gap-2">
        {cats.map((cat) => (
          <button
            key={cat}
            onClick={() => onCategory(cat)}
            className="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
            style={
              active === cat
                ? { background: "var(--green)", color: "white", boxShadow: "0 4px 12px rgba(55,182,58,.3)" }
                : { background: "var(--surface)", border: "1px solid var(--line)", color: "var(--muted)" }
            }
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Result count */}
      <p className="text-sm" style={{ color: "var(--muted)" }}>
        Pronađeno{" "}
        <span className="font-semibold" style={{ color: "var(--green-dk)" }}>{total}</span>{" "}
        {total === 1 ? "vozilo" : total >= 2 && total <= 4 ? "vozila" : "vozila"}
      </p>
    </div>
  );
}
