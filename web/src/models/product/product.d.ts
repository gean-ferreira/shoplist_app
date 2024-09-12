import type { Payload } from '../payload/payload';

export interface Product {
  product_id: number;
  product_name: string;
}

export interface ProductCreationResponse extends Payload<Product> {}

export interface ProductListResponse extends Payload<Product[]> {}
