<template>
  <header class="topbar">
    <!-- Left side -->
    <div class="left">
      <button class="hamburger" @click="$emit('toggleSidebar')">
        ☰
      </button>

      <h1 class="page-title">{{ title }}</h1>
    </div>

    <!-- Right side -->
    <div class="right">
      <div class="user">
        <div class="avatar">U</div>
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: "Dashboard",
  },
});
</script>

<style scoped>
.topbar {
  height: 64px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 24px;
  
  display: flex;
  align-items: center;
  justify-content: space-around;
}

/* Left side */
.left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

/* Right side */
.right {
  display: flex;
  align-items: center;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

/* Hamburger */
.hamburger {
  font-size: 22px;
  background: none;
  border: none;
  cursor: pointer;
  display: none;
}

/* Mobile */
@media (max-width: 900px) {
  .hamburger {
    display: block;
  }

  .page-title {
    font-size: 16px;
  }
}
</style>
