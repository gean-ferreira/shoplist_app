import { boot } from 'quasar/wrappers';
import axios, { AxiosError, AxiosInstance } from 'axios';
import { Notify } from 'quasar';

declare module 'vue' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: process.env.VITE_API_URL });

export default boot(({ app, router }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  // Interceptor para respostas
  api.interceptors.response.use(
    (response) => {
      return response;
    },
    (error: AxiosError) => {
      if (!error.response) return Promise.reject(error);

      const { status, data } = error.response;
      type ErrorDetail = { detail: string };
      const { detail } = data as ErrorDetail;

      const notifyError = (message: string) => {
        Notify.create({
          type: 'negative',
          message: message,
          timeout: 3000,
          position: 'top-right',
        });
      };

      switch (status) {
        case 401:
          router.push('/login');
          notifyError(detail);
          break;
        case 400:
        case 404:
        case 422:
          notifyError(detail);
          break;
        case 500:
          notifyError(
            'Erro interno do servidor. Por favor, tente novamente mais tarde'
          );
          break;
        default:
          notifyError('Ocorreu um erro inesperado.');
      }

      return Promise.reject(error.response);
    }
  );

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api };
