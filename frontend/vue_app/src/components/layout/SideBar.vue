<script setup>
   import { useAuthStore } from '../../store/authStore';
   import { useRouter } from 'vue-router';

   const authStore = useAuthStore();
    const router = useRouter();
    const logout = () => {
      authStore.logout();
      router.push('/');

    }
    defineProps({
      open: Boolean
    })
</script>



<template>
  <aside class="sidebar" :class="{ open: open}">
    <div class="logo">MyBI</div>
      <nav class="nav">
      <router-link to="/dashboard" class="nav-item">
        Dashboard
      </router-link>

      <router-link to="/analyses" class="nav-item">
        My Analyses
      </router-link>

      <router-link to="/upload" class="nav-item">
        Upload
      </router-link>

      <router-link to="/billing" class="nav-item">
        Billing
      </router-link>

      <router-link to="/settings" class="nav-item">
        Settings
      </router-link>
      <button class="nav-item logout" @click="logout">
  Logout
</button>

    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 120px;
  background: #111827;
  color: white;
  padding: 24px;

  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  z-index: 50;

  transition: transform 0.25s ease;
}
@media (min-width: 901px) {
  .sidebar {
    transform: translateX(0);
  
  }
}
@media (max-width: 900px) {
  .sidebar {
    transform: translateX(-100%);
  }
  .sidebar.open {
    transform: translateX(0);
  }
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
  text-decoration: none;
}

.nav-item:hover {
  background: #1f2937;
  color: white;
}

/* Активен route */
.router-link-exact-active {
  background: #2563eb;
  color: white;
}
.logout {
  width: 100%;
  text-align: left;
  background: transparent;
  border: none;
}


</style>
