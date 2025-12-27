<script setup>
import { ref, onMounted } from 'vue'
import { useUploadStore } from '../store/uploadStore.js'
import { useRouter } from 'vue-router'




const store = useUploadStore()
const router = useRouter()
const uploaded = store.uploaded
const insights = ref([])
const kpis = ref([])
const loading = ref(false)
const rows_sample = uploaded ? uploaded.rows_sample : []

onMounted(() => {
  store.loadFromSession()
})

const showUpload = () => {
  console.log('Show upload clicked')
  store.clearData()
  router.push('/upload')
}

async function showInsights() {
  console.log('Show insights clicked')
  loading.value = true
  await store.fetchInsights()
  insights.value = store.insights
  kpis.value = store.kpis
  loading.value = false
}
</script>



<template>
  <div class="dashboard">

    <!-- HEADER -->
    <header class="header">
      <h1>📊 Dashboard</h1>
      <button @click="showUpload">Upload New Dataset</button>
      <p v-if="uploaded">
        Dataset: <strong>{{ uploaded.filename }}</strong> ({{ uploaded.row_count }} rows)
      </p>
   
    </header>

    <!-- NO DATA -->
    <div v-if="!uploaded" class="empty">
      No dataset uploaded.
    </div>

    <template v-else>

      <!-- KPI SECTION -->
      <section class="kpis">
        <div
          v-for="(kpi, i) in kpis"
          :key="i"
          class="kpi-card"
        >
          <div class="kpi-value">{{ kpi.value }}</div>
          <div class="kpi-label">{{ kpi.label }}</div>
        </div>
      </section>

      <!-- SAMPLE TABLE -->
    

      <section class="table-section">
        <h2>Sample data</h2>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th v-for="col in uploaded.columns" :key="col.name">
                  {{ col.name }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in uploaded.rows_sample" :key="i">
                <td v-for="col in uploaded.columns" :key="col.name">
                  {{ row[col.name] }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- INSIGHTS -->
      <section class="insights">
        <div class="insights-header">
          <h2>Insights</h2>
          <button @click="showInsights" :disabled="loading">
            {{ loading ? 'Analyzing…' : 'Show Insights' }}
          </button>
        </div>

        <div v-if="loading" class="loading">
          Analyzing dataset…
        </div>

        <div v-else-if="insights.length === 0" class="empty">
          No insights yet.
        </div>


        <div class="insight-list">
             <small class="text-muted">
  Insights based on sample of {{ rows_sample.length }} rows
</small>
          <div
            v-for="(insight, i) in insights"
            :key="i"
            class="insight-card"
            :class="insight.severity"
          >
            <h3>{{ insight.title }}</h3>
            <p>{{ insight.text }}</p>
          </div>
        </div>
      </section>

    </template>

  </div>
</template>



<style scoped>
.dashboard {
  padding: 24px;
}

.header {
  margin-bottom: 24px;
}

.kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.kpi-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 10px rgba(0,0,0,.05);
  text-align: center;
}

.kpi-value {
  font-size: 28px;
  font-weight: bold;
}

.kpi-label {
  color: #666;
  margin-top: 4px;
}

.table-section {
  margin-bottom: 32px;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px 12px;
  border-bottom: 1px solid #eee;
  white-space: nowrap;
}

.insights-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.insight-list {
  display: grid;
  gap: 12px;
}

.insight-card {
  background: #fff;
  padding: 16px;
  border-radius: 12px;
  border-left: 5px solid #3b82f6;
}

.insight-card.warning {
  border-color: #f59e0b;
}

.insight-card.critical {
  border-color: #ef4444;
}

.loading,
.empty {
  color: #666;
  padding: 16px 0;
}
</style>
