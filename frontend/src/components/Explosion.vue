<template>
  <div ref="container" class="explosion-canvas"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { loadFull } from 'tsparticles'

const container = ref(null)
let scene, camera, renderer, sphere, animationFrameId

onMounted(() => {
  // THREE.js basic scene
  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  camera.position.z = 5

  renderer = new THREE.WebGLRenderer({ alpha: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  container.value.appendChild(renderer.domElement)

  // Shockwave sphere
  const geometry = new THREE.SphereGeometry(1, 64, 64)
  const material = new THREE.MeshBasicMaterial({
    color: 0xff5500,
    transparent: true,
    opacity: 0.5,
    wireframe: true
  })
  sphere = new THREE.Mesh(geometry, material)
  scene.add(sphere)

  const animate = () => {
    sphere.scale.x += 0.05
    sphere.scale.y += 0.05
    sphere.scale.z += 0.05
    sphere.material.opacity -= 0.01
    renderer.render(scene, camera)

    if (sphere.material.opacity > 0) {
      animationFrameId = requestAnimationFrame(animate)
    }
  }

  animate()

  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  cancelAnimationFrame(animationFrameId)
  window.removeEventListener('resize', onResize)
  renderer.dispose()
})

function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}
</script>

<style scoped>
.explosion-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
  pointer-events: none; /* click through */
}
</style>
