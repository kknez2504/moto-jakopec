import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-[#0a0a0a] border-t border-[#2a2a2a] mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <span className="text-orange-500 text-xl font-black">MOTO</span>
              <span className="text-white text-xl font-light">JAKOPEC</span>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Ovlašteni Kawasaki zastupnik za Hrvatsku. Prodaja novih motocikala,
              servis, rezervni dijelovi i oprema.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Navigacija</h3>
            <ul className="space-y-2 text-sm">
              {[
                { href: "/",          label: "Početna" },
                { href: "/motocikli", label: "Motocikli" },
                { href: "/kontakt",   label: "Kontakt" },
              ].map((l) => (
                <li key={l.href}>
                  <Link href={l.href} className="text-gray-400 hover:text-orange-500 transition-colors">
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white font-semibold mb-4">Kontakt</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li className="flex items-start gap-2">
                <svg className="w-4 h-4 mt-0.5 text-orange-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Vaša adresa, Krapina, Hrvatska
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4 text-orange-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <a href="tel:+38549123456" className="hover:text-orange-500 transition-colors">
                  +385 49 123 456
                </a>
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4 text-orange-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <a href="mailto:info@moto-jakopec.com" className="hover:text-orange-500 transition-colors">
                  info@moto-jakopec.com
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-[#2a2a2a] mt-10 pt-6 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-gray-600">
          <p>© {new Date().getFullYear()} Moto Jakopec. Sva prava pridržana.</p>
          <p>Ovlašteni Kawasaki zastupnik</p>
        </div>
      </div>
    </footer>
  );
}
