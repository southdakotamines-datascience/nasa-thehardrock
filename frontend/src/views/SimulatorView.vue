<template>
  <section class="page simulator-page">
    <div class="wrapper">
      <h1>Simulator</h1>

      <!-- Visualization Dialog: only shows when both showModal & simulationResult are set -->
      <Dialog
        v-model:visible="showModal"
        modal
        header="Impact Visualization"
        :style="{ width: '700px', maxWidth: '90vw' }"
      >
        <Visualization v-if="simulationResult" :result="simulationResult" />
      </Dialog>

      <form class="sim-form" @submit.prevent="handleSubmit">
        <div class="form-row">
          <label for="diameter">Diameter (m)</label>
          <input
            id="diameter"
            type="number"
            v-model.number="diameter"
            :min="diameterMin"
            :max="diameterMax"
            :step="diameterStep"
            required
          />
          <input
            class="slider"
            type="range"
            v-model.number="diameter"
            :min="diameterMin"
            :max="diameterMax"
            :step="diameterStep"
            aria-label="Diameter slider"
          />
          <div class="value">{{ diameter }}</div>
        </div>

        <div class="form-row">
          <label for="velocity">Velocity (km/s)</label>
          <input
            id="velocity"
            type="number"
            v-model.number="velocity"
            :min="velocityMin"
            :max="velocityMax"
            :step="velocityStep"
            required
          />
          <input
            class="slider"
            type="range"
            v-model.number="velocity"
            :min="velocityMin"
            :max="velocityMax"
            :step="velocityStep"
            aria-label="Velocity slider"
          />
          <div class="value">{{ velocity }}</div>
        </div>

        <div class="form-row">
          <label for="mass">Mass (kg)</label>
          <input
            id="mass"
            type="number"
            v-model.number="mass"
            :min="massMin"
            :max="massMax"
            :step="massStep"
            required
          />
          <input
            class="slider"
            type="range"
            v-model.number="mass"
            :min="massMin"
            :max="massMax"
            :step="massStep"
            aria-label="Mass slider"
          />
          <div class="value">{{ formatMass }}</div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn">Submit</button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import Dialog from 'primevue/dialog'

// Visualization. 
const showModal = ref(false)
import Visualization from '../components/Visualization.vue'
const simulationResult = ref(null)


// Assumptions for ranges of sliders; change as needed
const diameterMin = 0.1
const diameterMax = 1000
const diameterStep = 0.1

const velocityMin = 0
const velocityMax = 72
const velocityStep = 0.1

const massMin = 0.001
const massMax = 1e9
const massStep = 1

const diameter = ref(10)
const velocity = ref(20)
const mass = ref(1000)

// const formatMass = computed(() => {
//   if (mass.value >= 1e6) return (mass.value / 1e6).toFixed(2) + // 'M'
//   if (mass.value >= 1e3) return (mass.value / 1e3).toFixed(2) + // 'k'
//   return mass.value
// })

async function handleSubmit() {
  // Basic validation
  if (diameter.value <= 0 || velocity.value < 0 || mass.value <= 0) {
    alert('Please enter positive values for diameter, velocity and mass.')
    return
  }

  const payload = {
    diameter: diameter.value,
    velocity: velocity.value,
    mass: mass.value,
  }

  try {
    // Send payload to flask, listening at localhost.../simulate for processing.
    const response = await fetch('http://localhost:5000/simulate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    // debugger
    if (!response.ok) {
      throw new Error(`Server responded with ${response.status}`)
    }

    // Receive response from backened in simulate()
    const data = await response.json()
    console.log('Received from backend:', data)

    // Store the result, triggering visualization update
    simulationResult.value = data
    showModal.value = true   // Open modal after receiving data

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

.slider {
  width: 100%;
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
