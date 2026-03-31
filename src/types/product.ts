export type ProductCategory = "Oprema" | "Dijelovi";

export interface Product {
  id: number;
  name: string;
  category: ProductCategory;
  subcategory: string;      // npr. "Kacige", "Jakne", "Gume", "Filteri"...
  price: string;            // npr. "49,90 €" ili "Cijena na upit"
  description: string;
  image_folder: string;
  images: string[];
  is_new?: boolean;
}
