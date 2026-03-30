import { notFound } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";
import type { Motorcycle } from "@/types/motorcycle";
import modelsData from "@/data/models.json";

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
  const hasImages = bike.images && bike.images.length > 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-gray-500 mb-8">
        <Link href="/" className="hover:text-orange-500 transition-colors">Početna</Link>
        <span>/</span>
        <Link href="/motocikli" className="hover:text-orange-500 transition-colors">Motocikli</Link>
        <span>/</span>
        <span className="text-white">{bike.name}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">

        {/* Left — image */}
        <div>
          <div className="relative aspect-video bg-[#161616] rounded-xl overflow-hidden border border-[#2a2a2a] mb-4">
            {hasImages ? (
              <Image
                src={bike.images[0]}
                alt={bike.name}
                fill
                className="object-cover"
                sizes="(max-width: 1024px) 100vw, 50vw"
                priority
              />
            ) : (
              <div className="w-full h-full flex flex-col items-center justify-center gap-3">
                <svg className="w-20 h-20 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p className="text-gray-600 text-sm">Slika uskoro</p>
              </div>
            )}
          </div>

          {/* Thumbnail strip */}
          {bike.images.length > 1 && (
            <div className="flex gap-2 overflow-x-auto pb-2">
              {bike.images.map((img, i) => (
                <div key={i} className="relative w-20 h-14 shrink-0 rounded-lg overflow-hidden border border-[#2a2a2a]">
                  <Image src={img} alt={`${bike.name} ${i + 1}`} fill className="object-cover" />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right — details */}
        <div>
          {/* Badges */}
          <div className="flex flex-wrap gap-2 mb-4">
            {bike.is_new && (
              <span className="bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                NOVO {new Date().getFullYear()}
              </span>
            )}
            <span className="bg-[#161616] border border-[#2a2a2a] text-gray-300 text-xs font-medium px-3 py-1 rounded-full">
              {bike.category}
            </span>
            {bike.license_category && (
              <span className="bg-[#161616] border border-[#2a2a2a] text-gray-300 text-xs font-medium px-3 py-1 rounded-full">
                Kategorija {bike.license_category}
              </span>
            )}
          </div>

          <h1 className="text-3xl md:text-4xl font-black text-white mb-3">{bike.name}</h1>
          <p className="text-gray-400 leading-relaxed mb-6">{bike.description}</p>

          {/* Price */}
          <div className="card p-5 mb-6">
            <div className="text-gray-500 text-sm mb-1">Maloprodajna cijena</div>
            <div className="text-4xl font-black text-orange-500 mb-1">{bike.price}</div>
            {bike.price_2025 && bike.price_2025 !== bike.price && (
              <div className="text-xs text-gray-600">2025: {bike.price_2025}</div>
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
            <a href="tel:+38549123456" className="btn-outline flex-1 justify-center">
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
              <h2 className="text-white font-bold text-lg mb-3">Tehničke specifikacije</h2>
              <div className="card overflow-hidden">
                <table className="w-full text-sm">
                  <tbody>
                    {Object.entries(bike.specs).map(([key, value], i) => (
                      <tr key={key} className={i % 2 === 0 ? "bg-[#161616]" : "bg-[#1a1a1a]"}>
                        <td className="px-4 py-2.5 text-gray-500 font-medium w-1/2">{key}</td>
                        <td className="px-4 py-2.5 text-white">{value}</td>
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
      <div className="mt-12 pt-8 border-t border-[#2a2a2a]">
        <Link
          href="/motocikli"
          className="text-gray-400 hover:text-orange-500 transition-colors flex items-center gap-2 text-sm"
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
