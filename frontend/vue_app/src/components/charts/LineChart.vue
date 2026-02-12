<script setup>
import { onMounted, ref, onBeforeUnmount, watch } from "vue";
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
);

const props = defineProps({
  labels: Array,
  data: Array,
});

const canvas = ref(null);
let chartInstance = null;

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(canvas.value, {
    type: "line",
    data: {
      labels: props.labels,
      datasets: [
        {
          label: "Revenue",
          data: props.data,
          borderWidth: 2,
          tension: 0.3,
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
};

onMounted(renderChart);

watch(() => props.data, renderChart);

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<template>
  <canvas ref="canvas"></canvas>
</template>

<style scoped>
 canvas {
   width: 100% !important;
   height: 100% !important; 
  }
  </style>


