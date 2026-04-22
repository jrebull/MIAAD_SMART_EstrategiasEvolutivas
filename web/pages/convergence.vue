<script setup lang="ts">
interface ConvergenceData {
  generations: number[]
  variants: Record<string, { label: string, color: string, mean: number[], std: number[] }>
}

const { data } = await useFetch<ConvergenceData>('/data/convergence.json', { server: false })

const logScale = ref(false)
const maxGen = ref(120)

useHead({ title: 'Convergencia — EE Isotropía vs Anisotropía' })

const slicedData = computed<ConvergenceData | null>(() => {
  if (!data.value) return null
  const n = Math.min(maxGen.value, data.value.generations.length)
  const gens = data.value.generations.slice(0, n)
  const variants: ConvergenceData['variants'] = {}
  for (const [id, v] of Object.entries(data.value.variants)) {
    variants[id] = {
      label: v.label,
      color: v.color,
      mean: v.mean.slice(0, n),
      std: v.std.slice(0, n)
    }
  }
  return { generations: gens, variants }
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    <header class="mb-8">
      <p class="text-uacj-gold font-semibold tracking-widest uppercase text-xs">Convergencia</p>
      <h1 class="mt-2 text-3xl md:text-4xl font-bold text-slate-900">Gráfica de convergencia interactiva</h1>
      <p class="mt-3 text-slate-600 max-w-3xl">
        Promedio del mejor fitness a lo largo de las generaciones, sobre 30 ejecuciones.
        En escala lineal se muestra la banda <span class="font-mono">±1σ</span>; en escala logarítmica, la cantidad graficada es el gap <span class="font-mono">1 − f</span>.
      </p>
    </header>

    <div class="card">
      <div class="flex flex-wrap gap-4 items-center justify-between mb-4">
        <div class="flex gap-2">
          <button
            @click="logScale = false"
            class="px-3 py-1.5 rounded-md text-sm border transition-colors"
            :class="!logScale ? 'bg-uacj-blue text-white border-uacj-blue' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'"
          >
            Escala lineal
          </button>
          <button
            @click="logScale = true"
            class="px-3 py-1.5 rounded-md text-sm border transition-colors"
            :class="logScale ? 'bg-uacj-blue text-white border-uacj-blue' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'"
          >
            Gap (log)
          </button>
        </div>
        <label class="flex items-center gap-3 text-sm text-slate-700">
          <span>Generaciones: <span class="font-mono">{{ maxGen }}</span></span>
          <input
            type="range"
            :min="20"
            :max="500"
            step="10"
            v-model.number="maxGen"
            class="w-48"
          >
        </label>
      </div>

      <ClientOnly>
        <ConvergenceChart
          v-if="slicedData"
          :data="slicedData"
          :log-scale="logScale"
          :key="logScale ? 'log' : 'lin'"
        />
        <div v-else class="h-[440px] flex items-center justify-center text-slate-400 text-sm">
          Cargando datos de convergencia…
        </div>
        <template #fallback>
          <div class="h-[440px] flex items-center justify-center text-slate-400 text-sm">
            Cargando datos de convergencia…
          </div>
        </template>
      </ClientOnly>
    </div>

    <section class="card mt-6">
      <h2 class="section-title">Cómo leer esta gráfica</h2>
      <ul class="mt-3 list-disc list-inside text-sm text-slate-700 space-y-1">
        <li>En <strong>escala lineal</strong>, las cuatro curvas saturan rápidamente en <span class="font-mono">f ≈ 1</span>; distinguirlas requiere acercarse al inicio con el slider.</li>
        <li>En <strong>escala logarítmica del gap</strong>, se observa el decaimiento exponencial característico de las EE con autoadaptación — una recta en log es tasa de convergencia constante.</li>
        <li>Activa/desactiva variantes con los botones bajo la gráfica para comparar pares de interés (p. ej. plus vs comma dentro de la misma familia).</li>
      </ul>
    </section>
  </div>
</template>
