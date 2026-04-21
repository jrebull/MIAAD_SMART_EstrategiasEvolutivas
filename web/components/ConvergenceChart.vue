<script setup lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler,
  Title
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler,
  Title
)

interface ConvergenceData {
  generations: number[]
  variants: Record<string, { label: string, color: string, mean: number[], std: number[] }>
}

const props = defineProps<{
  data: ConvergenceData
  logScale?: boolean
  title?: string
}>()

const visible = ref<Record<string, boolean>>(
  Object.fromEntries(Object.keys(props.data.variants).map(k => [k, true]))
)

function hexToRgba (hex: string, alpha: number): string {
  const h = hex.replace('#', '')
  const r = parseInt(h.substring(0, 2), 16)
  const g = parseInt(h.substring(2, 4), 16)
  const b = parseInt(h.substring(4, 6), 16)
  return `rgba(${r},${g},${b},${alpha})`
}

function clipPositive (v: number): number {
  return Math.max(v, 1e-18)
}

const chartData = computed(() => {
  const datasets: any[] = []
  for (const [id, v] of Object.entries(props.data.variants)) {
    if (!visible.value[id]) continue
    const mean = props.logScale ? v.mean.map(y => clipPositive(1 - y)) : v.mean
    datasets.push({
      label: v.label,
      data: mean,
      borderColor: v.color,
      backgroundColor: hexToRgba(v.color, 0.12),
      borderWidth: 2.5,
      pointRadius: 0,
      tension: 0.1
    })
    if (!props.logScale) {
      datasets.push({
        label: v.label + ' (±1σ)',
        data: v.mean.map((m, i) => m + v.std[i]),
        borderColor: 'transparent',
        backgroundColor: hexToRgba(v.color, 0.1),
        fill: '+1',
        pointRadius: 0,
        showLine: false
      })
      datasets.push({
        label: '',
        data: v.mean.map((m, i) => m - v.std[i]),
        borderColor: 'transparent',
        backgroundColor: 'transparent',
        fill: false,
        pointRadius: 0,
        showLine: false
      })
    }
  }
  return {
    labels: props.data.generations,
    datasets
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: {
      labels: {
        filter: (item: any) => item.text && !item.text.endsWith('(±1σ)') && item.text !== ''
      }
    },
    title: props.title ? { display: true, text: props.title, font: { size: 14 } } : undefined,
    tooltip: {
      callbacks: {
        title: (items: any[]) => 'Generación ' + items[0].label,
        label: (item: any) => {
          const v = item.raw as number
          return `${item.dataset.label}: ${v.toExponential(3)}`
        }
      }
    }
  },
  scales: {
    x: {
      title: { display: true, text: 'Generación' },
      ticks: { maxTicksLimit: 10 }
    },
    y: props.logScale
      ? {
          type: 'logarithmic' as const,
          title: { display: true, text: 'Gap  1 − f(x_best)  (log)' },
          min: 1e-18
        }
      : {
          title: { display: true, text: 'Mejor fitness promedio' },
          min: 0,
          max: 1.02
        }
  }
}))

function toggle (id: string) {
  visible.value[id] = !visible.value[id]
}
</script>

<template>
  <div>
    <div class="relative h-[440px]">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    <div class="mt-3 flex flex-wrap gap-2 justify-center">
      <button
        v-for="(v, id) in data.variants"
        :key="id"
        @click="toggle(String(id))"
        class="inline-flex items-center gap-2 px-3 py-1.5 rounded-md text-sm border transition-all"
        :class="visible[String(id)]
          ? 'border-slate-300 bg-white text-slate-800 shadow-sm'
          : 'border-slate-200 bg-slate-100 text-slate-400 line-through'"
      >
        <span class="inline-block w-3 h-3 rounded-full" :style="{ backgroundColor: v.color }" />
        {{ v.label }}
      </button>
    </div>
  </div>
</template>
