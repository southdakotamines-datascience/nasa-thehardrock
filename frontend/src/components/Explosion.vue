<template>
  <div class="explosion-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const canvas = ref(null)
let ctx, animationFrame
let particles = []
let people = []
let startTime

function initParticles(width, height) {
  const centerX = width / 2
  const centerY = height / 2

  // Fireball particles
  for (let i = 0; i < 200; i++) {
    const angle = Math.random() * Math.PI * 2
    const speed = Math.random() * 3 + 2
    particles.push({
      x: centerX,
      y: centerY,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: 100 + Math.random() * 50,
      color: `rgba(${Math.floor(255)},${Math.floor(Math.random() * 150)},0,1)`
    })
  }

  // People particles
  for (let i = 0; i < 20; i++) {
    const angle = Math.random() * Math.PI * 2
    const speed = Math.random() * 1.5 + 1
    people.push({
      x: centerX,
      y: centerY,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - Math.random() * 1, // give some "up"
      onFire: Math.random() < 0.3,
      size: Math.random() * 8 + 5
    })
  }
}

function drawPeople(person) {
  ctx.save()
  ctx.translate(person.x, person.y)

  // Draw simple stick figure or rectangle for body
  ctx.fillStyle = '#000'
  ctx.fillRect(-person.size / 4, -person.size, person.size / 2, person.size)

  if (person.onFire) {
    ctx.fillStyle = `rgba(255, ${100 + Math.random() * 100}, 0, ${Math.random()})`
    ctx.beginPath()
    ctx.arc(0, -person.size, person.size / 2, 0, Math.PI * 2)
    ctx.fill()
  }

  ctx.restore()
}

function loop(timestamp) {
  if (!startTime) startTime = timestamp
  const elapsed = timestamp - startTime

  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  // Draw expanding fireball
  const maxRadius = 2000
  const fireballRadius = Math.min(maxRadius, (elapsed / 1000) * maxRadius)
  const grd = ctx.createRadialGradient(
    canvas.value.width / 2, canvas.value.height / 2, 0,
    canvas.value.width / 2, canvas.value.height / 2, fireballRadius
  )
  grd.addColorStop(0, 'white')
  grd.addColorStop(0.3, 'orange')
  grd.addColorStop(1, 'rgba(255, 69, 0, 0)')
  ctx.fillStyle = grd
  ctx.beginPath()
  ctx.arc(canvas.value.width / 2, canvas.value.height / 2, fireballRadius, 0, Math.PI * 2)
  ctx.fill()

  // Particles
  particles.forEach(p => {
    p.x += p.vx
    p.y += p.vy
    p.life -= 1
    ctx.fillStyle = p.color
    ctx.fillRect(p.x, p.y, 2, 2)
  })
  particles = particles.filter(p => p.life > 0)

  // People
  people.forEach(person => {
    person.x += person.vx
    person.y += person.vy
    person.vy += 0.05 // gravity
    drawPeople(person)
  })

  if (elapsed < 5000) {
    animationFrame = requestAnimationFrame(loop)
  }
}

onMounted(() => {
  const c = canvas.value
  c.width = window.innerWidth
  c.height = window.innerHeight
  ctx = c.getContext('2d')
  initParticles(c.width, c.height)
  animationFrame = requestAnimationFrame(loop)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(animationFrame)
})
</script>

<style scoped>
.explosion-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 1000vw;
  height: 1000vh;
  pointer-events: none;
  z-index: 9999;
}
canvas {
  display: block;
}
</style>
