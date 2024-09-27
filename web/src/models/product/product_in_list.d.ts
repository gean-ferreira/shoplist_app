import type { Payload } from '../payload/payload';

export interface ProductInList {
  quantity: number;
  price: number;
  product_id: number;
}

export interface ProductInListCreate extends ProductInList {
  product_in_list_id: number;
}

export interface ProductInListCreationResponse
  extends Payload<ProductInListCreate> {}

export interface ProductInListResponse extends Payload<ProductInListCreate[]> {}
