import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useUploadStore } from "../store/uploadStore";
import { storeToRefs } from "pinia";
import axiosBI from "../config/axiosinstance";

export const useKpisAndInsightsStore = defineStore("kpisAndInsights", () => {
  const uploadStore = useUploadStore();
  const { uploaded } = storeToRefs(uploadStore);
  const insights = ref([]);
  const kpis = ref([]);
  const chart = ref(null);
  const loadingInsights = ref(false);

  const hasDataset = computed(() => !!uploadStore.uploaded);

  const fetchInsights = async () => {
    console.log("Starting fetchInsights...");
    if (!uploaded.value) {
      throw new Error("No dataset uploaded");
    }
    loadingInsights.value = true;
   

    const payload = {
      columns: uploaded.value.columns,
      rows_sample: uploaded.value.rows_sample || [],
    };
    try {
      console.log("Sending insights request with payload:", payload); 
      const response = await axiosBI.post("api/insights/analyze/", payload);
      console.log("Received insights response:", response.data);
      insights.value = response.data.insights || [];
      kpis.value = response.data.kpis || [];
      chart.value = response.data.chart || null;
    } catch (e) {
console.error("Error fetching insights:", e);
    } finally {
      loadingInsights.value = false;
    }
  }

  return {
    insights,
    kpis,
    chart,
    loadingInsights,
    hasDataset,   
    fetchInsights
  }
}
//   state: () => ({
//     insights: [],
//     kpis: [],
//     loadingInsights: false,
//     uploaded: null,
//   }),
//   getters: {
//     hasDataset() {
//       return !!this.uploaded;
//     },
//   },
//   setup() {
//     const uploadStore = useUploadStore()
//     const insights = ref([])
//     const kpis = ref([])
//     const loadingInsights = ref(false)
//     const uploaded = ref(null)

//     return {
//       insights,
//       kpis,
//       loadingInsights,
//       uploaded,
//     }   
//   }),
//   actions: {
//     async fetchInsights() {
//       this.loadingInsights = true
//       this.insights = []
//       this.kpis = []
//       try {
//         const payload = {
//           columns: this.uploaded.columns,
//           rows_sample: this.uploaded.rows_sample || []
//         }
//         const response = await axiosBI.post('api/insights/analyze/', payload)
//         this.insights = response.data.insights || []
//         this.kpis = response.data.kpis || []
//       }
//       catch (e) {
//       }
//       finally {
//         this.loadingInsights = false
//       }
  
// },
//     setUploadedDataset(data) {

//       this.uploaded = data
//       sessionStorage.setItem('uploadedData', JSON.stringify(this.uploaded))
//     }
//   },
// })
)