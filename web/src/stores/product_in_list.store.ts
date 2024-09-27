import { defineStore } from 'pinia';
import { ref } from 'vue';
import type {
  ProductInList,
  ProductInListCreate,
  // ProductInListWithDetails,
} from 'src/models/product/product_in_list'; // Ajuste o path conforme sua estrutura
import {
  get_products_in_list,
  create_product_in_list,
  update_product_in_list,
  delete_product_in_list,
} from 'src/services/product_in_list.service';
import { useProductStore } from 'src/stores/product.store';

export const useProductInListStore = defineStore('product_in_list', {
  state: () => ({
    productsByList: {} as Record<number, ProductInListCreate[]>, // Armazena os produtos por list_id
    isLoading: ref(false),
  }),
  actions: {
    async fetchProductsInList(list_id: number) {
      if (!this.productsByList[list_id]) {
        this.isLoading = true;

        try {
          const productStore = useProductStore();
          await productStore.fetchProducts();

          const response = await get_products_in_list(list_id);
          this.productsByList[list_id] = response;
        } catch (error) {
          console.error('Erro ao buscar produtos da lista');
        } finally {
          this.isLoading = false;
        }
      }
    },
    async createProductInList(list_id: number, product: ProductInList) {
      try {
        // Faz a requisição para criar um novo produto na lista
        const response = await create_product_in_list(list_id, product);
        if (!this.productsByList[list_id]) {
          this.productsByList[list_id] = [];
        }
        this.productsByList[list_id].push(response);
      } catch (error) {
        console.error(`Erro ao criar produto na lista ${list_id}:`, error);
      }
    },
    async updateProductInList(list_id: number, product: ProductInListCreate) {
      try {
        // Faz a requisição para atualizar o produto da lista
        await update_product_in_list(
          list_id,
          product.product_in_list_id,
          product
        );
        const index = this.productsByList[list_id].findIndex(
          (p) => p.product_in_list_id === product.product_in_list_id
        );
        if (index !== -1) {
          this.productsByList[list_id][index] = product; // Atualiza o produto na store
        }
      } catch (error) {
        console.error(`Erro ao atualizar produto na lista ${list_id}:`, error);
      }
    },
    async deleteProductInList(list_id: number, product_in_list_id: number) {
      try {
        // Faz a requisição para deletar o produto da lista
        await delete_product_in_list(list_id, product_in_list_id);
        this.productsByList[list_id] = this.productsByList[list_id].filter(
          (product) => product.product_in_list_id !== product_in_list_id
        ); // Remove o produto da store
      } catch (error) {
        console.error(`Erro ao deletar produto na lista ${list_id}:`, error);
      }
    },
  },
});
