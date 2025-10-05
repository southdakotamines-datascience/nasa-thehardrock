<template>
  <div class="viz">
    <h2>Impact Visualization</h2>

    <div v-if="result">
      <!-- Example: replace with map/chart later -->
      <p><strong>Estimated houses destroyed:</strong> {{ result.houses_destroyed }}</p>
      <p><strong>Estimated casualties:</strong> {{ result.casualties }}</p>

      <!-- You could also plug in charts or Leaflet here -->
    </div>

    <div v-else>
      <p>No data yet — run a simulation above.</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  result: {
    type: Object,
    required: false
  }
})
</script>

<style scoped>
.viz {
  margin-top: 2rem;
  padding: 1rem;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #eee;
}
</style>
