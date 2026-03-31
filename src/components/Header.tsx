"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname, useSearchParams } from "next/navigation";
import { useState, Suspense } from "react";

const navLinks = [
  { href: "/",                            label: "Početna" },
  { href: "/motocikli",                   label: "Motocikli" },
  { href: "/motocikli?category=Quad",     label: "Quad" },
  { href: "/motocikli?category=Mule",     label: "Mule" },
  { href: "/motocikli?category=Jet+Ski",  label: "Jet Ski" },
  { href: "/kontakt",                     label: "Kontakt" },
];

function HeaderInner() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [open, setOpen] = useState(false);

  function isActive(href: string) {
    if (href === "/") return pathname === "/";
    const [path, query] = href.split("?");
    if (pathname !== path) return false;
    if (!query) return !searchParams.get("category");
    const param = new URLSearchParams(query);
    return searchParams.get("category") === param.get("category");
  }

  return (
    <header className="sticky top-0 z-50 backdrop-blur border-b" style={{background:"rgba(237,243,237,0.95)", borderColor:"var(--line)"}}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">

          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <Image
              src="/logo-jakopec.jpg"
              alt="Moto Jakopec"
              width={140}
              height={48}
              className="h-10 w-auto object-contain"
              priority
            />
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive(link.href)
                    ? "font-semibold"
                    : "hover:bg-black/5"
                }`}
                style={
                  isActive(link.href)
                    ? { color: "var(--green-dk)", background: "rgba(55,182,58,0.1)" }
                    : { color: "var(--text)" }
                }
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* Phone + CTA */}
          <div className="hidden md:flex items-center gap-4">
            <a
              href="tel:0013371059"
              className="text-sm flex items-center gap-1 transition-colors"
              style={{ color: "var(--muted)" }}
              onMouseEnter={e => (e.currentTarget.style.color = "var(--green-dk)")}
              onMouseLeave={e => (e.currentTarget.style.color = "var(--muted)")}
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              01/3371-059
            </a>
            <Link href="/motocikli" className="btn-primary text-sm py-2 px-4">
              Pregledaj ponudu
            </Link>
          </div>

          {/* Mobile hamburger */}
          <button
            className="md:hidden p-2 transition-colors"
            style={{ color: "var(--muted)" }}
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
          <div className="md:hidden border-t py-4 space-y-1" style={{borderColor:"var(--line)"}}>
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className={`block px-4 py-3 rounded-lg text-sm font-medium transition-colors`}
                style={
                  isActive(link.href)
                    ? { color: "var(--green-dk)", background: "rgba(55,182,58,0.1)" }
                    : { color: "var(--text)" }
                }
              >
                {link.label}
              </Link>
            ))}
            <div className="pt-2 px-4 text-sm" style={{ color: "var(--muted)" }}>
              01/3371-059
            </div>
          </div>
        )}
      </div>
    </header>
  );
}

export default function Header() {
  return (
    <Suspense fallback={null}>
      <HeaderInner />
    </Suspense>
  );
}
