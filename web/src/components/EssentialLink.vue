<template>
  <q-item clickable exact tag="router-link" :to="props.link">
    <q-item-section v-if="props.icon" avatar>
      <q-icon :name="props.icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ props.title }}</q-item-label>
      <q-item-label v-if="props.caption" caption>{{
        props.caption
      }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script setup lang="ts">
defineOptions({
  name: 'EssentialLink',
});

export interface EssentialLinkProps {
  title: string;
  caption?: string;
  link?: string;
  icon?: string;
}

const props = defineProps<EssentialLinkProps>();
</script>

<style scoped>
.active-link {
  background-color: #e0f7fa;
  border-radius: 8px;
}
</style>
