import Link from "next/link";
import Image from "next/image";
import type { Motorcycle } from "@/types/motorcycle";

const CATEGORY_COLORS: Record<string, string> = {
  Sport:     "bg-red-500/20 text-red-400 border-red-500/30",
  Naked:     "bg-purple-500/20 text-purple-400 border-purple-500/30",
  Adventure: "bg-green-500/20 text-green-400 border-green-500/30",
  Touring:   "bg-blue-500/20 text-blue-400 border-blue-500/30",
  Classic:   "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  Cruiser:   "bg-orange-500/20 text-orange-400 border-orange-500/30",
  Offroad:   "bg-lime-500/20 text-lime-400 border-lime-500/30",
};

interface Props {
  bike: Motorcycle;
}

export default function MotorcycleCard({ bike }: Props) {
  const categoryStyle =
    CATEGORY_COLORS[bike.category] ?? "bg-gray-500/20 text-gray-400 border-gray-500/30";

  const imageSrc = bike.images?.[0] ?? null;

  return (
    <Link
      href={`/motocikli/${bike.id}`}
      className="card group flex flex-col hover:border-orange-500/50 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-orange-500/10"
    >
      {/* Image */}
      <div className="relative aspect-[16/9] bg-[#1a1a1a] overflow-hidden">
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
            <svg className="w-16 h-16 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
                d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
          </div>
        )}

        {/* Badges */}
        <div className="absolute top-3 left-3 flex gap-2">
          {bike.is_new && (
            <span className="bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded">
              NOVO
            </span>
          )}
          {bike.license_category && (
            <span className="bg-black/70 text-white text-xs font-semibold px-2 py-1 rounded">
              {bike.license_category}
            </span>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-4 flex flex-col flex-1">
        <div className="flex items-start justify-between gap-2 mb-2">
          <h3 className="font-bold text-white text-base leading-tight group-hover:text-orange-400 transition-colors">
            {bike.name}
          </h3>
          <span className={`text-xs font-medium px-2 py-0.5 rounded border shrink-0 ${categoryStyle}`}>
            {bike.category}
          </span>
        </div>

        <p className="text-gray-500 text-sm line-clamp-2 flex-1 mb-4">
          {bike.description}
        </p>

        <div className="flex items-center justify-between mt-auto pt-3 border-t border-[#2a2a2a]">
          <span className="text-orange-500 font-bold text-lg">
            {bike.price}
          </span>
          <span className="text-xs text-gray-500 group-hover:text-orange-500 transition-colors flex items-center gap-1">
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
