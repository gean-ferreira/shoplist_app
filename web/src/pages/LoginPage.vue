<template>
  <q-page class="q-px-sm">
    <h1 class="text-h4 text-center">Login</h1>
    <q-form @submit="onSubmit">
      <q-input
        v-model="username"
        label="Username"
        type="text"
        :rules="[(val:string) => !!val || 'Campo obrigatório']"
        filled
        class="q-mb-md"
      />
      <q-input
        v-model="password"
        label="Senha"
        type="password"
        :rules="[(val:string) => !!val || 'Campo obrigatório']"
        filled
        class="q-mb-md"
      />
      <q-btn label="Login" type="submit" color="primary" />
    </q-form>
  </q-page>
</template>

<script setup lang="ts">
defineOptions({
  name: 'LoginPage',
});

import { ref } from 'vue';
import { login } from '../services/auth.service';

const username = ref('');
const password = ref('');

const onSubmit = async () => {
  await login({ username: username.value, password: password.value }).catch(
    () => console.error('Ocorreu um erro no formulário de login')
  );
};
</script>
