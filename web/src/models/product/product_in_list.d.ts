import type { Payload } from '../payload/payload';
import { Product } from 'src/models/product/product';

type QuantityType = 'unit' | 'kg';

export interface ProductInList {
  quantity_type: QuantityType;
  quantity: number;
  price: number;
  product_id: number;
}

export interface ProductInListCreate extends ProductInList {
  product_in_list_id: number;
}

export interface FormProductInList
  extends Partial<
    Omit<
      ProductInListCreate,
      'product_id' | 'quantity_type' | 'quantity' | 'price'
    >
  > {
  product_id: Product | undefined;
  quantity_type: QuantityType;
  quantity: string | undefined;
  price: string | undefined;
}

export interface ProductInListCreationResponse
  extends Payload<ProductInListCreate> {}

export interface ProductInListResponse extends Payload<ProductInListCreate[]> {}
