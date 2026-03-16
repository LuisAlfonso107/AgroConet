<template>
  <div class="min-h-screen bg-crema pt-20 px-4">
    <div class="max-w-7xl mx-auto py-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-8">Catálogo de Productos</h1>
      <div class="grid md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div 
          v-for="i in 8" 
          :key="i"
          class="bg-white rounded-xl shadow-md overflow-hidden"
        >
          <div class="h-48 bg-gray-200">
            <img 
              src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&q=80" 
              alt="Producto"
              class="w-full h-full object-cover"
              loading="lazy"
            />
          </div>
          <div class="p-4">
            <h3 class="font-bold text-gray-800 mb-1">Producto {{ i }}</h3>
            <p class="text-sm text-gray-500 mb-2">Región</p>
            <span class="text-lg font-bold text-agro-green">${{ 100 + i * 10 }}/qq</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bg-crema {
  background-color: #FFF8E1;
}
</style>
