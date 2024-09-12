import { defineStore } from 'pinia';
import { Product } from 'src/models/product/product';
import {
  create_product,
  delete_product,
  get_products,
  update_product,
} from 'src/services/products.sevice';
import { ref } from 'vue';

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [] as Product[],
    isLoading: ref(false),
  }),
  actions: {
    async fetchProducts() {
      if (!this.products.length) {
        this.isLoading = true;
        await get_products()
          .then((res) => (this.products = res.data))
          .catch(() => {
            throw console.error('Error na renderização dos produtos');
          })
          .finally(() => (this.isLoading = false));
      }
    },
    async createProduct(product_name: string) {
      await create_product(product_name)
        .then((res) => {
          this.products.push(res.data); // Adiciona o novo produto localmente
        })
        .catch(() => {
          throw console.error('Error ao criar produto');
        });
    },
    async updateProduct(product_id: number, product_name: string) {
      await update_product(product_id, product_name)
        .then(() => {
          const product = this.products.find(
            (p) => p.product_id === product_id
          );
          if (product) {
            product.product_name = product_name; // Atualiza o nome do produto localmente
          }
        })
        .catch(() => {
          throw console.error('Error ao atualizar produto');
        });
    },
    async deleteProduct(product_id: number) {
      await delete_product(product_id)
        .then(() => {
          this.products = this.products.filter(
            (p) => p.product_id !== product_id // Deleta o produto localmente
          );
        })
        .catch(() => {
          throw console.error('Erro ao excluir produto');
        });
    }
  },
});
