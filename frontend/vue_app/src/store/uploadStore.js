import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axiosBI from '../config/axiosinstance'

export const useUploadStore = defineStore('dataset', () => {

  // State
  const uploaded = ref(null)
  const insights = ref([])
  const kpis = ref([])  
  const loadingInsights = ref(false)

  //getters
  const hasDataset = computed(() => !!uploaded.value)

  // Actions
  

  function setUploadedDataset(data) {

    uploaded.value = data
    sessionStorage.setItem('uploadedData', JSON.stringify(uploaded.value))
  }
  function clearData() {
    uploaded.value = null
    insights.value = []
    kpis.value = []
    sessionStorage.removeItem('uploadedData')
  }

  function loadFromSession() {
    const raw = sessionStorage.getItem('uploadedData')
    uploaded.value = raw ? JSON.parse(raw) : null
  }

  async function fetchInsights() {
    if (!uploaded.value) {
      throw new Error("No dataset uploaded")
    }
    loadingInsights.value = true
    insights.value = []
    kpis.value = []

    const payload = {
      columns: uploaded.value.columns,
      rows_sample: uploaded.value.rows_sample || []
    }
    try {
      const response = await axiosBI.post('insights/analyze/', payload)
      insights.value = response.data.insights || []
      kpis.value = response.data.kpis || []
    }
    catch (e) {
      }
    finally {
      loadingInsights.value = false
    }
  }

  return {
    uploaded,
    setUploadedDataset,
    loadFromSession,
    hasDataset,
    insights,
    kpis,
    loadingInsights,
    fetchInsights,
    clearData
  }
})
// Old Options API style store (for reference)


// export const useUploadStore = defineStore('dataset', {
//   state: () => ({
//     uploaded: null
//   }),
//   actions: {
//     setUploadedDataset(data) {
//       this.uploaded = data
//       sessionStorage.setItem('uploadedData', JSON.stringify(data))
//       const rows_sample = data.columns.sample_values || []
//       console.log("Uploaded dataset stored:", {
//         dataset_id: data.dataset_id,
//         columns: data.columns,
//         rows_sample: rows_sample
//       })
//     },
//     loadFromSession() {
//       const raw = sessionStorage.getItem('uploadedData')
//       this.uploaded = raw ? JSON.parse(raw) : null
//     }
//   }
// })
