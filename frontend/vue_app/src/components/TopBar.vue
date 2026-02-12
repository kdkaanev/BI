<script setup>
   import { useAuthStore } from '../store/authStore';

   const authStore = useAuthStore();

   
</script>


<template>
  <header class="topbar">
    <div class="left">
      <span class="title">Analysis</span>
    </div>

    <div class="right">
      <span class="plan">Free</span>
      <div class="avatar">U</div>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  height: 64px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.title {
  font-weight: 600;
}

.right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.plan {
  background: #eef2ff;
  color: #3730a3;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.avatar {
  width: 32px;
  height: 32px;
  background: #2563eb;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}
</style>
