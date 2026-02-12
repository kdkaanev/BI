<script setup>
defineProps({
  label: String,
  value: [String, Number],
  sub: String,
});
</script>



<template>
  <div class="kpi-card">
    <span class="label">{{ label }}</span>
    <span class="value">{{ value }}</span>
    <span class="sub">{{ sub }}</span>
  </div>
</template>



<style scoped>
.kpi-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label {
  font-size: 12px;
  color: #6b7280;
}

.value {
  font-size: 28px;
  font-weight: 700;
}

.sub {
  font-size: 12px;
  color: #9ca3af;
}
</style>
