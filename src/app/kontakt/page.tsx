import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Kontakt",
  description: "Kontaktirajte Moto Jakopec — telefon, email ili posjetite nas u Samoboru.",
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
    value: "Eugena Kvaternika 4, 10430 Samobor (Mala Rakovica)",
    href: null,
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
      </svg>
    ),
    label: "Tel/Fax",
    value: "01/3371-059",
    href: "tel:0013371059",
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    ),
    label: "Email",
    value: "moto.jakopec@gmail.com",
    href: "mailto:moto.jakopec@gmail.com",
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    label: "Radno vrijeme",
    value: "Ponedjeljak i srijeda: 10:00 – 18:00\nUtorak, četvrtak i petak: 8:00 – 16:00",
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
              <div className="shrink-0 mt-0.5" style={{ color: "var(--green)" }}>{item.icon}</div>
              <div>
                <div className="text-xs font-medium uppercase tracking-wide mb-1" style={{ color: "var(--muted)" }}>
                  {item.label}
                </div>
                {item.href ? (
                  <a
                    href={item.href}
                    className="font-medium transition-colors hover:underline"
                    style={{ color: "var(--text)" }}
                  >
                    {item.value}
                  </a>
                ) : (
                  <span className="font-medium" style={{ color: "var(--text)", whiteSpace: "pre-line" }}>{item.value}</span>
                )}
              </div>
            </div>
          ))}

          {/* Map embed */}
          <div className="card overflow-hidden">
            <iframe
              title="Moto Jakopec lokacija"
              src="https://www.google.com/maps?q=Ul.+Eugena+Kvaternika+4,+10430,+Mala+Rakovica&output=embed"
              width="100%"
              height="260"
              style={{ border: 0 }}
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
            />
          </div>
        </div>

        {/* Contact form */}
        <div className="card p-6">
          <h2 className="font-bold text-xl mb-6" style={{ color: "var(--text)" }}>Pošalji upit</h2>
          <form
            action="mailto:moto.jakopec@gmail.com"
            method="get"
            className="space-y-4"
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm mb-1.5" style={{ color: "var(--muted)" }}>Ime i prezime</label>
                <input
                  name="name"
                  type="text"
                  required
                  placeholder="Ivan Horvat"
                  className="w-full rounded-lg px-4 py-3 text-sm focus:outline-none transition-colors"
                  style={{
                    background: "var(--bg2)",
                    border: "1px solid var(--line)",
                    color: "var(--text)",
                  }}
                />
              </div>
              <div>
                <label className="block text-sm mb-1.5" style={{ color: "var(--muted)" }}>Telefon</label>
                <input
                  name="phone"
                  type="tel"
                  placeholder="+385 9x xxx xxxx"
                  className="w-full rounded-lg px-4 py-3 text-sm focus:outline-none transition-colors"
                  style={{
                    background: "var(--bg2)",
                    border: "1px solid var(--line)",
                    color: "var(--text)",
                  }}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm mb-1.5" style={{ color: "var(--muted)" }}>Email</label>
              <input
                name="email"
                type="email"
                required
                placeholder="ivan@email.com"
                className="w-full rounded-lg px-4 py-3 text-sm focus:outline-none transition-colors"
                style={{
                  background: "var(--bg2)",
                  border: "1px solid var(--line)",
                  color: "var(--text)",
                }}
              />
            </div>

            <div>
              <label className="block text-sm mb-1.5" style={{ color: "var(--muted)" }}>Model koji vas zanima</label>
              <input
                name="model"
                type="text"
                placeholder="npr. Kawasaki Z900"
                className="w-full rounded-lg px-4 py-3 text-sm focus:outline-none transition-colors"
                style={{
                  background: "var(--bg2)",
                  border: "1px solid var(--line)",
                  color: "var(--text)",
                }}
              />
            </div>

            <div>
              <label className="block text-sm mb-1.5" style={{ color: "var(--muted)" }}>Poruka</label>
              <textarea
                name="body"
                required
                rows={4}
                placeholder="Vaša poruka..."
                className="w-full rounded-lg px-4 py-3 text-sm focus:outline-none transition-colors resize-none"
                style={{
                  background: "var(--bg2)",
                  border: "1px solid var(--line)",
                  color: "var(--text)",
                }}
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
