<script setup>
   import { useAuthStore } from '../store/authStore';
   import { useRouter } from 'vue-router';

   const authStore = useAuthStore();


</script>



<template>
  <aside class="sidebar">
    <div class="logo">MyBI</div>

    <nav>
      <a class="nav-item active">Dashboard</a>
      <a class="nav-item">My Analyses</a>
      <a class="nav-item" @click="$router.push('/upload')">Upload</a>
      <a class="nav-item">Billing</a>
      <a class="nav-item">Settings</a>
      <a class="nav-item" @click="authStore.logout">Logout</a>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 240px;
  background: #111827;
  color: white;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 40px;
}

.nav-item {
  display: block;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  color: #d1d5db;
}

.nav-item:hover {
  background: #1f2937;
  color: white;
}

.active {
  background: #2563eb;
  color: white;
}
</style>
