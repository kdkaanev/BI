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
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize();
  }
};
let resizeObserver = null;

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
const observeResize = () => {
  if (!canvas.value) return;

  const parent = canvas.value.parentElement;

  resizeObserver = new ResizeObserver(() => {
    if (chartInstance) {
      chartInstance.resize();
    }
  });

  resizeObserver.observe(parent);
};


onMounted(() => {
  renderChart();
 observeResize();
});


watch(
  () => [props.labels, props.data],
  renderChart,
  { deep: true }
);

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
  if (resizeObserver) {
    resizeObserver.disconnect();
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
    display: block;
  max-width: 100% !important;
  }
  </style>


