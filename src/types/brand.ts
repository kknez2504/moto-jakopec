export interface Brand {
  brand_id: string;
  name: string;
  logo: string;      // /images/brendovi/{logo_folder}.png
  website: string;
  active: boolean;
}

export interface BrandsData {
  oprema: Brand[];
  dijelovi: Brand[];
}
