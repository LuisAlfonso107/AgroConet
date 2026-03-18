<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20">
    <!-- Hero Section -->
    <section class="relative overflow-hidden py-12 sm:py-16 text-center bg-gradient-to-b from-agro-green/5 to-transparent">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 transition-all duration-1000"
           :class="mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white tracking-tight mb-4">
          Contacto – <span class="text-transparent bg-clip-text bg-gradient-to-r from-agro-green to-agro-green-light">Estamos aquí para ayudarte</span>
        </h1>
        <p class="mt-4 text-xl text-gray-600 dark:text-gray-300 mb-8">
          ¿Dudas? ¿Problemas? ¿Ideas? Escríbenos y te respondemos en menos de 24 horas.
        </p>
        <a href="#formulario" class="inline-block px-8 py-3 text-lg font-bold rounded-xl text-white bg-gradient-to-r from-agro-green to-agro-naranja hover:shadow-lg hover:scale-105 transition-all duration-200">
          Enviar mensaje
        </a>
      </div>
    </section>

    <!-- Main Content: Grid -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 pb-24">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        
        <!-- Contact Info Cards -->
        <div class="space-y-6 transition-all duration-1000 delay-100"
             :class="mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">
          
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Información de Contacto</h2>
          
          <!-- WhatsApp Card -->
          <a href="https://wa.me/50499887766" target="_blank" rel="noopener noreferrer" 
             class="flex items-center p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:-translate-y-1 transition-all group">
            <div class="flex-shrink-0 w-14 h-14 bg-green-100 text-green-600 rounded-2xl flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              <span aria-hidden="true">💬</span>
            </div>
            <div class="ml-4">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white group-hover:text-green-600 transition-colors">WhatsApp Directo</h3>
              <p class="text-gray-500 dark:text-gray-400">Chatea con nosotros ahora</p>
            </div>
          </a>

          <!-- Email Card -->
          <a href="mailto:soporte@agroconet.hn" 
             class="flex items-center p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:-translate-y-1 transition-all group">
            <div class="flex-shrink-0 w-14 h-14 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              <span aria-hidden="true">✉️</span>
            </div>
            <div class="ml-4">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white group-hover:text-blue-600 transition-colors">Correo Electrónico</h3>
              <p class="text-gray-500 dark:text-gray-400">soporte@agroconet.hn</p>
            </div>
          </a>

          <!-- Location & Hours Box -->
          <div class="p-6 bg-gradient-to-br from-agro-green/5 to-transparent rounded-2xl border border-agro-green/20">
            <div class="mb-4">
              <h4 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <span aria-hidden="true">📍</span> Ubicación
              </h4>
              <p class="text-gray-600 dark:text-gray-300 mt-1">Basados en San Pedro Sula, Honduras – conectando a toda Centroamérica.</p>
            </div>
            <div>
              <h4 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <span aria-hidden="true">⏱️</span> Horario de Atención
              </h4>
              <p class="text-gray-600 dark:text-gray-300 mt-1">Lunes a Viernes 8:00 AM – 5:00 PM</p>
            </div>
          </div>

          <!-- Social Media -->
          <div class="pt-4">
            <h4 class="font-bold text-gray-500 dark:text-gray-400 mb-3 uppercase text-sm tracking-wider">Síguenos</h4>
            <div class="flex gap-4">
              <a href="#" class="w-12 h-12 rounded-full bg-white dark:bg-gray-800 shadow-sm flex items-center justify-center text-gray-600 hover:text-agro-green hover:scale-110 transition-all">FB</a>
              <a href="#" class="w-12 h-12 rounded-full bg-white dark:bg-gray-800 shadow-sm flex items-center justify-center text-gray-600 hover:text-agro-green hover:scale-110 transition-all">IG</a>
              <a href="#" class="w-12 h-12 rounded-full bg-white dark:bg-gray-800 shadow-sm flex items-center justify-center text-gray-600 hover:text-agro-green hover:scale-110 transition-all">X</a>
            </div>
          </div>
        </div>

        <!-- Contact Form -->
        <div id="formulario" class="relative transition-all duration-1000 delay-200"
             :class="mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">
          
          <div class="bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-lg border border-gray-100 dark:border-gray-700">
            <div v-if="successMsg" class="mb-6 p-4 rounded-xl bg-green-50 text-green-800 flex items-start gap-4 animate-fade-in">
              <span class="text-2xl mt-1">✅</span>
              <div>
                <h4 class="font-bold text-lg">¡Mensaje enviado!</h4>
                <p>Te responderemos pronto. Gracias por contactarnos.</p>
              </div>
            </div>

            <div v-else-if="errorMsg" class="mb-6 p-4 rounded-xl bg-red-50 text-red-800 flex items-center justify-between animate-shake">
              <p>Hubo un problema, intenta de nuevo o contáctanos por WhatsApp.</p>
              <button @click="errorMsg = false" class="text-red-600 font-bold hover:text-red-900 px-2">X</button>
            </div>

            <form @submit.prevent="submitForm" class="space-y-6" novalidate>
              
              <!-- Nombre -->
              <div>
                <label for="nombre" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Nombre completo *</label>
                <div class="relative">
                  <input type="text" id="nombre" v-model="form.nombre" @blur="touched.nombre = true"
                         class="w-full px-4 py-3 rounded-xl border focus:ring-2 focus:outline-none transition-colors"
                         :class="(touched.nombre && !isNombreValid) ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 dark:border-gray-600 focus:border-agro-green focus:ring-agro-green/20 dark:bg-gray-700 dark:text-white'"
                         placeholder="Ej: Juan Pérez">
                  <span v-if="touched.nombre && isNombreValid" class="absolute right-4 top-3 text-green-500 font-bold text-xl">✓</span>
                </div>
                <p v-if="touched.nombre && !isNombreValid" class="mt-1 text-sm text-red-500">El nombre es requerido y debe tener al menos 3 caracteres.</p>
              </div>

              <!-- Email and WhatsApp (2 cols on desktop) -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <!-- Email -->
                <div>
                  <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Correo electrónico *</label>
                  <div class="relative">
                    <input type="email" id="email" v-model="form.email" @blur="touched.email = true"
                           class="w-full px-4 py-3 rounded-xl border focus:ring-2 focus:outline-none transition-colors"
                           :class="(touched.email && !isEmailValid) ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 dark:border-gray-600 focus:border-agro-green focus:ring-agro-green/20 dark:bg-gray-700 dark:text-white'"
                           placeholder="tu@correo.com">
                    <span v-if="touched.email && isEmailValid" class="absolute right-4 top-3 text-green-500 font-bold text-xl">✓</span>
                  </div>
                  <p v-if="touched.email && !isEmailValid" class="mt-1 text-sm text-red-500">Ingresa un correo válido.</p>
                </div>
                
                <!-- WhatsApp / Teléfono -->
                <div>
                  <label for="telefono" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Teléfono / WhatsApp *</label>
                  <div class="relative">
                    <input type="tel" id="telefono" v-model="form.telefono" @blur="touched.telefono = true"
                           class="w-full px-4 py-3 rounded-xl border focus:ring-2 focus:outline-none transition-colors"
                           :class="(touched.telefono && !isTelefonoValid) ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 dark:border-gray-600 focus:border-agro-green focus:ring-agro-green/20 dark:bg-gray-700 dark:text-white'"
                           placeholder="+504...">
                    <span v-if="touched.telefono && isTelefonoValid" class="absolute right-4 top-3 text-green-500 font-bold text-xl">✓</span>
                  </div>
                  <p v-if="touched.telefono && !isTelefonoValid" class="mt-1 text-sm text-red-500">Asegúrate de incluir tu código de país.</p>
                </div>
              </div>

              <!-- Asunto -->
              <div>
                <label for="asunto" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Asunto *</label>
                <select id="asunto" v-model="form.asunto" @blur="touched.asunto = true"
                        class="w-full px-4 py-3 rounded-xl border focus:ring-2 focus:outline-none transition-colors appearance-none"
                        :class="(touched.asunto && !isAsuntoValid) ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 dark:border-gray-600 focus:border-agro-green focus:ring-agro-green/20 dark:bg-gray-700 dark:text-white'">
                  <option value="" disabled>Selecciona el motivo</option>
                  <option value="Consulta general">Consulta general</option>
                  <option value="Problema técnico">Problema técnico</option>
                  <option value="Quiero ser productor">Quiero ser productor</option>
                  <option value="Soy comprador">Soy comprador</option>
                  <option value="Colaboración">Colaboración</option>
                  <option value="Otro">Otro</option>
                </select>
                <p v-if="touched.asunto && !isAsuntoValid" class="mt-1 text-sm text-red-500">Selecciona un asunto.</p>
              </div>

              <!-- Mensaje -->
              <div>
                <label for="mensaje" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Mensaje *</label>
                <div class="relative">
                  <textarea id="mensaje" v-model="form.mensaje" @blur="touched.mensaje = true" rows="4"
                            class="w-full px-4 py-3 rounded-xl border focus:ring-2 focus:outline-none transition-colors resize-y"
                            :class="(touched.mensaje && !isMensajeValid) ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 dark:border-gray-600 focus:border-agro-green focus:ring-agro-green/20 dark:bg-gray-700 dark:text-white'"
                            placeholder="Describe cómo podemos ayudarte..."></textarea>
                </div>
                <div class="flex justify-between mt-1">
                  <p v-if="touched.mensaje && !isMensajeValid" class="text-sm text-red-500">El mensaje debe tener al menos 10 caracteres.</p>
                  <p v-else class="text-sm text-gray-500"></p>
                  <span class="text-xs text-gray-400 font-mono">{{ form.mensaje.length }} / 500</span>
                </div>
              </div>

              <!-- Checkbox -->
              <div class="flex items-start mt-2">
                <div class="flex items-center h-5">
                  <input id="politicas" type="checkbox" v-model="form.politicas" @change="touched.politicas = true"
                         class="w-5 h-5 text-agro-green border-gray-300 rounded focus:ring-agro-green cursor-pointer">
                </div>
                <label for="politicas" class="ml-3 text-sm text-gray-600 dark:text-gray-400 cursor-pointer">
                  Acepto la <a href="#" class="text-agro-green font-bold hover:underline">política de privacidad</a> *
                </label>
              </div>
              <p v-if="touched.politicas && !isPoliticasValid" class="mt-1 text-sm text-red-500">Debes aceptar las políticas para continuar.</p>

              <!-- Botón Submit -->
              <button type="submit" 
                      :disabled="!isFormValid || isLoading"
                      class="w-full py-4 px-6 text-white text-lg font-bold rounded-xl shadow-md transition-all duration-300 relative overflow-hidden"
                      :class="{'bg-gray-400 cursor-not-allowed': !isFormValid, 'bg-gradient-to-r from-agro-green to-agro-green-light hover:shadow-lg hover:scale-[1.02]': isFormValid && !isLoading, 'opacity-90 cursor-wait': isLoading}">
                
                <span v-if="!isLoading">Enviar mensaje</span>
                
                <div v-else class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Enviando...</span>
                </div>
              </button>
            </form>
          </div>
        </div>

      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'

