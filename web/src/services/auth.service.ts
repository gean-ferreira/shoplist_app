import { api } from 'src/boot/axios';
import { Notify } from 'quasar';

interface LoginPayload {
  username: string;
  password: string;
}

export const login = async (payload: LoginPayload) => {
  try {
    const response = await api.post<{ message: string }>(
      '/auth/login/',
      payload,
    );
    Notify.create({
      type: 'positive',
      message: response.data.message,
      timeout: 2000,
      position: 'top-right',
    });
  } catch (error) {
    throw error;
  }
};
