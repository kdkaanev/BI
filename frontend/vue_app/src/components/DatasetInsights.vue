<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const props = defineProps({
  datasetId: Number
});

const insights = ref([]);

onMounted(async () => {
  const res = await axios.get(`/api/datasets/${props.datasetId}/`);
  insights.value = res.data.insights;
});
</script>



<template>
  <div>
    <h2 class="text-xl font-bold mb-2">Insights</h2>

    <div v-if="insights.length === 0">
      <p class="text-gray-500">No insights yet. Click Analyze.</p>
    </div>

    <ul class="space-y-3">
      <li 
        v-for="i in insights" 
        :key="i.id"
        class="p-3 border rounded bg-gray-50"
      >
        <span 
          class="text-sm font-bold uppercase"
          :class="{
            'text-blue-700': i.severity === 'info',
            'text-yellow-600': i.severity === 'warning',
            'text-red-600': i.severity === 'critical'
          }"
        >
          {{ i.severity }}
        </span>

        <h3 class="font-semibold">{{ i.title }}</h3>
        <p>{{ i.text }}</p>
      </li>
    </ul>
  </div>
</template>


