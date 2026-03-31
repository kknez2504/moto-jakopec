import { notFound } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import ProductCard from "@/components/ProductCard";
import type { Brand, BrandsData } from "@/types/brand";
import type { Product } from "@/types/product";
import brandsData from "@/data/brands.json";
import productsData from "@/data/products.json";

const allBrands = brandsData as unknown as BrandsData;
const allProducts = productsData as unknown as Product[];

export function generateStaticParams() {
  return (allBrands.dijelovi ?? [])
    .filter(b => b.active)
    .map(b => ({ brand: b.brand_id }));
}

interface Props {
  params: { brand: string };
}

export default function DijeloviBrend({ params }: Props) {
  const brand: Brand | undefined = (allBrands.dijelovi ?? []).find(
    b => b.brand_id === params.brand
  );

  if (!brand) notFound();

  const products = allProducts.filter(
    p => p.category === "Dijelovi" && p.brand === params.brand
  );

  // Grupiraj po subcategory
  const groups = products.reduce<Record<string, Product[]>>((acc, p) => {
    const key = p.subcategory || "Ostalo";
    if (!acc[key]) acc[key] = [];
    acc[key].push(p);
    return acc;
  }, {});
  const subcategories = Object.keys(groups).sort();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Natrag */}
      <Link
        href="/dijelovi"
        className="inline-flex items-center gap-2 text-sm mb-8 transition-colors hover:underline"
        style={{ color: "var(--muted)" }}
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Svi brendovi
      </Link>

      {/* Brand header */}
      <div className="flex items-center gap-6 mb-10">
        {brand.logo && (
          <div className="relative w-20 h-20 flex-shrink-0">
            <Image
              src={brand.logo}
              alt={brand.name}
              fill
              unoptimized={brand.logo.endsWith(".svg")}
              className="object-contain"
              sizes="80px"
            />
          </div>
        )}
        <div>
          <h1 className="section-title mb-1">{brand.name}</h1>
          {brand.website && (
            <a
              href={`https://${brand.website}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm transition-colors hover:underline"
              style={{ color: "var(--muted)" }}
            >
              {brand.website}
            </a>
          )}
        </div>
      </div>

      {/* Proizvodi */}
      {products.length === 0 ? (
        <div className="text-center py-24">
          <p className="text-lg" style={{ color: "var(--muted)" }}>
            Nema proizvoda za ovaj brend. Kontaktirajte nas za dostupnost.
          </p>
          <a href="/kontakt" className="btn-primary inline-flex mt-6">
            Kontaktirajte nas
          </a>
        </div>
      ) : (
        <div className="space-y-12">
          {subcategories.map(sub => (
            <section key={sub}>
              <h2 className="text-lg font-semibold mb-5 pb-2 border-b" style={{ color: "var(--text)", borderColor: "var(--line)" }}>
                {sub}
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
                {groups[sub].map(p => <ProductCard key={p.id} product={p} />)}
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  );
}