const mounted = ref(false)

const isLoading = ref(false)
const successMsg = ref(false)
const errorMsg = ref(false)

const form = reactive({
  nombre: '',
  email: '',
  telefono: '',
  asunto: '',
  mensaje: '',
  politicas: false
})

const touched = reactive({
  nombre: false,
  email: false,
  telefono: false,
  asunto: false,
  mensaje: false,
  politicas: false
})

// Validate Functions / Computed
const isNombreValid = computed(() => form.nombre.trim().length >= 3)
const isEmailValid = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email))
const isTelefonoValid = computed(() => /^\+?[0-9\s\-()]{8,15}$/.test(form.telefono))
const isAsuntoValid = computed(() => form.asunto !== '')
const isMensajeValid = computed(() => form.mensaje.trim().length >= 10)
const isPoliticasValid = computed(() => form.politicas)

const isFormValid = computed(() => {
  return isNombreValid.value && 
         isEmailValid.value && 
         isTelefonoValid.value && 
         isAsuntoValid.value && 
         isMensajeValid.value && 
         isPoliticasValid.value
})

const marcarTodosTocados = () => {
  touched.nombre = true
  touched.email = true
  touched.telefono = true
  touched.asunto = true
  touched.mensaje = true
  touched.politicas = true
}

const submitForm = async () => {
  errorMsg.value = false
  successMsg.value = false
  marcarTodosTocados()

  if (!isFormValid.value) return

  isLoading.value = true

  // Simulate APi call
  try {
    await new Promise((resolve) => {
      setTimeout(() => {
        // Random chance function (e.g. 5% chance of error simulation, disabled generally).
        // Let's keep it robust and resolve manually.
        resolve('OK')
      }, 2000)
    })

    successMsg.value = true
    console.log("Formulario enviado con éxito", form)
    
    // Opcional reset
    setTimeout(() => {
      // router.push('/catalogo')
    }, 4000)

  } catch (err) {
    errorMsg.value = true
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  mounted.value = true
})
</script>

<style scoped>
html { scroll-behavior: smooth; }

@keyframes fade-in {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.4s ease-out forwards;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  50% { transform: translateX(5px); }
  75% { transform: translateX(-5px); }
}
.animate-shake {
  animation: shake 0.4s ease-in-out;
}
</style>
