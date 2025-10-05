<template>
  <div class="viz">

    <div class="results-text" v-if="result">
      <p><strong>Estimated Houses Destroyed:</strong> {{ result.housesDamaged.toLocaleString() }}</p>
      <p><strong>Estimated Death Toll:</strong> {{ result.deaths.toLocaleString() }}</p>
    </div>

    <div id="impact-map" class="impact-map"></div>

  </div>
</template>


<script setup>
import { onMounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Props: the simulation result from backend
const props = defineProps({
  result: {
    type: Object,
    required: true
  }
})

let map

onMounted(() => {
  // Initialize map once
  map = L.map('impact-map').setView([0, 0], 3) // Default center, can adjust

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map)

  drawCircles(props.result)
})

// Re-draw circles when new result comes in
watch(() => props.result, (newResult) => {
  if (map && newResult) {
    drawCircles(newResult)
  }
})

function drawCircles(result) {
  // Clear any old layers except the base tile layer
  map.eachLayer(layer => {
    if (!(layer instanceof L.TileLayer)) map.removeLayer(layer)
  })

  // Use the backend data or defaults for radius
  const lat = result.lat ?? 0
  const lng = result.lng ?? 0

  map.setView([lat, lng], 6)

  // Example radii in meters (these can come from your simulation backend)
  const radii = [
    { radius: result.total_destruction_radius_m ?? 5000, color: 'red', label: 'Total destruction' },
    { radius: result.severe_damage_radius_m ?? 15000, color: 'orange', label: 'Severe damage' },
    { radius: result.moderate_damage_radius_m ?? 30000, color: 'yellow', label: 'Moderate damage' }
  ]

  radii.forEach(r => {
    L.circle([lat, lng], {
      radius: r.radius,
      color: r.color,
      fillColor: r.color,
      fillOpacity: 0.2,
      weight: 2
    }).addTo(map).bindTooltip(r.label, { permanent: false })
  })
}
</script>

<style scoped>
.impact-visualization {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.results-text {
  text-align: left;
}

.impact-map {
  height: 400px;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
}
</style>
