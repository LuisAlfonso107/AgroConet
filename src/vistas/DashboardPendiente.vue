<template>
  <div class="min-h-screen bg-gray-50 px-4 py-20">
    <div class="mx-auto max-w-2xl rounded-lg border border-gray-200 bg-white p-8 text-center shadow-sm">
      <p class="text-sm font-semibold text-agro-green">AgroConet</p>
      <h1 class="mt-2 text-3xl font-bold text-gray-900">Panel en preparación</h1>
      <p class="mt-3 text-gray-600">
        El panel de {{ roleLabel }} todavía no está implementado. Tu sesión está activa y esta ruta existe para respetar la redirección por rol.
      </p>
      <router-link to="/catalogo" class="mt-6 inline-block rounded-lg bg-agro-green px-4 py-2 text-sm font-semibold text-white">
        Ir al catálogo
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const roleLabel = computed(() => route.path.includes('agencia') ? 'agencia' : 'productor')
</script>
