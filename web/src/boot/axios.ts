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
      if (error.response && error.response.status === 401) {
        router.push('/login');
        Notify.create({
          type: 'negative',
          message: 'Sua sessão expirou, faça login novamente',
          timeout: 3000,
          position: 'top-right',
        });
      } else if (error.response && error.response.status === 500) {
        Notify.create({
          type: 'negative',
          message:
            'Erro interno do servidor. Por favor, tente novamente mais tarde',
          timeout: 3000,
          position: 'top-right',
        });
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
