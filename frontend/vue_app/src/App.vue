<script setup>

import UploadWizard from './components/UploadWizard.vue';
import Dashboard from './views/Dashboard.vue';
import { onMounted, ref } from 'vue';
import Login from './views/Login.vue';


import { useAuthStore } from './store/authStore';
const authStore = useAuthStore();
import { useRouter } from 'vue-router';
const router = useRouter();
const logout = () => {
  authStore.logout();
  router.push('/');
};

onMounted(() => {
  if (!authStore.getCurrentUser()) {
    router.push('/');
  }
  authStore.getCurrentUser();
});

</script>

<template>
  <div id="app">
    <div class="nav">

      <img alt="BI SaaS logo" class="logo" src="./assets/logo.png" />
      <button v-if="authStore.getCurrentUser()" @click="logout">logout</button>
      <button v-else @click="router.push('/')">login</button>
    </div>
    <router-view />
  </div>


</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}
</style>
