import { RouteRecordRaw } from 'vue-router';

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '/',
        name: 'Home',
        component: () => import('pages/IndexPage.vue'),
        meta: {
          icon: 'home',
          requiresAuth: true,
        },
      },
      {
        path: '/produtos',
        name: 'Produtos',
        component: () => import('pages/ProductPage.vue'),
        meta: {
          icon: 'inventory',
        },
      },
      {
        path: '/listas-de-compras',
        name: 'Listas de compras',
        component: () => import('src/pages/ShoppingListPage.vue'),
        meta: {
          icon: 'shopping_cart',
          requiresAuth: true,
        },
      },
      {
        path: '/listas-de-compras/:list_id/produtos',
        name: 'Produtos da lista',
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
