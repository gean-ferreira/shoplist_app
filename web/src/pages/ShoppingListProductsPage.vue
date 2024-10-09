<template>
  <q-page class="q-pa-sm">
    <h1 class="text-h4 text-center">Produtos na Lista</h1>

    <!-- Skeleton enquanto carrega -->
    <q-list separator v-if="productInListStore.isLoading">
      <q-item v-for="i in 5" :key="i">
        <q-item-section>
          <q-skeleton type="text" />
          <q-skeleton type="text" />
          <q-skeleton type="text" />
        </q-item-section>
        <q-item-section side>
          <q-skeleton flat type="circle" height="42px" width="42px" />
          <q-skeleton flat type="circle" height="42px" width="42px" />
        </q-item-section>
      </q-item>
    </q-list>

    <!-- Notificação caso não tenha produtos na lista -->
    <q-list v-else separator style="margin-bottom: 78px">
      <!-- Verifica se a lista está vazia -->
      <q-item v-if="productInListStore.productsByList[list_id]?.length === 0">
        <q-item-section class="text-center q-pa-md">
          <q-icon name="category" size="lg" class="q-mx-auto" />
          <q-item-label> Nenhum produto na lista </q-item-label>
          <q-item-label caption
            >Adicione um produto usando o botão abaixo</q-item-label
          >
        </q-item-section>
      </q-item>

      <q-item
        v-for="product in productInListStore.productsByList[list_id]"
        :key="product.product_in_list_id"
      >
        <q-item-section>
          <q-item-label>{{
            filterByKey(
              productStore.products,
              'product_id',
              product.product_id
            )['product_name']
          }}</q-item-label>
          <q-item-label v-if="product.quantity_type === 'kg'" caption
            >Quantidade:
            {{ product.quantity.toFixed(3).toString().replace('.', ',') }}
            kg</q-item-label
          >
          <q-item-label v-if="product.quantity_type === 'unit'" caption
            >Quantidade: {{ product.quantity }}
            {{ product.quantity > 1 ? 'unidades' : 'unidade' }}</q-item-label
          >
          <q-item-label caption
            >Preço {{ product.quantity_type === 'kg' ? '(kg)' : 'unidade' }}: R$
            {{ formatValues(product.price) }}</q-item-label
          >
          <q-item-label caption
            >Total: R$
            {{ formatValues(product.price * product.quantity) }}</q-item-label
          >
        </q-item-section>

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

      <q-item v-if="productInListStore.productsByList[list_id]?.length">
        <h2 class="text-h5 text-center q-mx-auto">
          Total<br />R$ {{ formatValues(productInListStore.totalAmount) }}
        </h2>
      </q-item>
    </q-list>

    <!-- Botão para adicionar novo produto à lista -->
    <q-page-sticky position="bottom-right" :offset="[22, 22]">
      <q-btn round icon="add" color="primary" @click="openAddProductDialog" />
    </q-page-sticky>

    <!-- Diálogo para adicionar/editar produto na lista -->
    <q-dialog
      position="bottom"
      backdrop-filter="blur(4px) saturate(150%)"
      v-model="isDialogOpen"
    >
      <q-card>
        <q-card-section>
          <div class="text-h6">
            {{ isEditMode ? 'Editar Produto' : 'Adicionar Produto' }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="onSubmit">
            <q-select
              v-model="productInList.product_id"
              :options="options"
              option-label="product_name"
              @filter="filterFn"
              behavior="menu"
              use-input
              label="Produto"
              transition-show="jump-up"
              transition-hide="jump-down"
              :rules="[(val) => !!val || 'Você deve selecionar um produto']"
            />
            <q-radio
              class="q-my-md"
              dense
              v-model="productInList.quantity_type"
              val="unit"
              label="Unidade"
            />
            <q-radio
              class="q-ml-md"
              dense
              v-model="productInList.quantity_type"
              val="kg"
              label="Quilograma (kg)"
            />

            <q-input
              v-if="productInList.quantity_type === 'kg'"
              v-model="productInList.quantity"
              label="Quantidade"
              mask="#,### kg"
              fill-mask="0"
              reverse-fill-mask
              :rules="[
                (val) => !!val || 'Campo obrigatório',
                (val) =>
                  parseFloat(val.replace(',', '.')) > 0 ||
                  'A quantidade deve ser maior que 0',
              ]"
            />
            <q-input
              v-if="productInList.quantity_type === 'unit'"
              v-model="productInList.quantity"
              label="Quantidade"
              mask="##########"
              :rules="[
                (val) => !!val || 'Campo obrigatório',
                (val) =>
                  parseFloat(val.replace(',', '.')) > 0 ||
                  'A quantidade deve ser maior que 0',
              ]"
            />

            <q-input
              v-model="productInList.price"
              label="Preço"
              mask="##,##"
              reverse-fill-mask
              :rules="[
                (val) => !!val || 'Campo obrigatório',
                (val) =>
                  parseFloat(val.replace(',', '.')) >= 0 ||
                  'O preço não pode ser negativo',
              ]"
              prefix="R$"
            />
            <q-card-actions align="right">
              <q-btn flat type="button" label="Cancelar" v-close-popup />
              <q-btn
                flat
                type="submit"
                label="Salvar"
                color="primary"
                :loading="buttonLoading"
                :disable="buttonLoading"
              />
            </q-card-actions>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog
      v-model="isDeleteDialogOpen"
      backdrop-filter="blur(4px) saturate(150%)"
      persistent
    >
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
            @click="deleteProductFromList"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { Product } from 'src/models/product/product';
