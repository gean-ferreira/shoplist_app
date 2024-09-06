import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '' as string,
  }),
  actions: {
    setUsername(username: string) {
      this.username = username;
    },
    clearUsername() {
      this.username = '';
    }
  },
});
