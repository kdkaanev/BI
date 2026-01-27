<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axiosBI from '../config/axiosinstance.js'
import { useUploadStore } from '../store/uploadStore.js'

const router = useRouter()
const store = useUploadStore()

const uploaded = ref(null)
const loading = ref(false)
const insights = ref([])
const kpis = ref([])

onMounted(() => {
  store.loadFromSession()
  uploaded.value = store.uploaded

  if (!uploaded.value) {
    router.push('/upload')
  }
})

function goUpload() {
  router.push('/upload')
}

async function showInsights() {
  if (!uploaded.value) return

  loading.value = true
  insights.value = []
  kpis.value = []

  try {
    const payload = {
      columns: uploaded.value.columns,
      rows_sample: uploaded.value.rows_sample || []
    }

    const res = await axiosBI.post('insights/analyze/', payload)

    kpis.value = res.data.kpis || []
    insights.value = res.data.insights || []
  } catch (e) {
    alert('Failed to analyze dataset.')
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="dashboard">

    <!-- HEADER -->
    <header class="dashboard-header">
      <div>
        <h1> Маин Dashboard</h1>
        <p class="subtitle" v-if="uploaded">
          Dataset: <strong>{{ uploaded.filename }}</strong> ·
          {{ uploaded.row_count }} rows ·
          {{ uploaded.columns.length }} columns
        </p>
        <p class="subtitle">
  Showing a small sample of the uploaded dataset
</p>
      </div>

      <div class="actions">
        <button
          class="btn primary"
          :disabled="loading"
          @click="showInsights"
        >
          {{ loading ? 'Analyzing…' : 'Analyze dataset' }}
        </button>

        <button class="btn link" @click="goUpload">
          Upload new
        </button>
      </div>
    </header>

    <!-- TABLE -->

    <section class="data-preview">
  <h2>Data preview</h2>

  <div class="table-wrapper">
    <table v-if="uploaded?.rows_sample?.length">
      <thead>
        <tr>
          <th
            v-for="col in uploaded.columns"
            :key="col.name"
          >
            {{ col.name }}
          </th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="(row, i) in uploaded.rows_sample.slice(0, 5)"
          :key="i"
        >
          <td
            v-for="col in uploaded.columns"
            :key="col.name"
          >
            {{ row[col.name] ?? '—' }}
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="empty">
      No sample rows available.
    </div>
  </div>
</section>

    <!-- KPI SECTION -->
    <section class="kpis">
      <template v-if="loading">
        <div v-for="i in 4" :key="i" class="kpi-card skeleton"></div>
      </template>

      <template v-else>
        <div
          v-for="kpi in kpis"
          :key="kpi.key"
          class="kpi-card"
          :class="kpi.severity"
        >
          <div class="kpi-label">{{ kpi.label }}</div>
          <div class="kpi-value">
            {{ kpi.value }}
            <span class="unit">{{ kpi.unit }}</span>
          </div>
        </div>
      </template>
    </section>

    <!-- INSIGHTS -->
    <section class="insights">
      <h2>Insights</h2>

      <div v-if="loading" class="insight skeleton"></div>

      <div v-else-if="!insights.length" class="empty">
        📊 No insights yet. Click <strong>Analyze dataset</strong>.
      </div>

      <div
        v-for="(insight, i) in insights"
        :key="i"
        class="insight"
        :class="insight.severity"
      >
        <div class="insight-title">
          {{ insight.title }}
        </div>
        <div class="insight-text">
          {{ insight.text }}
        </div>
      </div>
    </section>

  </div>
</template>



<style scoped>
/* ===== LAYOUT ===== */
.dashboard {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: system-ui, -apple-system, sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.subtitle {
  color: #666;
  font-size: 14px;
}

/* ===== ACTIONS ===== */
.actions {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.btn.primary {
  background: #2563eb;
  color: white;
}

.btn.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn.link {
  background: transparent;
  color: #2563eb;
}
/* ===== DATA PREVIEW ===== */
.data-preview {
  margin-bottom: 40px;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

thead {
  background: #f9fafb;
}

th, td {
  padding: 10px 12px;
  border-bottom: 1px solid #e5e7eb;
  white-space: nowrap;
}

th {
  text-align: left;
  font-weight: 600;
  color: #374151;
}

tbody tr:hover {
  background: #f3f4f6;
}

/* ===== KPIs ===== */
.kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 40px;
}

.kpi-card {
  padding: 16px;
  border-radius: 12px;
  background: #f9fafb;
  border-left: 6px solid #ddd;
}

.kpi-label {
  font-size: 14px;
  color: #555;
  margin-bottom: 6px;
}

.kpi-value {
  font-size: 28px;
  font-weight: 600;
}

.unit {
  font-size: 14px;
  color: #666;
  margin-left: 4px;
}

/* Severity */
.kpi-card.info { border-color: #3b82f6; }
.kpi-card.warning { border-color: #f59e0b; }
.kpi-card.critical { border-color: #ef4444; }

/* ===== INSIGHTS ===== */
.insights h2 {
  margin-bottom: 16px;
}

.insight {
  padding: 16px;
  border-radius: 10px;
  background: #f9fafb;
  border-left: 6px solid #ddd;
  margin-bottom: 12px;
}

.insight-title {
  font-weight: 600;
  margin-bottom: 6px;
}

.insight-text {
  color: #444;
  font-size: 14px;
}

/* Severity */
.insight.info { border-color: #3b82f6; }
.insight.warning { border-color: #f59e0b; }
.insight.critical { border-color: #ef4444; }

/* ===== EMPTY ===== */
.empty {
  padding: 24px;
  text-align: center;
  color: #666;
}

/* ===== SKELETON ===== */
.skeleton {
  background: linear-gradient(
    90deg,
    #eee 25%,
    #f5f5f5 37%,
    #eee 63%
  );
  background-size: 400% 100%;
  animation: shimmer 1.2s infinite;
}

.kpi-card.skeleton {
  height: 96px;
}

.insight.skeleton {
  height: 80px;
}

@keyframes shimmer {
  0% { background-position: 100% 0; }
  100% { background-position: -100% 0; }
}


</style>
