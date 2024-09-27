import { api } from 'src/boot/axios';
import { Notify } from 'quasar';
import type {
  ProductInList,
  ProductInListCreationResponse,
  ProductInListResponse,
} from 'src/models/product/product_in_list';

export const get_products_in_list = async (list_id: number) => {
  try {
    const response = await api.get<ProductInListResponse>(
      `/shopping-lists/${list_id}/products/`,
      { withCredentials: true }
    );
    Notify.create({
      type: 'positive',
      message: response.data.message,
      timeout: 3000,
      position: 'top-right',
    });
    return response.data.data;
  } catch (error) {
    throw error;
  }
};

export const create_product_in_list = async (
  list_id: number,
  product: ProductInList
) => {
  try {
    const response = await api.post<ProductInListCreationResponse>(
      `/shopping-lists/${list_id}/products/`,
      product,
      { withCredentials: true }
    );
    Notify.create({
      type: 'positive',
      message: response.data.message,
      timeout: 3000,
      position: 'top-right',
    });
    return response.data.data;
  } catch (error) {
    throw error;
  }
};

export const update_product_in_list = async (
  list_id: number,
  product_in_list_id: number,
  product: ProductInList
) => {
  try {
    const response = await api.put<{ message: string }>(
      `/shopping-lists/${list_id}/products/${product_in_list_id}/`,
      product,
      { withCredentials: true }
    );
    Notify.create({
      type: 'positive',
      message: response.data.message,
      timeout: 3000,
      position: 'top-right',
    });
  } catch (error) {
    throw error;
  }
};

export const delete_product_in_list = async (
  list_id: number,
  product_in_list_id: number
) => {
  try {
    const response = await api.delete<{ message: string }>(
      `/shopping-lists/${list_id}/products/${product_in_list_id}/`,
      { withCredentials: true }
    );
    Notify.create({
      type: 'positive',
      message: response.data.message,
      timeout: 3000,
      position: 'top-right',
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
