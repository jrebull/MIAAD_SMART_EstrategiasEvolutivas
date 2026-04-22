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

const props = defineProps<{ variants: VariantSummary[] }>()

function fmtGap (v: number): string {
  if (v === 0) return '0'
  return v.toExponential(2)
}

const bestVariant = computed(() => {
  return [...props.variants].sort((a, b) => a.gens_to_success_mean - b.gens_to_success_mean)[0]
})
const worstVariant = computed(() => {
  return [...props.variants].sort((a, b) => b.gens_to_success_mean - a.gens_to_success_mean)[0]
})
</script>

<template>
  <div class="overflow-x-auto rounded-lg border border-slate-200 shadow-sm">
    <table class="table-uacj">
      <thead>
        <tr>
          <th>Variante</th>
          <th class="text-right">Gap (media ± σ)</th>
          <th class="text-right">Éxito (%)</th>
          <th class="text-right">Gen → f ≥ 0.95</th>
          <th class="text-right">Mejor fitness prom.</th>
          <th class="text-right">Mejor fitness máx.</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="v in variants"
          :key="v.id"
          :class="{
            'bg-green-50': v.id === bestVariant?.id,
            'bg-red-50':   v.id === worstVariant?.id
          }"
        >
          <td class="font-semibold flex items-center gap-2">
            <span class="inline-block w-3 h-3 rounded-full" :style="{ backgroundColor: v.color }" />
            {{ v.label }}
          </td>
          <td class="text-right font-mono">{{ fmtGap(v.gap_mean) }} ± {{ fmtGap(v.gap_std) }}</td>
          <td class="text-right font-mono">{{ v.success_rate.toFixed(1) }}</td>
          <td class="text-right font-mono">
            {{ v.gens_to_success_mean.toFixed(2) }} ± {{ v.gens_to_success_std.toFixed(2) }}
          </td>
          <td class="text-right font-mono">{{ v.best_fitness_mean.toFixed(6) }}</td>
          <td class="text-right font-mono">{{ v.best_fitness_max.toFixed(6) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