import {
  FormProductInList,
  ProductInListCreate,
} from 'src/models/product/product_in_list';
import { useProductStore } from 'src/stores/product.store';
import { useProductInListStore } from 'src/stores/product_in_list.store';
import { formatValues } from 'src/utils/functions/formatValues.function';
import { filterByKey } from 'src/utils/functions/filterByKey.function';
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

// Datas
const isDeleteDialogOpen = ref(false);
const productInListStore = useProductInListStore();
const productStore = useProductStore();
const isDialogOpen = ref(false);
const isEditMode = ref(false);
const productInList = ref<FormProductInList>({
  price: undefined,
  product_id: undefined,
  product_in_list_id: undefined,
  quantity: undefined,
  quantity_type: 'unit',
});
const productInListId = ref<number | null>(null);
const buttonLoading = ref(false);
const options = ref<Product[]>([]);
const route = useRoute();

// Methods
// Função para abrir o diálogo de adição
const openAddProductDialog = () => {
  isEditMode.value = false;
  productInList.value = {
    quantity_type: 'unit',
    quantity: undefined,
    price: undefined,
    product_id: undefined,
    product_in_list_id: undefined,
  };
  isDialogOpen.value = true;
};

// Função para abrir o diálogo de edição
const openEditDialog = (product: ProductInListCreate) => {
  isEditMode.value = true;
  productInList.value = {
    ...product,
    product_id: filterByKey(
      productStore.products,
      'product_id',
      product.product_id
    ),
    quantity:
      product.quantity_type === 'kg'
        ? product.quantity.toFixed(3).toString()
        : product.quantity.toString(),
    price: formatValues(product.price),
  };
  isDialogOpen.value = true;
};

// Função para salvar o produto
const onSubmit = async () => {
  buttonLoading.value = true;
  const productInListPayload = {
    product_in_list_id: productInList.value.product_in_list_id as number,
    product_id: productInList.value.product_id?.product_id as number,
    quantity_type: productInList.value.quantity_type,
    quantity: Number(
      productInList.value.quantity
        ?.toString()
        .replace(',', '.')
        .replace(' kg', '')
    ),
    price: Number(productInList.value.price?.toString().replace(',', '.')),
  };

  try {
    if (isEditMode.value) {
      // Edição do produto
      await productInListStore
        .updateProductInList(Number(list_id.value), productInListPayload)
        .then(() => (isDialogOpen.value = false));
    } else {
      // Criação de novo produto
      await productInListStore
        .createProductInList(Number(list_id.value), productInListPayload)
        .then(() => (isDialogOpen.value = false));
    }
  } catch {
    console.error('Error no save Dialog em Produtos');
  } finally {
    buttonLoading.value = false;
  }
};

// Função para abrir Dialog de exclusão
const openDeleteDialog = (product: ProductInListCreate) => {
  productInListId.value = product.product_in_list_id;
  isDeleteDialogOpen.value = true;
};

// Função para deletar produto da lista
const deleteProductFromList = async () => {
  buttonLoading.value = true;

  try {
    await productInListStore
      .deleteProductInList(
        Number(list_id.value),
        productInListId.value as number
      )
      .then(() => (isDeleteDialogOpen.value = false));
  } catch {
    console.error('Error no Delete Dialog em produtos da Lista de Compras');
  } finally {
    buttonLoading.value = false;
  }
};

const filterFn = (val: string, update: (fn: () => void) => void) => {
  if (val === '') {
    update(() => {
      options.value = productStore.products;
    });
    return;
  }

  update(() => {
    const needle = val.toLowerCase();
    options.value = productStore.products.filter(
      (p) => p.product_name.toLowerCase().indexOf(needle) > -1
    );
  });
};

// Computed
const list_id = computed(() => Number(route.params.list_id));

// Mounted
onMounted(async () => {
  const list_id = route.params.list_id;
  await productInListStore
    .fetchProductsInList(Number(list_id))
    .catch(() => console.error('Error na renderização dos produtos da lista.'));
});
</script>
