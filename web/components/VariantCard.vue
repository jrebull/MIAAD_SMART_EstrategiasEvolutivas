<script setup lang="ts">
interface VariantSummary {
  id: string
  label: string
  color: string
  gap_mean: number
  gap_std: number
  success_rate: number
  best_fitness_mean: number
  best_fitness_max: number
  gens_to_success_mean: number
  gens_to_success_std: number
}

defineProps<{ variant: VariantSummary }>()

function fmtGap (v: number): string {
  if (v === 0) return '0.0'
  return v.toExponential(2)
}
</script>

<template>
  <div class="card border-l-4" :style="{ borderLeftColor: variant.color }">
    <h3 class="text-lg font-semibold text-slate-800">{{ variant.label }}</h3>
    <dl class="mt-3 grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
      <dt class="text-slate-500">Gap promedio</dt>
      <dd class="font-mono text-slate-800 text-right">{{ fmtGap(variant.gap_mean) }}</dd>

      <dt class="text-slate-500">Tasa de éxito</dt>
      <dd class="font-mono text-slate-800 text-right">{{ variant.success_rate.toFixed(1) }}%</dd>

      <dt class="text-slate-500">Gen → f ≥ 0.95</dt>
      <dd class="font-mono text-slate-800 text-right">
        {{ variant.gens_to_success_mean.toFixed(1) }} ± {{ variant.gens_to_success_std.toFixed(1) }}
      </dd>

      <dt class="text-slate-500">Mejor fitness prom.</dt>
      <dd class="font-mono text-slate-800 text-right">{{ variant.best_fitness_mean.toFixed(6) }}</dd>
    </dl>
  </div>
</template>
