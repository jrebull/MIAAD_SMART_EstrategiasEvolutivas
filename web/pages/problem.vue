<script setup lang="ts">
useHead({ title: 'Problema — EE Isotropía vs Anisotropía' })
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 py-12">
    <header class="mb-10">
      <p class="text-uacj-gold font-semibold tracking-widest uppercase text-xs">Definición del problema</p>
      <h1 class="mt-2 text-3xl md:text-4xl font-bold text-slate-900">Elipsoide Invertida mal condicionada</h1>
      <p class="mt-3 text-slate-600 max-w-3xl">
        El paisaje de búsqueda es una Gaussiana anisotrópica con ejes de curvatura creciente.
        El objetivo es maximizar <span class="font-mono">f(x)</span> sobre <span class="font-mono">ℝ¹⁰</span>.
      </p>
    </header>

    <section class="card">
      <h2 class="section-title">Función objetivo</h2>
      <div class="mt-4 flex justify-center py-4 bg-slate-50 rounded-md border border-slate-200">
        <MathEquation
          expression="f(x) \;=\; \exp\!\left(-\sum_{i=1}^{D} \frac{(x_i - 2)^2}{i}\right), \quad x \in [-5, 5]^D, \quad D = 10"
          :display-mode="true"
        />
      </div>
      <ul class="mt-4 space-y-2 text-sm text-slate-700 list-disc list-inside">
        <li>Máximo global único en <span class="font-mono">x* = (2, 2, …, 2)</span> con <span class="font-mono">f(x*) = 1</span>.</li>
        <li>La coordenada <span class="font-mono">i</span> pesa <span class="font-mono">1/i</span>: <span class="font-mono">x₁</span> es la más sensible y <span class="font-mono">x₁₀</span> la más plana.</li>
        <li>Número de condición ≈ <span class="font-mono">D = 10</span>, favoreciendo mutaciones que escalen cada eje de forma distinta.</li>
      </ul>
    </section>

    <section class="card mt-6">
      <h2 class="section-title">Las cuatro variantes</h2>
      <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="rounded-md border border-slate-200 p-4">
          <h3 class="font-semibold text-uacj-blue">(μ+λ) — Plus</h3>
          <p class="text-sm text-slate-600 mt-1">
            La siguiente generación se elige entre padres e hijos combinados: elitista, nunca empeora.
          </p>
        </div>
        <div class="rounded-md border border-slate-200 p-4">
          <h3 class="font-semibold text-uacj-blue">(μ,λ) — Comma</h3>
          <p class="text-sm text-slate-600 mt-1">
            Sólo se selecciona de entre los <span class="font-mono">λ</span> hijos. Permite escapar de óptimos locales pero puede retroceder.
          </p>
        </div>
        <div class="rounded-md border border-slate-200 p-4">
          <h3 class="font-semibold text-uacj-gold">Mutación isotrópica</h3>
          <p class="text-sm text-slate-600 mt-1">
            Un único σ compartido por todas las coordenadas. Esférica en todas las direcciones.
          </p>
        </div>
        <div class="rounded-md border border-slate-200 p-4">
          <h3 class="font-semibold text-uacj-gold">Mutación anisotrópica</h3>
          <p class="text-sm text-slate-600 mt-1">
            Un σᵢ autoadaptativo por dimensión. Ajusta la escala a la curvatura local del paisaje.
          </p>
        </div>
      </div>
    </section>

    <section class="card mt-6">
      <h2 class="section-title">Autoadaptación (regla log-normal de Schwefel)</h2>

      <div class="mt-4">
        <p class="font-medium text-slate-800">Isotrópica — <span class="font-mono">τ = 1/√(2D)</span></p>
        <div class="mt-2 flex justify-center py-3 bg-slate-50 rounded-md border border-slate-200">
          <MathEquation
            expression="\sigma' = \sigma \cdot \exp\!\big(\tau \, \mathcal{N}(0,1)\big), \qquad x' = x + \sigma' \cdot \mathcal{N}(0, I_D)"
            :display-mode="true"
          />
        </div>
      </div>

      <div class="mt-6">
        <p class="font-medium text-slate-800">
          Anisotrópica — <span class="font-mono">τ₀ = 1/√(2D)</span>, <span class="font-mono">τᵢ = 1/√(2√D)</span>
        </p>
        <div class="mt-2 flex justify-center py-3 bg-slate-50 rounded-md border border-slate-200">
          <MathEquation
            expression="\sigma_i' = \sigma_i \cdot \exp\!\big(\tau_0 \, \mathcal{N}(0,1) + \tau_i \, \mathcal{N}_i(0,1)\big), \quad x_i' = x_i + \sigma_i' \cdot \mathcal{N}_i(0,1)"
            :display-mode="true"
          />
        </div>
        <p class="mt-3 text-sm text-slate-600">
          Un ruido global común <span class="font-mono">N(0,1)</span> escala todas las dimensiones a la vez; los ruidos individuales <span class="font-mono">Nᵢ(0,1)</span> permiten ajustar cada σᵢ de forma independiente.
        </p>
      </div>
    </section>

    <section class="card mt-6">
      <h2 class="section-title">Predicción teórica</h2>
      <p class="mt-3 text-sm text-slate-700">
        Bajo autoadaptación óptima en la Elipsoide con pesos <span class="font-mono">1/i</span>, el valor estacionario de cada σ satisface aproximadamente
      </p>
      <div class="mt-3 flex justify-center py-3 bg-slate-50 rounded-md border border-slate-200">
        <MathEquation
          expression="\sigma_i^{*} \;\propto\; \sqrt{i}"
          :display-mode="true"
        />
      </div>
      <p class="mt-3 text-sm text-slate-600">
        Es decir: <span class="font-mono">σ₁₀ ≈ √10 · σ₁ ≈ 3.16 · σ₁</span>.
        Este patrón debe emerger espontáneamente de la autoadaptación en las variantes anisotrópicas.
        Véase la página <NuxtLink to="/sigma" class="text-uacj-blue underline">Evolución de σ</NuxtLink>.
      </p>
    </section>
  </div>
</template>
