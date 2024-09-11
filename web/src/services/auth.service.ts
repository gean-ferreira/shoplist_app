import { api } from 'src/boot/axios';
import { Notify } from 'quasar';
import type { LoginPayload } from 'src/models/auth/login';
import { useUserStore } from 'src/stores/user.store';

export const read_user_data = async () => {
  const userStore = useUserStore();

  try {
    const response = await api.get<{
      message: string;
      data: { username: string };
    }>('/users/', { withCredentials: true });
    userStore.setUsername(response.data.data.username);
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
