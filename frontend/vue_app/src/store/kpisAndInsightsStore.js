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
  const analysisId = ref(null);
  const status = ref(null);

  const hasDataset = computed(() => !!uploaded.value);

  // STEP 1: trigger analysis
  const fetchInsights = async () => {

    if (!uploaded.value?.dataset_id) {
      throw new Error("No dataset id");
    }

    loadingInsights.value = true;

    try {

      const response = await axiosBI.post(
        `api/datasets/${uploaded.value.dataset_id}/analyze/`
      );

      analysisId.value = response.data.analysis_id;
      status.value = response.data.status;

      // start polling
      pollAnalysis();

    } catch (e) {

      console.error("Error triggering analysis:", e);
      loadingInsights.value = false;

    }

  };

  // STEP 2: poll until completed
  const pollAnalysis = async () => {

    if (!analysisId.value) return;

    try {

      const response = await axiosBI.get(
        `api/analyses/${analysisId.value}/`
      );

      status.value = response.data.status;

      if (status.value === "completed") {

        insights.value = response.data.insights || [];
        kpis.value = response.data.kpis || [];
        chart.value = response.data.chart || null;

        loadingInsights.value = false;

        return;

      }

      if (status.value === "failed") {

        console.error("Analysis failed");
        loadingInsights.value = false;

        return;

      }

      // still processing → poll again
      setTimeout(pollAnalysis, 2000);

    } catch (e) {

      console.error("Polling error:", e);
      loadingInsights.value = false;

    }

  };

  return {

    insights,
    kpis,
    chart,

    loadingInsights,
    hasDataset,

    fetchInsights,

    status

  };

});