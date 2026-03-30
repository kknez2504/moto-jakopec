import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Kontakt",
  description: "Kontaktirajte Moto Jakopec — telefon, email ili posjetite nas u Krapini.",
};

const INFO = [
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
    label: "Adresa",
    value: "Vaša ulica bb, 49000 Krapina",
    href: null,
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
      </svg>
    ),
    label: "Telefon",
    value: "+385 49 123 456",
    href: "tel:+38549123456",
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    ),
    label: "Email",
    value: "info@moto-jakopec.com",
    href: "mailto:info@moto-jakopec.com",
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    label: "Radno vrijeme",
    value: "Pon–Pet: 8–17h  |  Sub: 8–13h",
    href: null,
  },
];

export default function KontaktPage() {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="mb-12">
        <h1 className="section-title">Kontakt</h1>
        <p className="section-subtitle">
          Javite nam se — odgovaramo što brže možemo.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">

        {/* Contact info */}
        <div className="space-y-5">
          {INFO.map((item) => (
            <div key={item.label} className="card p-5 flex items-start gap-4">
              <div className="text-orange-500 shrink-0 mt-0.5">{item.icon}</div>
              <div>
                <div className="text-gray-500 text-xs font-medium uppercase tracking-wide mb-1">
                  {item.label}
                </div>
                {item.href ? (
                  <a
                    href={item.href}
                    className="text-white font-medium hover:text-orange-500 transition-colors"
                  >
                    {item.value}
                  </a>
                ) : (
                  <span className="text-white font-medium">{item.value}</span>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Contact form */}
        <div className="card p-6">
          <h2 className="text-white font-bold text-xl mb-6">Pošalji upit</h2>
          <form
            action="mailto:info@moto-jakopec.com"
            method="get"
            className="space-y-4"
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-400 text-sm mb-1.5">Ime i prezime</label>
                <input
                  name="name"
                  type="text"
                  required
                  placeholder="Ivan Horvat"
                  className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-orange-500 transition-colors text-sm"
                />
              </div>
              <div>
                <label className="block text-gray-400 text-sm mb-1.5">Telefon</label>
                <input
                  name="phone"
                  type="tel"
                  placeholder="+385 9x xxx xxxx"
                  className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-orange-500 transition-colors text-sm"
                />
              </div>
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1.5">Email</label>
              <input
                name="email"
                type="email"
                required
                placeholder="ivan@email.com"
                className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-orange-500 transition-colors text-sm"
              />
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1.5">Model koji vas zanima</label>
              <input
                name="model"
                type="text"
                placeholder="npr. Kawasaki Z900"
                className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-orange-500 transition-colors text-sm"
              />
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1.5">Poruka</label>
              <textarea
                name="body"
                required
                rows={4}
                placeholder="Vaša poruka..."
                className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-orange-500 transition-colors text-sm resize-none"
              />
            </div>

            <button type="submit" className="btn-primary w-full justify-center">
              Pošalji upit
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
