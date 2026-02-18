<script setup>
    import { computed } from 'vue';
    

</script>


<template>
    <section class="kpi-grid">
        <div
            v-for="kpi in kpis"
            :key="kpi.key"
            class="kpi-card"
            
        >
        <div class="kpi-label">{{ kpi.label }}</div>
        <div class="kpi-value">{{ kpi.value }}</div>
        <div class="kpi-sub">{{ kpi.description }}</div>

        </div>

    </section>
</template>