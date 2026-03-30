import Link from "next/link";
import Image from "next/image";
import type { Motorcycle } from "@/types/motorcycle";

interface Props {
  bike: Motorcycle;
}

export default function MotorcycleCard({ bike }: Props) {
  const imageSrc = bike.images?.[0] ?? null;

  return (
    <Link
      href={`/motocikli/${bike.id}`}
      className="card group flex flex-col transition-all duration-300 hover:-translate-y-1"
      style={{ boxShadow: "0 4px 20px rgba(0,0,0,.06)" }}
      onMouseEnter={e => (e.currentTarget.style.boxShadow = "0 8px 30px rgba(55,182,58,.18)")}
      onMouseLeave={e => (e.currentTarget.style.boxShadow = "0 4px 20px rgba(0,0,0,.06)")}
    >
      {/* Image */}
      <div className="relative aspect-[16/9] overflow-hidden" style={{ background: "var(--bg2)" }}>
        {imageSrc ? (
          <Image
            src={imageSrc}
            alt={bike.name}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-500"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <svg className="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: "var(--muted)" }}>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}

        {/* Badges */}
        <div className="absolute top-3 left-3 flex gap-2">
          {bike.is_new && (
            <span className="text-white text-xs font-bold px-2 py-1 rounded" style={{ background: "var(--green)" }}>
              NOVO
            </span>
          )}
          {bike.license_category && (
            <span className="text-xs font-semibold px-2 py-1 rounded" style={{ background: "rgba(255,255,255,.85)", color: "var(--text)" }}>
              {bike.license_category}
            </span>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-4 flex flex-col flex-1">
        <div className="flex items-start justify-between gap-2 mb-2">
          <h3 className="font-bold text-base leading-tight transition-colors" style={{ color: "var(--text)" }}>
            {bike.name}
          </h3>
          <span className="text-xs font-medium px-2 py-0.5 rounded border shrink-0" style={{ background: "rgba(55,182,58,.1)", color: "var(--green-dk)", borderColor: "rgba(55,182,58,.25)" }}>
            {bike.category}
          </span>
        </div>

        <p className="text-sm line-clamp-2 flex-1 mb-4" style={{ color: "var(--muted)" }}>
          {bike.description}
        </p>

        <div className="flex items-center justify-between mt-auto pt-3 border-t" style={{ borderColor: "var(--line)" }}>
          <span className="font-bold text-lg" style={{ color: "var(--green-dk)" }}>
            {bike.price}
          </span>
          <span className="text-xs flex items-center gap-1 transition-colors" style={{ color: "var(--muted)" }}>
            Više detalja
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </span>
        </div>
      </div>
    </Link>
  );
}
