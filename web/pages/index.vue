<script setup lang="ts">
interface Summary {
  variants: Array<{
    id: string
    label: string
    color: string
    gap_mean: number
    success_rate: number
    gens_to_success_mean: number
    gens_to_success_std: number
    best_fitness_mean: number
    best_fitness_max: number
    best_fitness_min: number
    gap_std: number
    best_fitness_std: number
  }>
  hyperparameters: {
    mu: number
    lambda: number
    generations: number
    dimension: number
    bounds: [number, number]
    n_runs: number
    success_threshold: number
    sigma_init: number
  }
}

const { data } = await useFetch<Summary>('/data/summary.json')

useHead({
  title: 'EE: Isotropía vs Anisotropía — MIAAD UACJ'
})
</script>

<template>
  <div>
    <section class="bg-gradient-to-br from-uacj-blue to-slate-900 text-white">
      <div class="max-w-6xl mx-auto px-4 py-20 lg:py-28">
        <p class="text-uacj-gold font-semibold tracking-widest uppercase text-sm">
          MIAAD · Optimización Inteligente · UACJ
        </p>
        <h1 class="mt-3 text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
          Estrategias Evolutivas:<br>
          <span class="text-uacj-gold">Isotropía vs Anisotropía</span>
        </h1>
        <p class="mt-6 text-lg md:text-xl text-slate-200 max-w-3xl">
          Estudio comparativo de cuatro variantes de Estrategias Evolutivas
          <span class="font-mono">(μ+λ)</span> y <span class="font-mono">(μ,λ)</span>
          con mutación isotrópica y anisotrópica sobre la función Elipsoide Invertida en <span class="font-mono">ℝ¹⁰</span>.
        </p>
        <div class="mt-8 flex flex-wrap gap-3">
          <NuxtLink to="/results" class="btn-uacj">Ver resultados</NuxtLink>
          <NuxtLink to="/problem" class="btn-outline">Definición del problema</NuxtLink>
        </div>
      </div>
    </section>

    <section class="max-w-6xl mx-auto px-4 py-14">
      <h2 class="section-title text-center">Resumen de las 4 variantes evaluadas</h2>
      <p class="text-center text-slate-600 mt-2 max-w-2xl mx-auto">
        30 ejecuciones independientes por variante; 120 corridas en total.
        Cada variante combina un esquema de selección con un tipo de mutación.
      </p>
      <div v-if="data" class="mt-8 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <VariantCard
          v-for="v in data.variants"
          :key="v.id"
          :variant="v"
        />
      </div>
    </section>

    <section class="bg-slate-100 border-y border-slate-200">
      <div class="max-w-6xl mx-auto px-4 py-14">
        <h2 class="section-title text-center">Hiperparámetros del experimento</h2>
        <div v-if="data" class="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="card text-center">
            <p class="text-slate-500 text-sm">Padres (μ)</p>
            <p class="text-3xl font-bold text-uacj-blue mt-1">{{ data.hyperparameters.mu }}</p>
          </div>
          <div class="card text-center">
            <p class="text-slate-500 text-sm">Hijos (λ)</p>
            <p class="text-3xl font-bold text-uacj-blue mt-1">{{ data.hyperparameters.lambda }}</p>
          </div>
          <div class="card text-center">
            <p class="text-slate-500 text-sm">Generaciones</p>
            <p class="text-3xl font-bold text-uacj-blue mt-1">{{ data.hyperparameters.generations }}</p>
          </div>
          <div class="card text-center">
            <p class="text-slate-500 text-sm">Dimensión</p>
            <p class="text-3xl font-bold text-uacj-blue mt-1">{{ data.hyperparameters.dimension }}</p>
          </div>
          <div class="card text-center">
            <p class="text-slate-500 text-sm">Ejecuciones</p>
            <p class="text-3xl font-bold text-uacj-blue mt-1">{{ data.hyperparameters.n_runs }}</p>
          </div>
          <div class="card text-center">
            <p class="text-slate-500 text-sm">Umbral éxito</p>
            <p class="text-3xl font-bold text-uacj-blue mt-1">f ≥ {{ data.hyperparameters.success_threshold }}</p>
          </div>
          <div class="card text-center">
            <p class="text-slate-500 text-sm">σ inicial</p>
            <p class="text-3xl font-bold text-uacj-blue mt-1">{{ data.hyperparameters.sigma_init.toFixed(1) }}</p>
          </div>
          <div class="card text-center">
            <p class="text-slate-500 text-sm">Dominio</p>
            <p class="text-2xl font-bold text-uacj-blue mt-2">[{{ data.hyperparameters.bounds[0] }}, {{ data.hyperparameters.bounds[1] }}]<sup>D</sup></p>
          </div>
        </div>
      </div>
    </section>

    <section class="max-w-6xl mx-auto px-4 py-14">
      <h2 class="section-title text-center">Recorrido sugerido</h2>
      <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <NuxtLink to="/problem" class="card hover:shadow-md transition-shadow group">
          <h3 class="font-semibold text-lg text-uacj-blue group-hover:underline">1 · Problema</h3>
          <p class="mt-2 text-slate-600 text-sm">Formulación matemática de la Elipsoide Invertida y fundamentos de EE con autoadaptación.</p>
        </NuxtLink>
        <NuxtLink to="/convergence" class="card hover:shadow-md transition-shadow group">
          <h3 class="font-semibold text-lg text-uacj-blue group-hover:underline">2 · Convergencia</h3>
          <p class="mt-2 text-slate-600 text-sm">Curvas de convergencia interactivas en escala lineal y logarítmica.</p>
        </NuxtLink>
        <NuxtLink to="/sigma" class="card hover:shadow-md transition-shadow group">
          <h3 class="font-semibold text-lg text-uacj-blue group-hover:underline">3 · Evolución de σ</h3>
          <p class="mt-2 text-slate-600 text-sm">Trayectoria de los tamaños de paso y verificación empírica de la predicción teórica σᵢ ∝ √i.</p>
        </NuxtLink>
      </div>
    </section>
  </div>
</template>
