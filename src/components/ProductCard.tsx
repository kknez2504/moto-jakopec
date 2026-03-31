"use client";

import Link from "next/link";
import Image from "next/image";
import type { Product } from "@/types/product";

interface Props {
  product: Product;
}

export default function ProductCard({ product }: Props) {
  const imageSrc = product.images?.[0] ?? null;
  const href = `/katalog/${product.category.toLowerCase()}/${product.id}`;

  return (
    <div
      className="card group flex flex-col transition-all duration-300 hover:-translate-y-1"
      style={{ boxShadow: "0 4px 20px rgba(0,0,0,.06)" }}
      onMouseEnter={e => (e.currentTarget.style.boxShadow = "0 8px 30px rgba(55,182,58,.18)")}
      onMouseLeave={e => (e.currentTarget.style.boxShadow = "0 4px 20px rgba(0,0,0,.06)")}
    >
      {/* Image */}
      <div className="relative aspect-[4/3] overflow-hidden" style={{ background: "var(--bg2)" }}>
        {imageSrc ? (
          <Image
            src={imageSrc}
            alt={product.name}
            fill
            className="object-contain group-hover:scale-105 transition-transform duration-500 p-2"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <svg className="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: "var(--muted)" }}>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
                d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
        )}

        {/* Badges */}
        <div className="absolute top-3 left-3 flex gap-2">
          {product.is_new && (
            <span className="text-white text-xs font-bold px-2 py-1 rounded" style={{ background: "var(--green)" }}>
              NOVO
            </span>
          )}
          {product.subcategory && (
            <span className="text-xs font-semibold px-2 py-1 rounded" style={{ background: "rgba(255,255,255,.85)", color: "var(--text)" }}>
              {product.subcategory}
            </span>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-4 flex flex-col flex-1">
        <h3 className="font-bold text-base leading-tight mb-2 transition-colors" style={{ color: "var(--text)" }}>
          {product.name}
        </h3>

        <p className="text-sm line-clamp-2 flex-1 mb-4" style={{ color: "var(--muted)" }}>
          {product.description}
        </p>

        <div className="flex items-center justify-between mt-auto pt-3 border-t" style={{ borderColor: "var(--line)" }}>
          <span className="font-bold text-lg" style={{ color: "var(--green-dk)" }}>
            {product.price}
          </span>
          <a
            href={`mailto:moto.jakopec@gmail.com?subject=Upit: ${encodeURIComponent(product.name)}`}
            className="text-xs flex items-center gap-1 transition-colors hover:underline"
            style={{ color: "var(--muted)" }}
          >
            Pošalji upit
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </a>
        </div>
      </div>
    </div>
  );
}
