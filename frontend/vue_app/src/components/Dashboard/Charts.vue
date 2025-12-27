<template>
  <div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import { onMounted, ref, watch } from 'vue'
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip } from 'chart.js'
Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip)

export default {
  props: ['chartData'],
  setup(props) {
    const canvas = ref(null)
    let chartInstance = null

    const draw = () => {
      if (!props.chartData || !canvas.value) return
      const ctx = canvas.value.getContext('2d')
      if (chartInstance) chartInstance.destroy()
      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: props.chartData.labels,
          datasets: [{
            label: props.chartData.label || 'Values',
            data: props.chartData.values || [],
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } }
        }
      })
    }

    onMounted(draw)
    watch(() => props.chartData, draw)

    return { canvas }
  }
}
</script>

<style scoped>
canvas { width:100%; height:300px; }
</style>
