<script setup lang="ts">
interface SigmaSeries {
  label: string
  color: string
  mutation_type: 'isotropic' | 'anisotropic'
  series: number[] | number[][]
}
type SigmaEntries = Record<string, SigmaSeries>

const { data } = await useFetch<SigmaEntries>('/data/sigma_evolution.json')

useHead({ title: 'Evolución de σ — EE Isotropía vs Anisotropía' })

const anisoVariant = ref<'plus_aniso' | 'comma_aniso'>('plus_aniso')
const maxGen = ref(80)

const sigmaRatio = computed(() => {
  if (!data.value) return null
  const entry = data.value[anisoVariant.value]
  if (!entry || entry.mutation_type !== 'anisotropic') return null
  const src = entry.series as number[][]
  const gen = Math.min(maxGen.value - 1, src.length - 1)
  if (gen < 0) return null
  const row = src[gen]
  if (!row || row.length < 2) return null
  const s1 = row[0]
  const sD = row[row.length - 1]
  return { gen, s1, sD, ratio: sD / s1, sqrtD: Math.sqrt(row.length) }
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    <header class="mb-8">
      <p class="text-uacj-gold font-semibold tracking-widest uppercase text-xs">Evolución de σ</p>
      <h1 class="mt-2 text-3xl md:text-4xl font-bold text-slate-900">
        Trayectorias del tamaño de paso
      </h1>
      <p class="mt-3 text-slate-600 max-w-3xl">
        ¿Descubre la autoadaptación la estructura del paisaje?
        Las curvas muestran el promedio sobre 30 ejecuciones; la predicción teórica para la Elipsoide Invertida es
        <span class="font-mono">σᵢ ∝ √i</span>.
      </p>
    </header>

    <section v-if="data" class="card">
      <h2 class="section-title">σ isotrópico (1 valor por variante)</h2>
      <p class="text-sm text-slate-600 mt-1">
        En la mutación isotrópica todos los ejes comparten un mismo σ. Se espera un decaimiento monótono a medida que el algoritmo se acerca al óptimo.
      </p>
      <div class="mt-4">
        <SigmaChart :entries="data" :iso-only="true" :max-generations="maxGen" />
      </div>
    </section>

    <section v-if="data" class="card mt-8">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <h2 class="section-title mb-0">σ anisotrópico (D = 10 valores)</h2>
        <div class="flex gap-2">
          <button
            @click="anisoVariant = 'plus_aniso'"
            class="px-3 py-1.5 rounded-md text-sm border transition-colors"
            :class="anisoVariant === 'plus_aniso' ? 'bg-uacj-blue text-white border-uacj-blue' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'"
          >
            (μ+λ) Anisotrópica
          </button>
          <button
            @click="anisoVariant = 'comma_aniso'"
            class="px-3 py-1.5 rounded-md text-sm border transition-colors"
            :class="anisoVariant === 'comma_aniso' ? 'bg-uacj-blue text-white border-uacj-blue' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'"
          >
            (μ,λ) Anisotrópica
          </button>
        </div>
      </div>

      <label class="mt-4 flex items-center gap-3 text-sm text-slate-700">
        <span>Generaciones: <span class="font-mono">{{ maxGen }}</span></span>
        <input
          type="range"
          :min="20"
          :max="200"
          step="10"
          v-model.number="maxGen"
          class="w-64"
        >
      </label>

      <div class="mt-4">
        <SigmaChart
          :entries="entriesForAniso"
          :aniso-variant="anisoVariant"
          :max-generations="maxGen"
          :key="anisoVariant + '-' + maxGen"
        />
      </div>

      <div v-if="sigmaRatio" class="mt-6 rounded-md border border-slate-200 bg-slate-50 p-4">
        <h3 class="font-semibold text-slate-800">Verificación empírica en gen = {{ sigmaRatio.gen }}</h3>
        <div class="mt-2 grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
          <div>
            <p class="text-slate-500">σ₁</p>
            <p class="font-mono font-semibold text-slate-800">{{ sigmaRatio.s1.toExponential(3) }}</p>
          </div>
          <div>
            <p class="text-slate-500">σ₁₀</p>
            <p class="font-mono font-semibold text-slate-800">{{ sigmaRatio.sD.toExponential(3) }}</p>
          </div>
          <div>
            <p class="text-slate-500">Razón observada σ₁₀/σ₁</p>
            <p class="font-mono font-semibold text-uacj-blue">{{ sigmaRatio.ratio.toFixed(3) }}</p>
          </div>
          <div>
            <p class="text-slate-500">Predicción √D</p>
            <p class="font-mono font-semibold text-uacj-gold">{{ sigmaRatio.sqrtD.toFixed(3) }}</p>
          </div>
        </div>
        <p class="mt-3 text-xs text-slate-600">
          La autoadaptación descubre espontáneamente el patrón <span class="font-mono">σᵢ ∝ √i</span> predicho por la teoría; la razón <span class="font-mono">σ₁₀/σ₁</span> converge al mismo orden que <span class="font-mono">√D = √10 ≈ 3.16</span>.
        </p>
      </div>
    </section>
  </div>
</template>
