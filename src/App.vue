<template>
  <div id="app">
    <Navbar v-if="!isDashboardRoute" />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './componentes/Navbar.vue'

const route = useRoute()
const isDashboardRoute = computed(() => route.path.startsWith('/dashboard'))
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>
