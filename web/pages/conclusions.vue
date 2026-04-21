<script setup lang="ts">
useHead({ title: 'Conclusiones — EE Isotropía vs Anisotropía' })

const profileSrc = ref('/javiprofile.jpg')
const profileLoaded = ref(true)
function onProfileError () { profileLoaded.value = false }
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 py-12">
    <header class="mb-10">
      <p class="text-uacj-gold font-semibold tracking-widest uppercase text-xs">Conclusiones</p>
      <h1 class="mt-2 text-3xl md:text-4xl font-bold text-slate-900">
        Lecciones del estudio comparativo
      </h1>
      <p class="mt-3 text-slate-600 max-w-3xl">
        Síntesis de hallazgos del experimento y reflexión sobre su aplicación al dominio profesional del autor.
      </p>
    </header>

    <section class="card">
      <h2 class="section-title">Hallazgos principales</h2>
      <ol class="mt-4 space-y-4 text-slate-700">
        <li>
          <p class="font-semibold text-uacj-blue">1 · Todas las variantes resuelven el problema.</p>
          <p class="text-sm mt-1">
            Con <span class="font-mono">(μ=20, λ=100, 500 gen)</span>, las cuatro combinaciones alcanzan <span class="font-mono">f = 1</span> en el 100% de las 30 ejecuciones. La tasa de éxito y el gap final no son métricas discriminantes en este paisaje unimodal.
          </p>
        </li>
        <li>
          <p class="font-semibold text-uacj-blue">2 · Isotrópica es más rápida con condición moderada.</p>
          <p class="text-sm mt-1">
            Las variantes isotrópicas alcanzan <span class="font-mono">f ≥ 0.95</span> en <span class="font-mono">~22-24</span> generaciones, frente a <span class="font-mono">~32-39</span> para las anisotrópicas. Con κ ≈ 10, el costo de autoadaptar D=10 sigmas supera su beneficio.
          </p>
        </li>
        <li>
          <p class="font-semibold text-uacj-blue">3 · (μ+λ) converge un poco más rápido que (μ,λ).</p>
          <p class="text-sm mt-1">
            En un paisaje sin óptimos locales, el elitismo del esquema plus acelera ligeramente la convergencia. La ventaja de (μ,λ) —escapar de mínimos locales— no es relevante aquí.
          </p>
        </li>
        <li>
          <p class="font-semibold text-uacj-blue">4 · La anisotropía aprende la geometría del problema.</p>
          <p class="text-sm mt-1">
            A pesar de ser más lenta, la mutación anisotrópica <em>redescubre</em> el patrón predicho por la teoría <span class="font-mono">σᵢ ∝ √i</span>. La razón empírica <span class="font-mono">σ₁₀/σ₁</span> se acerca a <span class="font-mono">√D ≈ 3.16</span> conforme la adaptación se estabiliza, validando el ejercicio teórico de la unidad.
          </p>
        </li>
      </ol>
    </section>

    <section class="card mt-6">
      <h2 class="section-title">Cuándo usar cada mutación</h2>
      <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="rounded-md border border-slate-200 p-4">
          <h3 class="font-semibold text-uacj-blue">Isotrópica</h3>
          <ul class="mt-2 text-sm text-slate-700 list-disc list-inside space-y-1">
            <li>Problemas con condición numérica baja (κ cercana a 1).</li>
            <li>Presupuesto generacional limitado.</li>
            <li>Paisajes bien escalados o pre-normalizados.</li>
          </ul>
        </div>
        <div class="rounded-md border border-slate-200 p-4">
          <h3 class="font-semibold text-uacj-gold">Anisotrópica</h3>
          <ul class="mt-2 text-sm text-slate-700 list-disc list-inside space-y-1">
            <li>Paisajes con ejes de sensibilidad heterogéneos (κ ≫ 1).</li>
            <li>Cuando se tolera un mayor costo computacional inicial.</li>
            <li>Como precursor de estrategias con matriz de covarianza completa (CMA-ES).</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="card mt-6">
      <h2 class="section-title">Aplicación al dominio profesional</h2>
      <div class="mt-4 grid grid-cols-1 md:grid-cols-[auto_1fr] gap-6 items-start">
        <img
          v-if="profileLoaded"
          :src="profileSrc"
          alt="Javier Rebull"
          class="rounded-lg shadow w-40 h-40 object-cover mx-auto md:mx-0"
          @error="onProfileError"
        >
        <div
          v-else
          class="rounded-lg w-40 h-40 bg-slate-200 flex items-center justify-center text-slate-500 text-xs text-center mx-auto md:mx-0 px-2"
        >
          Coloca <span class="font-mono">javiprofile.jpg</span> en <span class="font-mono">web/public/</span>
        </div>
        <div class="text-sm text-slate-700 leading-relaxed">
          <p>
            En el entorno bancario (<strong>Banco Santander</strong>), los problemas de optimización rara vez son unimodales: la calibración de modelos de riesgo, la asignación de cuotas comerciales o el balanceo de portafolios involucran decenas de variables con sensibilidades muy distintas —exactamente el escenario donde la <em>anisotropía</em> empieza a pagar su costo adicional.
          </p>
          <p class="mt-3">
            La lección práctica de esta unidad es que la elección entre isotropía y anisotropía no es una preferencia estética sino una decisión <em>informada por la geometría</em> del problema. Antes de elegir un operador, conviene estudiar el condicionamiento del paisaje o, al menos, realizar un diagnóstico inicial con σ compartido para luego decidir si vale la pena pagar D grados de libertad adicionales.
          </p>
          <p class="mt-3">
            Hacia adelante, las EE con matriz de covarianza completa (CMA-ES) extienden esta idea capturando correlaciones entre variables —el siguiente paso natural cuando los ejes del problema no están alineados con los del sistema de coordenadas.
          </p>
        </div>
      </div>
    </section>

    <section class="card mt-6 bg-slate-50">
      <h2 class="section-title">Créditos</h2>
      <dl class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2 text-sm">
        <dt class="text-slate-500">Autor</dt>
        <dd class="font-semibold text-slate-800">Javier Augusto Rebull Saucedo</dd>
        <dt class="text-slate-500">Matrícula</dt>
        <dd class="font-mono text-slate-800">263483</dd>
        <dt class="text-slate-500">Programa</dt>
        <dd class="text-slate-800">MIAAD · UACJ</dd>
        <dt class="text-slate-500">Materia</dt>
        <dd class="text-slate-800">Optimización Inteligente</dd>
        <dt class="text-slate-500">Repositorio</dt>
        <dd class="text-slate-800">
          <a href="https://github.com/jrebull/MIAAD_SMART_EstrategiasEvolutivas" target="_blank" rel="noopener" class="text-uacj-blue underline">
            github.com/jrebull/MIAAD_SMART_EstrategiasEvolutivas
          </a>
        </dd>
      </dl>
    </section>
  </div>
</template>
