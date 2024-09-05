<template>
  <q-page class="row items-center justify-evenly">
    Bem-vindo ao Lista de Compras App
    <q-btn label="Go to Login" @click="goToLogin" />
  </q-page>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

defineOptions({
  name: 'IndexPage',
});

const router = useRouter();

const goToLogin = () => {
  router.push('/login');
};
</script>
