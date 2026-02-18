<script setup>
defineProps({
  text: String,
  title: String,
  severity: String, // e.g. "info", "warning", "critical"
});
</script>




<template>
  <div class="insight-card">
    <span class="icon">💡</span>
    <div>
      <strong>{{ title }}</strong>
      <p>{{ text }}</p>
    </div>
    
  </div>
</template>



<style scoped>
.insight-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  gap: 12px;
  font-size: 14px;
  line-height: 1.5;
}

.icon {
  font-size: 18px;
}
</style>
