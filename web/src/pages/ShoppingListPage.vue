<template>
  <q-page class="q-pa-sm">
    <h1 class="text-h4 text-center">Listas de compras</h1>

    <!-- Skeleton enquanto carrega -->
    <q-list separator v-if="shoppingListStore.isLoading">
      <q-item v-for="i in 5" :key="i">
        <q-item-section>
          <q-skeleton type="text" />
          <q-skeleton
            type="text"
            width="50%"
            class="q-item__label q-item__label--caption text-caption"
          />
        </q-item-section>
        <q-item-section side>
          <q-skeleton flat type="circle" height="42px" width="42px" />
          <q-skeleton flat type="circle" height="42px" width="42px" />
        </q-item-section>
      </q-item>
    </q-list>

    <!-- Notificação caso não tenha produtos na lista -->
    <q-list v-else separator style="margin-bottom: 78px" v-auto-animate>
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
        clickable
        v-ripple
      >
        <!-- Nome da lista como um link para a página de produtos -->
        <q-item-section @click="goToListDetails(list.list_id)">
          <q-item-label>{{ list.list_name }} </q-item-label>
          <q-item-label caption>Ver detalhes da lista</q-item-label>
        </q-item-section>

        <!-- Botões de editar e excluir -->
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
            @click="openDeleteDialog(list)"
            color="negative"
          />
        </q-item-section>
      </q-item>
    </q-list>

    <!-- Botão para adicionar novo lista de compra -->
    <q-page-sticky position="bottom-right" :offset="[22, 22]">
      <q-btn
        round
        icon="add"
        color="primary"
        @click="openAddShoppingListDialog"
      />
    </q-page-sticky>

    <!-- Diálogo para editar ou adicionar lista -->
    <q-dialog
      position="bottom"
      backdrop-filter="blur(4px) saturate(150%)"
      v-model="editDialog"
    >
      <q-card>
        <q-card-section>
          <h2 class="text-h6">
            {{
              isEditMode
                ? 'Editar Lista de Compras'
                : 'Adicionar Lista de Compras'
            }}
          </h2>
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

    <!-- Diálogo para deletar produto -->
    <q-dialog
      v-model="isDeleteDialogOpen"
      backdrop-filter="blur(4px) saturate(150%)"
      persistent
    >
      <q-card>
        <q-card-section>
          <h2 class="text-h6">
            Tem certeza que deseja excluir
            <span class="text-accent">{{ editShoppingListName }}</span> das
            listas de compras?
          </h2>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="primary" v-close-popup />
          <q-btn
            flat
            label="Excluir"
            color="negative"
            :loading="buttonLoading"
            :disable="buttonLoading"
            @click="deleteShoppingList"
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
import { useRouter } from 'vue-router';
import { vAutoAnimate } from '@formkit/auto-animate/vue';

// Data
const isDeleteDialogOpen = ref(false);
const shoppingListStore = useShoppingListStore();
const router = useRouter();
const editDialog = ref(false);
const editShoppingListName = ref('');
const selectedShoppingListId = ref<number | null>(null);
const isEditMode = ref(false);
const buttonLoading = ref(false);

// Mounted
// Carregar lista de compras ao montar o componente
onMounted(async () => {
  await shoppingListStore.fetchShoppingList();
});

// Methods
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

// Função para abrir Dialog de exclusão
const openDeleteDialog = (shoppingList: ShoppingList) => {
  selectedShoppingListId.value = shoppingList.list_id;
  editShoppingListName.value = shoppingList.list_name;
  isDeleteDialogOpen.value = true;
};

// Função para excluir o lista de compra
const deleteShoppingList = async () => {
  buttonLoading.value = true;

  try {
    await shoppingListStore
      .deleteShoppingList(selectedShoppingListId.value as number)
      .then(() => (isDeleteDialogOpen.value = false));
  } catch {
    console.error('Error no Delete Dialog em Listas de Compras');
  } finally {
    buttonLoading.value = false;
  }
};

const goToListDetails = (list_id: number) => {
  router.push({
    name: 'Produtos da lista',
    params: { list_id: list_id.toString() }, // Convertendo o número para string
  });
};
</script>
