import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/IndexPage.vue'),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: 'produtos',
        component: () => import('pages/ProductPage.vue'),
      {
        path: 'listas-de-compras',
        name: 'Listas de compras',
        component: () => import('src/pages/ShoppingListPage.vue'),
        meta: {
          requiresAuth: true,
        },
      },
      {
        name: 'Produtos da lista',
        path: 'listas-de-compras/:list_id/produtos',
        component: () => import('src/pages/ShoppingListProductsPage.vue'),
        meta: {
          requiresAuth: true,
        },
      },
    ],
  },
  {
    path: '/login',
    component: () => import('layouts/BlankLayout.vue'),
    children: [{ path: '', component: () => import('pages/LoginPage.vue') }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
