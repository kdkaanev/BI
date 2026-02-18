<script setup>

import UploadWizard from '../src/views/UploadWizard.vue';

import { onMounted, ref } from 'vue';
import Login from './views/Login.vue';
import SideBar from './components/layout/SideBar.vue';
import TopBar from './components/layout/TopBar.vue'; 


import { useAuthStore } from './store/authStore';
const authStore = useAuthStore();
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(() => {
  authStore.initAuth();
});
const sidebarOpen = ref(false);
</script>

<template>
  <div id="app">
    <SideBar 
      :open="sidebarOpen"
      @close="sidebarOpen = false"

    />
    <div class="main-area">
      <TopBar 
        :title="$route.meta.title || 'Dashboard'"
        @toggleSidebar="sidebarOpen = true" />
       <router-view />
      
    </div>
    <div
      v-if="sidebarOpen"
      class="overlay"
      @click="sidebarOpen = false"
    ></div>
    
  </div>


</template>

<style>
@media (max-width: 900px) {
  .content {
    padding: 20px;
    gap: 24px;
  }
  .kpi-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  .insights-row {
    grid-template-columns: 1fr;
    
}
}
@media (max-width: 600px) {
  .content {
    padding: 16px;
    gap: 20px;
  }
  .kpi-row {
    grid-template-columns: 1fr;
    
  }
}
#app {
  display: flex;
  height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f9fafb;
  width: 100%;
}
.main-area {
  flex: 1;
  margin-left: 6rem;
  display: flex;
  flex-direction: column;

}
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 40;
}
@media (max-width: 768px) {
  .main-area {
    margin-left: 0;
  }
}
</style>
