import axiosBI from "../config/axiosinstance";
import { ref } from "vue";
import { useUploadStore } from "../store/uploadStore";

export const useKpisAndInsightsService = () => {
    const store = useUploadStore();
    const insights = ref([]);
    const loading = ref(false);

    const getInsightsAndKpis = async () => {
        loading.value = true;
        insights.value = [];

        try {
            const payload = {
                columns: store.uploaded.columns,
                rows_sample: store.uploaded.rows_sample || []
            };
            console.log("PAYLOAD INSIGHTS CHECK:", JSON.stringify(payload, null, 2));

            const res = await axiosBI.post("insights/analyze/", payload);

            insights.value = res.data;
            console.log("INSIGHTS RECEIVED:", insights.value);
        } catch (e) {
            console.error(e);
            alert("Error while analyzing dataset.");
        } finally {
            loading.value = false;
        }
    };

    return {
        insights,
        loading,
        getInsightsAndKpis
    };
};


// sync function getInsights() {
//   loading.value = true
//   insights.value = []

//   try {
//    const payload = {

//   columns: store.uploaded.columns,
//   rows_sample: store.uploaded.rows_sample || []
// }
// console.log("PAYLOAD INSIGHTS CHECK:", JSON.stringify(payload, null, 2))


//     const res = await axiosBI.post("insights/analyze/", payload)
    
//     insights.value = res.data
//     console.log("INSIGHTS RECEIVED:", insights.value)
//   }
//   catch (e) {
//     console.error(e)
//     alert("Error while analyzing dataset.")
//   }
//   finally {
//     loading.value = false
//   }
// }