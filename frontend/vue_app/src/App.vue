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
      <button v-if="authStore.getCurrentUser()" @click="logout" class="btn primary">logout</button>
    
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
.btn {
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.btn.primary {
  background: #2563eb;
  color: white;
}

</style>
