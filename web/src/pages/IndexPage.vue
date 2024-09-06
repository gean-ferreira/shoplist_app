<template>
  <q-page class="row items-center justify-evenly">
    Bem-vindo ao Lista de Compras App, {{ userStore.username }}
  </q-page>
</template>

<script setup lang="ts">
defineOptions({
  name: 'IndexPage',
});

import { useUserStore } from 'src/stores/user.store';
const userStore = useUserStore()
</script>
