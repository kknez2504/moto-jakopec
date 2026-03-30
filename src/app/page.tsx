import Link from "next/link";
import MotorcycleCard from "@/components/MotorcycleCard";
import type { Motorcycle } from "@/types/motorcycle";
import modelsData from "@/data/models.json";

const models = modelsData as Motorcycle[];

const FEATURED_COUNT = 6;

const CATEGORIES_INFO = [
  { name: "Sport",     icon: "🏁", desc: "Supersport & track motocikli" },
  { name: "Naked",     icon: "⚡", desc: "Street naked & roadster" },
  { name: "Adventure", icon: "🌍", desc: "On/off road avanturisti" },
  { name: "Touring",   icon: "🛣️", desc: "Dugopružni touring modeli" },
  { name: "Classic",   icon: "🏛️", desc: "Modern classic stil" },
  { name: "Cruiser",   icon: "🤙", desc: "Urban cruiser modeli" },
];

export default function HomePage() {
  const featured = models.filter((m) => m.is_new).slice(0, FEATURED_COUNT);
  const display = featured.length >= 3 ? featured : models.slice(0, FEATURED_COUNT);

  return (
    <>
      {/* ── Hero ─────────────────────────────────────────────────────── */}
      <section className="relative min-h-[85vh] flex items-center overflow-hidden">
        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#0f0f0f] via-[#1a0f0a] to-[#0f0f0f]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_rgba(249,115,22,0.15)_0%,_transparent_60%)]" />

        {/* Grid pattern */}
        <div
          className="absolute inset-0 opacity-5"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.1) 1px, transparent 1px)",
            backgroundSize: "50px 50px",
          }}
        />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="max-w-2xl">
            <span className="inline-flex items-center gap-2 bg-orange-500/10 border border-orange-500/30 text-orange-400 text-sm font-medium px-3 py-1 rounded-full mb-6">
              <span className="w-1.5 h-1.5 bg-orange-500 rounded-full animate-pulse" />
              Ovlašteni Kawasaki zastupnik
            </span>

            <h1 className="text-5xl md:text-7xl font-black text-white leading-[1.05] mb-6">
              Vaš put{" "}
              <span className="text-orange-500">počinje</span>{" "}
              ovdje.
            </h1>

            <p className="text-gray-400 text-xl leading-relaxed mb-8 max-w-xl">
              Kawasaki specijalist u Hrvatskoj. Novi motocikli, servis,
              rezervni dijelovi i oprema — sve na jednom mjestu.
            </p>

            <div className="flex flex-wrap gap-4">
              <Link href="/motocikli" className="btn-primary text-base px-8 py-4">
                Pregledaj ponudu
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
              <Link href="/kontakt" className="btn-outline text-base px-8 py-4">
                Kontaktiraj nas
              </Link>
            </div>

            {/* Stats */}
            <div className="flex flex-wrap gap-8 mt-12 pt-8 border-t border-[#2a2a2a]">
              {[
                { value: `${models.length}+`, label: "Modela u ponudi" },
                { value: "20+",              label: "Godina iskustva" },
                { value: "Kawasaki",          label: "Ovlašteni zastupnik" },
              ].map((stat) => (
                <div key={stat.label}>
                  <div className="text-2xl font-bold text-orange-500">{stat.value}</div>
                  <div className="text-sm text-gray-500">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Featured bikes ───────────────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="flex items-end justify-between mb-10">
          <div>
            <h2 className="section-title">Istaknuti modeli</h2>
            <p className="section-subtitle">Novosti i najpopularniji modeli</p>
          </div>
          <Link href="/motocikli" className="text-orange-500 hover:text-orange-400 text-sm font-medium flex items-center gap-1 transition-colors">
            Svi modeli
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {display.map((bike) => (
            <MotorcycleCard key={bike.id} bike={bike} />
          ))}
        </div>
      </section>

      {/* ── Categories ───────────────────────────────────────────────── */}
      <section className="bg-[#0a0a0a] border-y border-[#2a2a2a] py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="section-title mb-2">Kategorije</h2>
          <p className="section-subtitle mb-10">Pronađi motocikl koji odgovara tvom stilu</p>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {CATEGORIES_INFO.map((cat) => (
              <Link
                key={cat.name}
                href={`/motocikli?category=${cat.name}`}
                className="card p-5 text-center hover:border-orange-500/50 transition-all hover:-translate-y-1 group"
              >
                <div className="text-3xl mb-3">{cat.icon}</div>
                <div className="text-white font-semibold text-sm group-hover:text-orange-400 transition-colors">
                  {cat.name}
                </div>
                <div className="text-gray-600 text-xs mt-1">{cat.desc}</div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="relative rounded-2xl overflow-hidden bg-gradient-to-r from-orange-600 to-orange-500 p-10 md:p-16 text-center">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_rgba(255,255,255,0.1)_0%,_transparent_70%)]" />
          <div className="relative">
            <h2 className="text-3xl md:text-5xl font-black text-white mb-4">
              Zanima te određeni model?
            </h2>
            <p className="text-orange-100 text-lg mb-8 max-w-xl mx-auto">
              Kontaktiraj nas za test vožnju, detaljne informacije ili posebne ponude.
            </p>
            <Link href="/kontakt" className="inline-flex items-center gap-2 bg-white text-orange-600 font-bold px-8 py-4 rounded-lg hover:bg-orange-50 transition-colors text-lg">
              Pošalji upit
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
