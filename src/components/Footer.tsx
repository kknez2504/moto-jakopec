"use client";

import Link from "next/link";
import Image from "next/image";

export default function Footer() {
  return (
    <footer className="mt-20 border-t" style={{background:"var(--bg2)", borderColor:"var(--line)"}}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

          {/* Brand */}
          <div>
            <div className="mb-4">
              <Image
                src="/logo-jakopec.jpg"
                alt="Moto Jakopec"
                width={140}
                height={48}
                className="h-10 w-auto object-contain"
              />
            </div>
            <p className="text-sm leading-relaxed" style={{ color: "var(--muted)" }}>
              Ovlašteni Kawasaki zastupnik za Hrvatsku. Prodaja novih motocikala,
              servis, rezervni dijelovi i oprema.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold mb-4" style={{ color: "var(--text)" }}>Navigacija</h3>
            <ul className="space-y-2 text-sm">
              {[
                { href: "/",          label: "Početna" },
                { href: "/motocikli", label: "Motocikli" },
                { href: "/kontakt",   label: "Kontakt" },
              ].map((l) => (
                <li key={l.href}>
                  <Link
                    href={l.href}
                    className="transition-colors"
                    style={{ color: "var(--muted)" }}
                    onMouseEnter={e => (e.currentTarget.style.color = "var(--green-dk)")}
                    onMouseLeave={e => (e.currentTarget.style.color = "var(--muted)")}
                  >
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-semibold mb-4" style={{ color: "var(--text)" }}>Kontakt</h3>
            <ul className="space-y-2 text-sm" style={{ color: "var(--muted)" }}>
              <li className="flex items-start gap-2">
                <svg className="w-4 h-4 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: "var(--green)" }}>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Eugena Kvaternika 4, 10430 Samobor
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: "var(--green)" }}>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <a href="tel:0013371059" className="transition-colors hover:text-green-700">
                  01/3371-059
                </a>
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: "var(--green)" }}>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <a href="mailto:moto.jakopec@gmail.com" className="transition-colors hover:text-green-700">
                  moto.jakopec@gmail.com
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-10 pt-6 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs border-t" style={{ color: "var(--muted)", borderColor: "var(--line)" }}>
          <p>© {new Date().getFullYear()} Moto Jakopec. Sva prava pridržana.</p>
          <p>Ovlašteni Kawasaki zastupnik</p>
        </div>
      </div>
    </footer>
  );
}
