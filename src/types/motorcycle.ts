export interface Motorcycle {
  id: number;
  name: string;
  brand: string;
  category: string;
  purpose: string;
  license_category?: string;
  is_new?: boolean;
  description: string;
  price: string;
  price_2024?: string;
  price_2025?: string;
  price_2026?: string;
  images: string[];
  specs: Record<string, string>;
}

export type Category =
  | "Sve"
  | "Sport"
  | "Naked"
  | "Adventure"
  | "Touring"
  | "Classic"
  | "Cruiser"
  | "Offroad";

export const CATEGORIES: Category[] = [
  "Sve",
  "Sport",
  "Naked",
  "Adventure",
  "Touring",
  "Classic",
  "Cruiser",
  "Offroad",
];
