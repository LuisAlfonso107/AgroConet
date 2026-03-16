<template>
  <div class="min-h-screen bg-crema pt-20 px-4">
    <div class="max-w-md mx-auto py-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Registro</h1>
      <form @submit.prevent="handleRegister" class="bg-white p-6 rounded-xl shadow-md">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Nombre completo</label>
          <input type="text" class="w-full px-4 py-2 border rounded-lg" />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Email</label>
          <input type="email" class="w-full px-4 py-2 border rounded-lg" />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Tipo de usuario</label>
          <select class="w-full px-4 py-2 border rounded-lg">
            <option value="comprador">Comprador</option>
            <option value="productor">Productor</option>
            <option value="agencia">Agencia Exportadora</option>
          </select>
        </div>
        <button type="submit" class="w-full bg-agro-green text-white py-3 rounded-lg font-semibold hover:bg-agro-green-light">
          Registrarse
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
const handleRegister = () => {
  alert('Registro functionality coming soon!')
}
</script>

<style scoped>
.bg-crema {
  background-color: #FFF8E1;
}
</style>
