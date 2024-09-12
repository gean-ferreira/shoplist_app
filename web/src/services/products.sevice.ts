import { api } from 'src/boot/axios';
import { Notify } from 'quasar';
import {
  ProductCreationResponse,
  ProductListResponse,
} from 'src/models/product/product';

export const get_products = async () => {
  try {
    const response = await api.get<ProductListResponse>('/products/');
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

export const create_product = async (product_name: string) => {
  try {
    const response = await api.post<ProductCreationResponse>('/products/', {
      product_name: product_name,
    });
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

export const update_product = async (
  product_id: number,
  product_name: string
) => {
  try {
    const response = await api.put<{ message: string }>(
      `/products/${product_id}`,
      {
        product_name: product_name,
      }
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

export const delete_product = async (product_id: number) => {
  try {
    const response = await api.delete<{ message: string }>(
      `/products/${product_id}`
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
