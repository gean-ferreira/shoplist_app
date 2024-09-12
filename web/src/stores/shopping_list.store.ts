import { defineStore } from 'pinia';
import { ShoppingList } from 'src/models/shopping_list/shopping_list';
import {
  get_shopping_lists,
  create_shopping_list,
  update_shopping_list,
  delete_shopping_list,
} from 'src/services/shopping_list.service';
import { ref } from 'vue';

export const useShoppingListStore = defineStore('shopping', {
  state: () => ({
    shopping_list: [] as ShoppingList[],
    isLoading: ref(false),
    hasFetched: false,
  }),
  actions: {
    async fetchShoppingList() {
      if (!this.hasFetched) {
        this.isLoading = true;
        await get_shopping_lists()
          .then((res) => {
            this.shopping_list = res.data;
            this.hasFetched = true;
          })
          .catch(() => {
            throw console.error('Error na renderização das listas de comprass');
          })
          .finally(() => (this.isLoading = false));
      }
    },
    async createShoppingList(list_name: string) {
      await create_shopping_list(list_name)
        .then((res) => {
          this.shopping_list.push(res.data); // Adiciona uma nova lista de compras localmente
        })
        .catch(() => {
          throw console.error('Error ao criar uma lista de compras');
        });
    },
    async updateShoppingList(list_id: number, list_name: string) {
      await update_shopping_list(list_id, list_name)
        .then(() => {
          const shoppingList = this.shopping_list.find(
            (p) => p.list_id === list_id
          );
          if (shoppingList) {
            shoppingList.list_name = list_name; // Atualiza o nome da lista de compras localmente
          }
        })
        .catch(() => {
          throw console.error('Error ao atualizar lista de compras');
        });
    },
    async deleteShoppingList(list_id: number) {
      await delete_shopping_list(list_id)
        .then(() => {
          this.shopping_list = this.shopping_list.filter(
            (p) => p.list_id !== list_id // Deleta a lista de compras localmente
          );
        })
        .catch(() => {
          throw console.error('Erro ao excluir lista de compras');
        });
    },
  },
});
