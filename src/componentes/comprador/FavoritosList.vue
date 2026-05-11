<template>
  <section class="space-y-5">
    <div>
      <p class="text-sm font-medium text-agro-green">Productos Favoritos</p>
      <h2 class="text-2xl font-bold text-gray-900">Tus productos guardados</h2>
    </div>

    <div v-if="favoritos.length" class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      <article v-for="favorito in favoritos" :key="favorito.id" class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
        <img :src="favorito.producto?.imagen" :alt="favorito.producto?.nombre" class="h-44 w-full object-cover" />
        <div class="p-4">
          <h3 class="font-bold text-gray-900">{{ favorito.producto?.nombre }}</h3>
          <p class="mt-1 text-sm text-gray-500">{{ favorito.producto?.productor }} · {{ favorito.producto?.region }}</p>
          <p class="mt-3 text-lg font-bold text-agro-green">${{ favorito.producto?.precio }}/qq</p>
          <div class="mt-3 flex flex-wrap gap-2">
            <span v-for="cert in favorito.producto?.certificaciones" :key="cert" class="rounded-full bg-green-50 px-2 py-1 text-xs text-green-700">{{ cert }}</span>
          </div>
          <div class="mt-4 flex gap-3">
            <router-link :to="`/producto/${favorito.productoId}`" class="flex-1 rounded-lg bg-agro-green px-3 py-2 text-center text-sm font-semibold text-white">Hacer pedido</router-link>
            <button class="rounded-lg border border-gray-300 px-3 py-2 text-sm font-semibold text-gray-700" @click="removeFavorito(favorito.id)">Quitar</button>
          </div>
        </div>
      </article>
    </div>

    <div v-else class="rounded-lg border border-dashed border-gray-300 bg-white p-8 text-center">
      <p class="text-gray-600">Aún no tienes productos favoritos. Explora el catálogo y guarda tus productos preferidos.</p>
      <router-link to="/catalogo" class="mt-4 inline-block rounded-lg bg-agro-green px-4 py-2 text-sm font-semibold text-white">Ir al catálogo</router-link>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '../../stores/authStore'
import { useFavoritoStore } from '../../stores/favoritoStore'

const { currentUser } = useAuthStore()
const { favoritos, loadFavoritos, removeFavorito } = useFavoritoStore()

onMounted(() => {
  if (currentUser.value) loadFavoritos(currentUser.value.id)
})
</script>
