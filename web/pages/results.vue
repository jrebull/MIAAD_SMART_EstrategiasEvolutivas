<script setup lang="ts">
interface VariantSummary {
  id: string
  label: string
  color: string
  gap_mean: number
  gap_std: number
  success_rate: number
  best_fitness_mean: number
  best_fitness_std: number
  best_fitness_max: number
  best_fitness_min: number
  gens_to_success_mean: number
  gens_to_success_std: number
  n_runs: number
}
interface Summary {
  variants: VariantSummary[]
  hyperparameters: Record<string, any>
}

const { data } = await useFetch<Summary>('/data/summary.json')

useHead({ title: 'Resultados — EE Isotropía vs Anisotropía' })

const gapItems = computed(() =>
  (data.value?.variants ?? []).map(v => ({
    label: v.label,
    value: Math.max(v.gap_mean, 1e-20),
    color: v.color
  }))
)
const gensItems = computed(() =>
  (data.value?.variants ?? []).map(v => ({
    label: v.label,
    value: v.gens_to_success_mean,
    color: v.color,
    error: v.gens_to_success_std
  }))
)
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    <header class="mb-10">
      <p class="text-uacj-gold font-semibold tracking-widest uppercase text-xs">Resultados</p>
      <h1 class="mt-2 text-3xl md:text-4xl font-bold text-slate-900">Comparativa global de las 4 variantes</h1>
      <p class="mt-3 text-slate-600 max-w-3xl">
        Métricas agregadas sobre 30 ejecuciones independientes por variante.
        La mejor variante (por generaciones hasta el éxito) aparece resaltada en verde; la peor, en rojo.
      </p>
    </header>

    <section v-if="data">
      <ResultsTable :variants="data.variants" />
    </section>

    <section v-if="data" class="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <h2 class="section-title">Gap final (escala log)</h2>
        <p class="text-sm text-slate-600 mt-1">
          Distancia <span class="font-mono">1 − f(x_best)</span> al óptimo. Todas las variantes alcanzan gap numéricamente nulo.
        </p>
        <div class="mt-4">
          <BarChart
            :items="gapItems"
            y-label="Gap (1 − f)"
            :log-scale="true"
          />
        </div>
      </div>
      <div class="card">
        <h2 class="section-title">Generaciones hasta f ≥ 0.95</h2>
        <p class="text-sm text-slate-600 mt-1">
          Métrica discriminante: cuántas generaciones requiere cada variante para superar el umbral de éxito.
        </p>
        <div class="mt-4">
          <BarChart
            :items="gensItems"
            y-label="Generaciones"
          />
        </div>
      </div>
    </section>

    <section v-if="data" class="mt-10 card">
      <h2 class="section-title">Lectura comparativa</h2>
      <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-700">
        <div>
          <h3 class="font-semibold text-uacj-blue">Tasa de éxito</h3>
          <p class="mt-1">Las cuatro variantes alcanzan <span class="font-mono">100%</span> de éxito: el paisaje es unimodal y suficientemente suave para los 500 presupuesto generacional.</p>
        </div>
        <div>
          <h3 class="font-semibold text-uacj-blue">Velocidad</h3>
          <p class="mt-1">Las variantes isotrópicas convergen <span class="font-mono">~30-40%</span> más rápido que las anisotrópicas: con condición moderada (κ ≈ 10), adaptar D=10 sigmas individuales cuesta más de lo que rinde.</p>
        </div>
        <div>
          <h3 class="font-semibold text-uacj-blue">Selección (+) vs (,)</h3>
          <p class="mt-1">El esquema <span class="font-mono">(μ+λ)</span> es marginalmente superior en ambas familias: en un paisaje sin óptimos locales, preservar a los mejores padres acelera la convergencia.</p>
        </div>
        <div>
          <h3 class="font-semibold text-uacj-blue">Ganancia estructural</h3>
          <p class="mt-1">La mutación anisotrópica <em>sí</em> descubre el patrón <span class="font-mono">σᵢ ∝ √i</span> (ver <NuxtLink to="/sigma" class="underline text-uacj-blue">página σ</NuxtLink>), pero su beneficio se vuelve evidente en problemas de mayor condición.</p>
        </div>
      </div>
    </section>
  </div>
</template>
