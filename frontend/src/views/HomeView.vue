<template>
  <div ref="container" class="earth-container"></div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

const container = ref(null);

onMounted(() => {
  // Scene
  const scene = new THREE.Scene();

  // Camera
  const camera = new THREE.PerspectiveCamera(
    75,
    container.value.clientWidth / container.value.clientHeight,
    0.1,
    1000
  );
  camera.position.z = 3;

  // Renderer (transparent background)
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(container.value.clientWidth, container.value.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  container.value.appendChild(renderer.domElement);

  // Orbit Controls (mouse drag/zoom)
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enablePan = false;
  controls.minDistance = 2;
  controls.maxDistance = 6;

  // Earth geometry
  const earthGeometry = new THREE.SphereGeometry(1, 64, 64);

  // Load textures
  const textureLoader = new THREE.TextureLoader();
  const earthTexture = textureLoader.load(
    "https://threejs.org/examples/textures/land_ocean_ice_cloud_2048.jpg"
  );
  const bumpMap = textureLoader.load(
    "https://threejs.org/examples/textures/earthbump1k.jpg"
  );
  const specularMap = textureLoader.load(
    "https://threejs.org/examples/textures/earthspec1k.jpg"
  );

  // Earth material
  const earthMaterial = new THREE.MeshPhongMaterial({
    map: earthTexture,
    bumpMap: bumpMap,
    bumpScale: 0.05,
    specularMap: specularMap,
    specular: new THREE.Color("grey"),
  });

  const earth = new THREE.Mesh(earthGeometry, earthMaterial);
  scene.add(earth);

  // Cloud layer
  const cloudGeometry = new THREE.SphereGeometry(1.01, 64, 64);
  const cloudTexture = textureLoader.load(
    "https://threejs.org/examples/textures/earthcloudmaptrans.jpg"
  );
  const cloudMaterial = new THREE.MeshPhongMaterial({
    map: cloudTexture,
    transparent: true,
    opacity: 0.2, // softer, less solid
    depthWrite: false,
  });
  const clouds = new THREE.Mesh(cloudGeometry, cloudMaterial);
  scene.add(clouds);

  // Lighting (make it less bright / more natural)
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.15); // softer ambient
  scene.add(ambientLight);

  const sunLight = new THREE.DirectionalLight(0xffffff, 0.9); // toned down
  sunLight.position.set(5, 2, 5);
  scene.add(sunLight);

  // Animate
  function animate() {
    requestAnimationFrame(animate);
    controls.update(); // needed for OrbitControls
    earth.rotation.y += 0.0015; // slow auto-rotation
    clouds.rotation.y += 0.0021; 
    renderer.render(scene, camera);
  }
  animate();

  // Handle window resize
  window.addEventListener("resize", () => {
    camera.aspect = container.value.clientWidth / container.value.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.value.clientWidth, container.value.clientHeight);
  });
});
</script>

<style scoped>
.earth-container {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: transparent; /* fully transparent */
}
</style>
