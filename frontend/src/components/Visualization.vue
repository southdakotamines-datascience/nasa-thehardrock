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
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
  position: relative;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.modal-close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}
</style>

