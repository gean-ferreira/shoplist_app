import { api } from 'src/boot/axios';
import { Notify } from 'quasar';
import type { LoginPayload } from 'src/models/auth/login';

export const login = async (payload: LoginPayload) => {
  try {
    const response = await api.post<{ message: string }>(
      '/auth/login/',
      payload,
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
