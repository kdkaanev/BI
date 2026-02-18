<script setup>
import Sidebar from "../components/layout/SideBar.vue";
import Topbar from "../components/layout/TopBar.vue";
import KpiCard from "../components/cards/KpiRow.vue";
import InsightCard from "../components/cards/InsightsRow.vue";
import ChartCard from "../components/cards/ChartCart.vue";
import LineChart from "../components/charts/LineChart.vue";
import BarChart from "../components/charts/BarChart.vue";

import { useUploadStore } from '../store/uploadStore.js'
import { useKpisAndInsightsStore } from "../store/kpisAndInsightsStore.js";
import { ref, onMounted } from 'vue'
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

const router = useRouter()
const store = useUploadStore()
const kpisAndInsightsStore = useKpisAndInsightsStore()
const { kpis, insights, chart } = storeToRefs(kpisAndInsightsStore)

const uploaded = ref(null)
const loading = ref(false)


onMounted(() => {
  store.loadFromSession()
  uploaded.value = store.uploaded
  if (kpisAndInsightsStore.hasDataset) {
    kpisAndInsightsStore.fetchInsights() // Automatically analyze dataset on mount if dataset is uploaded
  } 

    if (!uploaded.value) {
        router.push('/upload')
    }
  
})

function goUpload() {
  router.push('/upload')
}

async function showInsights() {
  if (!kpisAndInsightsStore.hasDataset) {
    alert("Please upload a dataset first.");
    return;
  }
  console.log("Fetching insights for dataset ID:", kpisAndInsightsStore.datasetId);

  try {
    loading.value = true;
    await kpisAndInsightsStore.fetchInsights();
  } catch (e) {
    alert("Error fetching insights: " + e.message);
  } finally {
    loading.value = false;
  }
}


</script>




<template>
  <div class="app-layout">
    

    <div class="main-area">


      <main class="content">
        <!-- Page header -->
        <section class="page-header">
          <h1 v-if="uploaded">{{ uploaded.filename }} <span @click="showInsights" class="refresh-btn" >refresh analyze</span><span @click="goUpload" class="refresh-btn">upload new file</span></h1>
          <p v-if="uploaded">Showing a small sample of the uploaded dataset</p>
        </section>
       

        <!-- KPI row -->
        <section class="kpi-row">
            
          <KpiCard v-for="kpi in kpis" 
          :key="kpi.key" 
          :label="kpi.label" 
          :value="kpi.value" 
          :sub="kpi.unit" />
        </section>

        <!-- Insights -->
        <section class="insights-row">
          <InsightCard v-for="(insight, index) in insights.slice(0, 6)" 
          :key="index" 
          :title="insight.title" 
          :text="insight.text" 
          :severity="insight.severity" />   
          
        </section>

        <!-- Chart -->
         <ChartCard
  v-if="chart"
  :title="chart.title"
  size="large"
>
  <LineChart
    v-if="chart.type === 'line'"
    :labels="chart.labels"
    :data="chart.values"
  />

  <BarChart
    v-else-if="chart.type === 'bar'"
    :labels="chart.labels"
    :data="chart.values"
  />
</ChartCard>


        <!-- Data preview -->
         <section class="card data-preview">
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

      </main>
    </div>
  </div>
</template>



<style scoped>


.app-layout {
  display: flex;
  min-height: 100vh;
  background: #f6f7f9;
}

/* Main area */
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Content */
.content {
  padding: 32px;
  width: 100%;
  max-width: 1080px;
  margin: 0 auto;
  
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* Page header */
.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

/* KPI row */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

/* Insights row */
.insights-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

/* Cards */
.card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 24px;
}

.card h2 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
}

/* Charts */
.chart-large {
  height: 360px;
}

.chart-small {
  height: 280px;
}

.secondary-charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.chart-placeholder {
  background: #f3f4f6;
  height: 100%;
  border-radius: 8px;
}

/* Table */
.data-preview table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.data-preview th,
.data-preview td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}
.refresh-btn {
  font-size: 14px;
  color: #2563eb;
  cursor: pointer;
  margin-left: 16px;
}
.refresh-btn:hover {
  text-decoration: underline;
}
.chart-body {
  flex: 1;
  height: 100%;
  position: relative;
}
.table-wrapper {
  width: 100%;
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}
@media (max-width: 900px) {
  .content {
    padding: 20px;
    gap: 24px;
  }
  .kpi-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  .insights-row {
    grid-template-columns: 1fr;
    
}
}

@media (max-width: 600px) {
  .card {
    padding: 16px;
  }
}
@media (max-width: 600px) {
  .content {
    max-width: 100% !important;
    width: 100% !important;
    padding: 16px !important;
    margin: 0 !important;
  }
  .kpi-row {
    grid-template-columns: 1fr;
    
  }
}
@media (max-width: 600px) {
  .chart-card {
    width: 100% !important;
    max-width: 100% !important;
  }
}

@media (max-width: 600px) {
  .data-preview table {
    min-width: 600px;
  }
}

</style>
