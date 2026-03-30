"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const navLinks = [
  { href: "/",           label: "Početna" },
  { href: "/motocikli",  label: "Motocikli" },
  { href: "/kontakt",    label: "Kontakt" },
];

export default function Header() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-[#0f0f0f]/95 backdrop-blur border-b border-[#2a2a2a]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">

          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <span className="text-orange-500 text-2xl font-black tracking-tight group-hover:text-orange-400 transition-colors">
              MOTO
            </span>
            <span className="text-white text-2xl font-light tracking-tight">
              JAKOPEC
            </span>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  pathname === link.href
                    ? "text-orange-500 bg-orange-500/10"
                    : "text-gray-300 hover:text-white hover:bg-white/5"
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* Phone + CTA */}
          <div className="hidden md:flex items-center gap-4">
            <a
              href="tel:+38549123456"
              className="text-sm text-gray-400 hover:text-orange-500 transition-colors flex items-center gap-1"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              +385 49 123 456
            </a>
            <Link href="/motocikli" className="btn-primary text-sm py-2 px-4">
              Pregledaj ponudu
            </Link>
          </div>

          {/* Mobile hamburger */}
          <button
            className="md:hidden p-2 text-gray-400 hover:text-white"
            onClick={() => setOpen(!open)}
            aria-label="Toggle menu"
          >
            {open ? (
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>

        {/* Mobile menu */}
        {open && (
          <div className="md:hidden border-t border-[#2a2a2a] py-4 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className={`block px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                  pathname === link.href
                    ? "text-orange-500 bg-orange-500/10"
                    : "text-gray-300 hover:text-white hover:bg-white/5"
                }`}
              >
                {link.label}
              </Link>
            ))}
            <div className="pt-2 px-4">
              <a href="tel:+38549123456" className="text-sm text-gray-400">
                +385 49 123 456
              </a>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
