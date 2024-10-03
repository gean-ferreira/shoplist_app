<template>
  <q-page class="q-px-sm">
    <h1 class="text-h4 text-center">Produtos</h1>

    <!-- Skeleton enquanto carrega -->
    <q-list separator v-if="productStore.isLoading">
      <q-item v-for="i in 5" :key="i">
        <q-item-section>
          <q-skeleton type="text" />
        </q-item-section>
        <q-item-section side>
          <q-skeleton flat type="circle" height="42px" width="42px" />
          <q-skeleton flat type="circle" height="42px" width="42px" />
        </q-item-section>
      </q-item>
    </q-list>

    <!-- Listagem de produtos -->
    <q-list separator v-else style="margin-bottom: 78px">
      <!-- Verifica se a lista está vazia -->
      <q-item v-if="productStore.products.length === 0">
        <q-item-section class="text-center q-pa-md">
          <q-icon name="category" size="lg" class="q-mx-auto" />
          <q-item-label> Nenhum produto disponível </q-item-label>
          <q-item-label caption>Adicione um novo produto abaixo</q-item-label>
        </q-item-section>
      </q-item>

      <!-- Renderiza os produtos se houver -->
      <q-item
        v-for="product in productStore.products"
        :key="product.product_id"
      >
        <!-- Nome do produto -->
        <q-item-section>
          <q-item-label>{{ product.product_name }}</q-item-label>
        </q-item-section>

        <!-- Botões de editar e excluir -->
        <q-item-section side>
          <q-btn
            flat
            round
            icon="edit"
            @click="openEditDialog(product)"
            color="primary"
          />
          <q-btn
            flat
            round
            icon="delete"
            @click="openDeleteDialog(product)"
            color="negative"
          />
        </q-item-section>
      </q-item>

      <!-- Botão para adicionar novo produto -->
      <q-page-sticky position="bottom-right" :offset="[18, 18]">
        <q-btn
          round
          icon="add"
          color="primary"
          @click="openAddProductDialog"
        />
      </q-page-sticky>
    </q-list>

    <!-- Diálogo para editar ou adicionar produto -->
    <q-dialog
      position="bottom"
      backdrop-filter="blur(4px) saturate(150%)"
      v-model="editDialog"
    >
      <q-card>
        <q-card-section>
          <div class="text-h6">
            {{ isEditMode ? 'Editar Produto' : 'Adicionar Produto' }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-input v-model="editProductName" label="Nome do Produto" />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="primary" v-close-popup />
          <q-btn
            flat
            label="Salvar"
            color="primary"
            :loading="buttonLoading"
            :disable="buttonLoading"
            @click="saveProduct"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Diálogo para deletar produto -->
    <q-dialog v-model="isDeleteDialogOpen" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">Tem certeza que deseja excluir este item?</div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="primary" v-close-popup />
          <q-btn
            flat
            label="Excluir"
            color="negative"
            :loading="buttonLoading"
            :disable="buttonLoading"
            @click="deleteProduct"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useProductStore } from 'src/stores/product.store';
import { Product } from 'src/models/product/product';

const productStore = useProductStore();
const isDeleteDialogOpen = ref(false);
const editDialog = ref(false);
const editProductName = ref('');
let selectedProductId = ref<number | null>(null);
let isEditMode = ref(false);
let buttonLoading = ref(false);

// Carregar produtos ao montar o componente
onMounted(async () => {
  await productStore.fetchProducts();
});

// Função para abrir o diálogo de edição
const openEditDialog = (product: Product) => {
  selectedProductId.value = product.product_id;
  editProductName.value = product.product_name;
  isEditMode.value = true;
  editDialog.value = true;
};

// Função para abrir o diálogo de adição
const openAddProductDialog = () => {
  selectedProductId.value = null; // Não há produto selecionado ao adicionar
  editProductName.value = ''; // Campo de nome vazio para adição
  isEditMode.value = false;
  editDialog.value = true;
};

// Função para salvar o produto (edição ou criação)
const saveProduct = async () => {
  buttonLoading.value = true;

  try {
    if (isEditMode.value && selectedProductId.value !== null) {
      // Edição do produto
      await productStore.updateProduct(
        selectedProductId.value,
        editProductName.value
      );
    } else {
      // Criação de novo produto
      await productStore.createProduct(editProductName.value);
    }

    editDialog.value = false;
  } catch {
    console.error('Error no save Dialog em Produtos');
  } finally {
    buttonLoading.value = false;
  }
};
// Função para abrir Dialog de exclusão
const openDeleteDialog = (product: Product) => {
  selectedProductId.value = product.product_id;
  isDeleteDialogOpen.value = true;
};

// Função para excluir o produto
const deleteProduct = async () => {
  buttonLoading.value = true;

  try {
    await productStore
      .deleteProduct(selectedProductId.value as number)
      .then(() => (isDeleteDialogOpen.value = false));
  } catch {
    console.error('Error no Delete Dialog em Produtos');
  } finally {
    buttonLoading.value = false;
  }
};
</script>
