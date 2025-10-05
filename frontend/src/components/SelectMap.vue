<template>
  <div id="select-map" class="select-map"></div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
const props = defineProps({
  longitude: Number,
  latitude: Number,
})

const emits = defineEmits(['update:longitude', 'update:latitude'])
var map

onMounted(() => {
  // Initialize map once
  const geographicCenterOfTheUS = [39.8283, -98.5795]
  map = L.map('select-map').setView(geographicCenterOfTheUS, 4)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors',
  }).addTo(map)

  let marker = null
  map.on('click', function (e) {
    debugger
    const { lat, lng } = e.latlng
    if (marker) {
      map.removeLayer(marker)
    }
    marker = L.marker([lat, lng]).addTo(map)
    emits('update:latitude', lat)
    emits('update:longitude', lng)
  })
})
</script>

<style>
.select-map {
  width: 500px;
  height: 500px;
}
</style>
