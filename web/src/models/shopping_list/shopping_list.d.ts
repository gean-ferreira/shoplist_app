import { Payload } from '../payload/payload';

export interface ShoppingList {
  list_id: number;
  list_name: string;
  created_at: Date;
}

export interface ShoppingListCreationResponse extends Payload<ShoppingList> {}

export interface ShoppingListResponse extends Payload<ShoppingList[]> {}
