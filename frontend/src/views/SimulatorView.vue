<template>
  <section class="page simulator-page">
    <div class="wrapper">
      <h1>Simulator</h1>

      <!-- Visualization Dialog: only shows when both showModal & simulationResult are set -->
      <Dialog v-model:visible="showModal" modal header="Impact Visualization"
        :style="{ width: '700px', maxWidth: '90vw' }">
        <Visualization v-if="simulationResult" :result="simulationResult" />
      </Dialog>

      <form class="sim-form" @submit.prevent="handleSubmit">

        <div class="form-row">
          <label for="velocity">Velocity (m)</label>
            <InputText
                id="velocity"
                type="number"
                v-model.number="velocity"
                :min="velocityMin"
                :max="velocityMax"
                :step="velocityStep"
            />  
          <Slider
                v-model="velocity"
                :min="velocityMin"
                :max="velocityMax"
                :step="velocityStep"
                style="width: 100%;"
                aria-label="Velocity slider"
            />
        </div>

        <div class="form-row">
          <label for="mass">Mass (kg)</label>
          <InputText
            id="mass"
            type="number"
            v-model.number="mass"
            :min="massMin"
            :max="massMax"
            :step="massStep"
          />
          <Slider
            v-model.number="mass"
            :min="massMin"
            :max="massMax"
            :step="massStep"
            style="width: 100%;"
            aria-label="Mass slider"
          />
        </div>

        <SelectMap :latitude="lat" :longitude="long" @update:latitude="updateLatitude"
          @update:longitude="updateLongitude" />
        <div class="value">Latitude Selected: {{ lat }}</div>
        <div class="value">Longitude Selected: {{ long }}</div>

        <div class="form-actions">
          <button type="submit" class="btn">Submit</button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import SelectMap from '../components/SelectMap.vue'
import Dialog from 'primevue/dialog'

// Visualization.
const showModal = ref(false)
import Visualization from '../components/Visualization.vue'
const simulationResult = ref(null)

// Assumptions for ranges of sliders; change as needed
// km/s
const velocityMin = 0
const velocityMax = 72 // practical upper bound for entry velocity due to gravity and relative earth velocity or something
const velocityStep = 1

// kg
const massMin = 0.01
const massMax = 1000
const massStep = 1

const velocity = ref(20)
const mass = ref(100)
const lat = ref(0)
const long = ref(0)

// const formatMass = computed(() => {
//   if (mass.value >= 1e6) return (mass.value / 1e6).toFixed(2) + // 'M'
//   if (mass.value >= 1e3) return (mass.value / 1e3).toFixed(2) + // 'k'
//   return mass.value
// })
function updateLatitude(newLat) {
  lat.value = newLat
}

function updateLongitude(newLong) {
  long.value = newLong
}

async function handleSubmit() {
  // Basic validation
  if (velocity.value < 0 || mass.value <= 0) {
    alert('Please enter positive values for velocity and mass.')
    return
  }

  const payload = {
    velocity: velocity.value,
    mass: mass.value,
    longitude: long.value,
    latitude: lat.value,
  }

  try {
    // Send payload to flask, listening at localhost.../simulate for processing.
    const response = await fetch('http://localhost:5000/simulate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      throw new Error(`Server responded with ${response.status}`)
    }

    // Receive response from backened in simulate()
    const data = await response.json()
    console.log('Received from backend:', data)

    // Store the result, triggering visualization update
    simulationResult.value = data
    showModal.value = true // Open modal after receiving data
  } catch (error) {
    console.error('Error submitting data:', error)
    alert('Something went wrong while contacting the server.')
  }
}
</script>

<style scoped>
.simulator-page {
  padding: 2rem 1rem;
}

.sim-form {
  max-width: 720px;
  margin: 0 auto;
  display: grid;
  gap: 1.25rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 2fr 120px;
  gap: 0.75rem;
  align-items: center;
}

.form-row label {
  font-weight: 600;
}

.form-row input[type='number'] {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid var(--color-border, #ddd);
}

::v-deep(.p-slider .p-slider-track) {
  background-color: #ddd;  /* empty track */
}

::v-deep(.p-slider .p-slider-range) {
  background-color: #ff5722; /* filled track */
}

::v-deep(.p-slider .p-slider-handle) {
  background-color: #ff5722; /* thumb */
  border-color: #ff5722;
}

/* Hover state */
::v-deep(.p-slider .p-slider-handle:hover) {
  background-color: #e64a19;  /* darker orange on hover */
  border-color: #e64a19;
}

/* Focus / active state (ring around the thumb) */
::v-deep(.p-slider .p-slider-handle:focus),
::v-deep(.p-slider .p-slider-handle:focus-visible) {
  border-color: #ff5722 !important;       /* replaces green border */
  box-shadow: 0 0 0 0.25rem rgba(255,87,34,0.5) !important; /* orange ring */
}

.value {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.form-actions {
  text-align: center;
  margin-top: 1rem;
}

.btn {
  background: orangered;
  color: white;
  border: 0;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .value {
    text-align: left;
  }
}
</style>
