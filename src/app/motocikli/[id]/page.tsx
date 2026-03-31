import { notFound } from "next/navigation";
import Link from "next/link";
import type { Metadata } from "next";
import type { Motorcycle } from "@/types/motorcycle";
import modelsData from "@/data/models.json";
import BikeGallery from "@/components/BikeGallery";

const models = modelsData as unknown as Motorcycle[];

interface Props {
  params: Promise<{ id: string }>;
}

export async function generateStaticParams() {
  return models.map((m) => ({ id: String(m.id) }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { id } = await params;
  const bike = models.find((m) => m.id === Number(id));
  if (!bike) return { title: "Model nije pronađen" };
  return {
    title: bike.name,
    description: bike.description,
  };
}

export default async function BikeDetailPage({ params }: Props) {
  const { id } = await params;
  const bike = models.find((m) => m.id === Number(id));

  if (!bike) notFound();

  const hasSpecs = bike.specs && Object.keys(bike.specs).length > 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm mb-8" style={{ color: "var(--muted)" }}>
        <Link href="/" className="transition-colors hover:underline" style={{ color: "var(--muted)" }}>Početna</Link>
        <span>/</span>
        <Link href="/motocikli" className="transition-colors hover:underline" style={{ color: "var(--muted)" }}>Vozila</Link>
        <span>/</span>
        <span style={{ color: "var(--text)" }}>{bike.name}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">

        {/* Left — gallery */}
        <div>
          <BikeGallery images={bike.images} name={bike.name} />
        </div>

        {/* Right — details */}
        <div>
          {/* Badges */}
          <div className="flex flex-wrap gap-2 mb-4">
            {bike.is_new && (
              <span className="text-white text-xs font-bold px-3 py-1 rounded-full" style={{ background: "var(--green)" }}>
                NOVO {new Date().getFullYear()}
              </span>
            )}
            <span className="text-xs font-medium px-3 py-1 rounded-full border" style={{ background: "rgba(55,182,58,.08)", color: "var(--green-dk)", borderColor: "rgba(55,182,58,.25)" }}>
              {bike.category}
            </span>
            {bike.license_category && (
              <span className="text-xs font-medium px-3 py-1 rounded-full border" style={{ background: "var(--bg2)", color: "var(--muted)", borderColor: "var(--line)" }}>
                Kategorija {bike.license_category}
              </span>
            )}
          </div>

          <h1 className="text-3xl md:text-4xl font-black mb-3" style={{ color: "var(--text)" }}>{bike.name}</h1>
          <p className="leading-relaxed mb-6" style={{ color: "var(--muted)" }}>{bike.description}</p>

          {/* Price */}
          <div className="card p-5 mb-6">
            <div className="text-sm mb-1" style={{ color: "var(--muted)" }}>Maloprodajna cijena</div>
            <div className="text-4xl font-black mb-1" style={{ color: "var(--green-dk)" }}>{bike.price}</div>
            {bike.price_2025 && bike.price_2025 !== bike.price && (
              <div className="text-xs" style={{ color: "var(--muted)" }}>2025: {bike.price_2025}</div>
            )}
          </div>

          {/* CTA buttons */}
          <div className="flex flex-col sm:flex-row gap-3 mb-8">
            <Link href="/kontakt" className="btn-primary flex-1 justify-center">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Pošalji upit
            </Link>
            <a href="tel:0013371059" className="btn-outline flex-1 justify-center">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              Nazovi nas
            </a>
          </div>

          {/* Specs */}
          {hasSpecs && (
            <div>
              <h2 className="font-bold text-lg mb-3" style={{ color: "var(--text)" }}>Tehničke specifikacije</h2>
              <div className="card overflow-hidden">
                <table className="w-full text-sm">
                  <tbody>
                    {Object.entries(bike.specs).map(([key, value], i) => (
                      <tr key={key} style={{ background: i % 2 === 0 ? "var(--bg)" : "var(--surface)" }}>
                        <td className="px-4 py-2.5 font-medium w-1/2" style={{ color: "var(--muted)" }}>{key}</td>
                        <td className="px-4 py-2.5" style={{ color: "var(--text)" }}>{value}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Back link */}
      <div className="mt-12 pt-8 border-t" style={{ borderColor: "var(--line)" }}>
        <Link
          href="/motocikli"
          className="flex items-center gap-2 text-sm transition-colors"
          style={{ color: "var(--muted)" }}
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Natrag na sve modele
        </Link>
      </div>
    </div>
  );
}
