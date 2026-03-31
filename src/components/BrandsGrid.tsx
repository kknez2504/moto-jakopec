"use client";

import Link from "next/link";
import Image from "next/image";
import type { Brand, BrandsData } from "@/types/brand";
import brandsData from "@/data/brands.json";

interface Props {
  category: "oprema" | "dijelovi";
}

export default function BrandsGrid({ category }: Props) {
  const data = brandsData as unknown as BrandsData;
  const brands: Brand[] = (data[category] ?? []).filter(b => b.active);

  if (brands.length === 0) return null;

  return (
    <section className="mb-10">
      <h2 className="text-sm font-semibold uppercase tracking-widest mb-4" style={{ color: "var(--muted)" }}>
        Brendovi
      </h2>
      <div className="flex flex-wrap gap-3">
        {brands.map(brand => (
          <Link
            key={brand.brand_id}
            href={`/${category}/${brand.brand_id}`}
            className="group flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200"
            style={{
              background: "var(--surface)",
              border: "1px solid var(--line)",
              boxShadow: "0 2px 8px rgba(0,0,0,.06)",
            }}
            onMouseEnter={e => {
              (e.currentTarget as HTMLElement).style.borderColor = "#f59e0b";
              (e.currentTarget as HTMLElement).style.boxShadow = "0 4px 16px rgba(245,158,11,.2)";
            }}
            onMouseLeave={e => {
              (e.currentTarget as HTMLElement).style.borderColor = "var(--line)";
              (e.currentTarget as HTMLElement).style.boxShadow = "0 2px 8px rgba(0,0,0,.06)";
            }}
          >
            {brand.logo ? (
              <div className="relative w-10 h-10 flex-shrink-0 transition-opacity group-hover:opacity-80">
                <Image
                  src={brand.logo}
                  alt={brand.name}
                  fill
                  unoptimized={/\.(svg|ico)$/.test(brand.logo)}
                  className="object-contain"
                  sizes="40px"
                />
              </div>
            ) : (
              <div className="w-10 h-10 flex-shrink-0 rounded flex items-center justify-center text-xs font-bold"
                style={{ background: "var(--bg2)", color: "var(--muted)" }}>
                {brand.name.slice(0, 2).toUpperCase()}
              </div>
            )}
            <span className="font-medium text-sm transition-colors group-hover:text-amber-500"
              style={{ color: "var(--text)" }}>
              {brand.name}
            </span>
          </Link>
        ))}
      </div>
    </section>
  );
}
