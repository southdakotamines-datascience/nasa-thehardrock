<template>
  <div class="viz">

    <div class="results-text" v-if="result">
      <p><strong>Estimated Houses Damaged:</strong> {{ result.housesDamaged.toLocaleString() }}</p>
      <p><strong>Estimated House Destroyed:</strong> {{ result.housesDestroyed.toLocaleString() }}</p>
      <p><strong>Estimated Injuries:</strong> {{ result.injuries.toLocaleString() }}</p>
      <p><strong>Estimated Missing Persons:</strong> {{ result.missing.toLocaleString() }}</p>
      <p><strong>Estimated Deaths:</strong> {{ result.deaths.toLocaleString() }}</p>
      <p><strong>Estimated Damage (Millions of Dollars):</strong> {{ result.damageMillionsDollars.toLocaleString() }}</p>
    </div>

    <div id="impact-map" class="impact-map"></div>

  </div>
</template>


<script setup>
import { onMounted, watch, nextTick } from 'vue'
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

onMounted(async () => {
    await nextTick()

    // Initialize map once
    map = L.map('impact-map').setView([44.0805, -103.2310], 10) // Centered on Rapid City

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
  const lat = result.latitude ?? 0
  const lng = result.longitude ?? 0

  map.setView([lat, lng], 6)

  // Example radii in meters (these can come from your simulation backend)
  const radii = [
    { radius: result.severe_damage_radius_m ?? 5000, color: 'red', label: 'Severe damage' },
    { radius: result.moderate_damage_radius_m ?? 15000, color: 'orange', label: 'Moderate damage' },
    { radius: result.total_destruction_radius_m ?? 30000, color: 'yellow', label: 'Total destruction' }
  ]

    // Draw largest first, so smaller are on top and catch hover events
    radii
    .slice()            // copy the array so we don't mutate it
    .reverse()          // largest first
    .forEach(r => {
        L.circle([lat, lng], {
        radius: r.radius,
        color: r.color,
        fillColor: r.color,
        fillOpacity: 0.2,
        weight: 2
        })
        .addTo(map)
        .bindTooltip(r.label, { permanent: false });
    });
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
