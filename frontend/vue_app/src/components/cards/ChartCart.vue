<script setup>
import { computed } from "vue";

const props = defineProps({
  title: String,
  subtitle: String,
  size: {
    type: String,
    default: "medium", // small | medium | large
  },
});

const sizeClass = computed(() => {
  return `size-${props.size}`;
});
</script>





<template>
  <div class="chart-card" :class="sizeClass">
    <div class="card-header" v-if="title || $slots.actions">
      <div class="title-group">
        <h2 v-if="title">{{ title }}</h2>
        <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
      </div>

      <div class="actions" v-if="$slots.actions">
        <slot name="actions"></slot>
      </div>
    </div>

    <div class="chart-body">
      <slot />
    </div>
  </div>
</template>


<style >
.chart-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 0;
}

/* Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.title-group h2 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.subtitle {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

.actions {
  display: flex;
  gap: 8px;
}

/* Body */
.chart-body {
  flex: 1;
  height: 100%;
  position: relative;
  width: 100%;
  min-height: 0;
}

/* Sizes */
.size-small {
  height: 220px;
}

.size-medium {
  height: 280px;
}

.size-large {
  height: 360px;
}
@media (max-width: 600px) {
  .size-large {
    height: 240px;
    
  }
  .chart-card{
    padding: 16px;
  }
}
</style>


