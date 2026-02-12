<template>
  <canvas ref="canvas"></canvas>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

const props = defineProps({
  labels: {
    type: Array,
    default: () => [],
  },
  data: {
    type: Array,
    default: () => [],
  },
});

const canvas = ref(null);
let chartInstance = null;

function renderChart() {
  if (!canvas.value) return;

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(canvas.value, {
    type: "bar",
    data: {
      labels: props.labels,
      datasets: [
        {
          label: "Value",
          data: props.data,
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  });
}

onMounted(renderChart);

watch(
  () => [props.labels, props.data],
  renderChart,
  { deep: true }
);

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
