<template>
  <q-page class="q-px-sm">
    <h1 class="text-h4 text-center">Listas de compras</h1>

    <!-- Skeleton enquanto carrega -->
    <q-list separator v-if="shoppingListStore.isLoading">
      <q-item v-for="i in 5" :key="i">
        <q-item-section>
          <q-skeleton type="text" />
        </q-item-section>
        <q-item-section side>
          <q-skeleton flat type="circle" height="25px" width="25px" />
          <q-skeleton flat type="circle" height="25px" width="25px" />
        </q-item-section>
      </q-item>
    </q-list>

    <q-list v-else separator>
      <!-- Verifica se a lista está vazia -->
      <q-item v-if="shoppingListStore.shopping_list.length === 0">
        <q-item-section class="text-center q-pa-md">
          <q-icon name="inbox" size="lg" class="q-mx-auto" />
          <q-item-label> Nenhuma lista de compras disponível </q-item-label>
          <q-item-label caption
            >Adicione uma nova lista de compras abaixo</q-item-label
          >
        </q-item-section>
      </q-item>

      <!-- Renderiza as listas de compras se houver itens -->
      <q-item
        v-for="list in shoppingListStore.shopping_list"
        :key="list.list_id"
      >
        <q-item-section>
          <q-item-label>{{ list.list_name }}</q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-btn
            flat
            round
            icon="edit"
            @click="openEditDialog(list)"
            color="primary"
          />
          <q-btn
            flat
            round
            icon="delete"
            @click="deleteShoppingList(list.list_id)"
            color="negative"
          />
        </q-item-section>
      </q-item>

      <!-- Botão para adicionar novo lista de compra -->
      <q-btn
        round
        icon="add"
        color="primary"
        class="block q-mt-md q-mx-auto"
        @click="openAddShoppingListDialog"
      />
    </q-list>

    <!-- Diálogo para editar ou adicionar lista -->
    <q-dialog
      position="bottom"
      backdrop-filter="blur(4px) saturate(150%)"
      v-model="editDialog"
    >
      <q-card>
        <q-card-section>
          <div class="text-h6">
            {{
              isEditMode
                ? 'Editar Lista de Compras'
                : 'Adicionar Lista de Compras'
            }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-input
            v-model="editShoppingListName"
            label="Nome da Lista de Compras"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="primary" v-close-popup />
          <q-btn
            flat
            label="Salvar"
            color="primary"
            :loading="buttonLoading"
            :disable="buttonLoading"
            @click="saveShoppingList"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useShoppingListStore } from 'src/stores/shopping_list.store';
import { ShoppingList } from 'src/models/shopping_list/shopping_list';

const shoppingListStore = useShoppingListStore();

// Diálogo de edição/adição
const editDialog = ref(false);
const editShoppingListName = ref('');
let selectedShoppingListId = ref<number | null>(null);
let isEditMode = ref(false);
let buttonLoading = ref(false);

// Carregar lista de compras ao montar o componente
onMounted(async () => {
  await shoppingListStore.fetchShoppingList();
});

// Função para abrir o diálogo de edição
const openEditDialog = (shoppingList: ShoppingList) => {
  selectedShoppingListId.value = shoppingList.list_id;
  editShoppingListName.value = shoppingList.list_name;
  isEditMode.value = true;
  editDialog.value = true;
};

// Função para abrir o diálogo de adição
const openAddShoppingListDialog = () => {
  selectedShoppingListId.value = null; // Não há lista de compra selecionado ao adicionar
  editShoppingListName.value = ''; // Campo de nome vazio para adição
  isEditMode.value = false;
  editDialog.value = true;
};

// Função para salvar o lista de compra (edição ou criação)
const saveShoppingList = async () => {
  buttonLoading.value = true;

  try {
    if (isEditMode.value && selectedShoppingListId.value !== null) {
      // Edição do lista de compra
      await shoppingListStore.updateShoppingList(
        selectedShoppingListId.value,
        editShoppingListName.value
      );
    } else {
      // Criação de novo lista de compra
      await shoppingListStore.createShoppingList(editShoppingListName.value);
    }

    editDialog.value = false;
  } catch {
    console.error('Error no save Dialog em lista de compras');
  } finally {
    buttonLoading.value = false;
  }
};

// Função para excluir o lista de compra
const deleteShoppingList = async (list_id: number) => {
  await shoppingListStore.deleteShoppingList(list_id);
};
</script>
