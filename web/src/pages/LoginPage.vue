<template>
  <q-page class="q-px-sm flex column flex-center">
    <LoginForm />
  </q-page>
</template>

<script setup lang="ts">
defineOptions({
  name: 'LoginPage',
});

import LoginForm from 'src/components/forms/LoginForm.vue';
</script>
