import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: {
    default: "Moto Jakopec — Kawasaki specijalist",
    template: "%s | Moto Jakopec",
  },
  description:
    "Ovlašteni Kawasaki zastupnik. Prodaja motocikala, rezervnih dijelova i opreme. Posjetite nas u Samoboru.",
  keywords: ["kawasaki", "motocikli", "moto jakopec", "samobor", "prodaja motocikala"],
  openGraph: {
    type: "website",
    locale: "hr_HR",
    siteName: "Moto Jakopec",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="hr" className={inter.variable}>
      <body className="min-h-screen flex flex-col" style={{background:"var(--bg)"}}>
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
