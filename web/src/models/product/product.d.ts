import type { Payload } from '../payload/payload';

export interface Product {
  product_id: number;
  product_name: string;
}

export interface ProductsPayload extends Payload<Product[]> {}

export interface ProductPayload extends Payload<Product> {}
