import { boot } from 'quasar/wrappers';
import axios, { AxiosError, AxiosInstance } from 'axios';
import { Notify } from 'quasar';

declare module 'vue' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}

// Define a estrutura esperada da resposta de erro
interface ErrorResponse {
  detail: string;
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: process.env.VITE_API_URL });

// Interceptor para respostas
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
const api = axios.create({ baseURL: 'https://api.example.com' });
    if (error.response) {
      const errorData = error.response.data as ErrorResponse;
      const message = errorData.detail || 'Ocorreu um erro';

      Notify.create({
        type: 'negative',
        message: message,
        timeout: 3000,
        position: 'top-right',
      });
    } else {
      // Erro genérico quando não há resposta
      Notify.create({
        type: 'negative',
        message: 'Ocorreu um erro inesperado aconteceu',
        timeout: 3000,
        position: 'top-right',
      });
    }
    return Promise.reject(error.response);
  }
);

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api };
