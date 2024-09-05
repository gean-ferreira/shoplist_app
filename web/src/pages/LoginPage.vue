<template>
  <q-page class="q-px-sm">
    <h1 class="text-h4 text-center">Login</h1>
    <q-form @submit="onSubmit" @reset="onReset">
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
      <q-card-actions align="right">
        <q-btn label="Login" type="submit" color="primary" />
        <q-btn label="Reset" type="reset" color="secondary" flat />
      </q-card-actions>
    </q-form>
  </q-page>
</template>

<script setup lang="ts">
defineOptions({
  name: 'LoginPage',
});

import { ref } from 'vue';

const username = ref('');
const password = ref('');

const onSubmit = () => {
  if (username.value && password.value) {
    // Aqui você faria a lógica de autenticação
    console.log('Login:', username.value, password.value);
  }
};

const onReset = () => {
  username.value = '';
  password.value = '';
};
</script>
