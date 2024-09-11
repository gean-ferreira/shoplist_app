<template>
  <q-form @submit="onSubmit" style="max-width: 300px; width: 100%">
    <h1 class="text-h4 text-center">Login</h1>
    <q-input
      v-model="form.username"
      label="Username"
      type="text"
      :rules="[(val:string) => !!val || 'Campo obrigatório']"
      filled
      class="q-mb-md"
    />
    <q-input
      v-model="form.password"
      label="Senha"
      type="password"
      :rules="[(val:string) => !!val || 'Campo obrigatório']"
      filled
      class="q-mb-md"
    />
    <q-btn
      label="Login"
      type="submit"
      color="primary"
      :loading="isLoading"
      :disable="isLoading"
    />
  </q-form>
</template>

<script setup lang="ts">
defineOptions({
  name: 'LoginForm',
});

import { ref, reactive } from 'vue';
import { login } from 'src/services/auth.service';
import { useRouter } from 'vue-router';
import { useUserStore } from 'src/stores/user.store';
import type { LoginForm } from 'src/models/auth/login';

const form = reactive<LoginForm>({
  username: '',
  password: '',
});

const isLoading = ref(false);
const router = useRouter();
const userStore = useUserStore();

const onSubmit = async () => {
  isLoading.value = true;

  await login({ username: form.username, password: form.password })
    .then(() => {
      userStore.setUsername(form.username);
      router.push('/');
    })
    .catch(() => console.error('Ocorreu um erro no formulário de login'))
    .finally(() => (isLoading.value = false));
};
</script>
