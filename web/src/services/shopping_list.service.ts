import { api } from 'src/boot/axios';
import { Notify } from 'quasar';
import type {
  ShoppingListCreationResponse,
  ShoppingListResponse,
} from 'src/models/shopping_list/shopping_list';

export const get_shopping_lists = async () => {
  try {
    const response = await api.get<ShoppingListResponse>('/shopping-lists/', {
      withCredentials: true,
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

export const create_shopping_list = async (list_name: string) => {
  try {
    const response = await api.post<ShoppingListCreationResponse>(
      '/shopping-lists/',
      {
        list_name: list_name,
      },
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

export const update_shopping_list = async (
  list_id: number,
  list_name: string
) => {
  try {
    const response = await api.put<{ message: string }>(
      `/shopping-lists/${list_id}`,
      {
        list_name: list_name,
      },
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

export const delete_shopping_list = async (list_id: number) => {
  try {
    const response = await api.delete<{ message: string }>(
      `/shopping-lists/${list_id}`,
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
