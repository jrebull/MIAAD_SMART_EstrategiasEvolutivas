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
  Title
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, LogarithmicScale, PointElement, LineElement, Tooltip, Legend, Title)

interface SigmaSeries {
  label: string
  color: string
  mutation_type: 'isotropic' | 'anisotropic'
  series: number[] | number[][]
}

const props = defineProps<{
  entries: Record<string, SigmaSeries>
  isoOnly?: boolean
  anisoVariant?: string
  title?: string
  maxGenerations?: number
}>()

function viridis (t: number): string {
  const stops = [
    [68, 1, 84],      // 0.0 púrpura
    [59, 82, 139],    // 0.25 azul
    [33, 145, 140],   // 0.5 verde azulado
    [94, 201, 98],    // 0.75 verde claro
    [253, 231, 37]    // 1.0 amarillo
  ]
  const idx = Math.min(Math.floor(t * (stops.length - 1)), stops.length - 2)
  const frac = (t * (stops.length - 1)) - idx
  const a = stops[idx]
  const b = stops[idx + 1]
  const r = Math.round(a[0] + (b[0] - a[0]) * frac)
  const g = Math.round(a[1] + (b[1] - a[1]) * frac)
  const bl = Math.round(a[2] + (b[2] - a[2]) * frac)
  return `rgb(${r},${g},${bl})`
}

const chartData = computed(() => {
  const datasets: any[] = []
  if (props.isoOnly) {
    for (const [id, entry] of Object.entries(props.entries)) {
      if (entry.mutation_type !== 'isotropic') continue
      const data = (entry.series as number[]).map(v => Math.max(v, 1e-10))
      const sliced = props.maxGenerations ? data.slice(0, props.maxGenerations) : data
      datasets.push({
        label: entry.label,
        data: sliced,
        borderColor: entry.color,
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.1
      })
    }
  } else {
    const vid = props.anisoVariant ?? 'plus_aniso'
    const entry = props.entries[vid]
    if (entry && entry.mutation_type === 'anisotropic') {
      const series2d = entry.series as number[][]
      const sliced = props.maxGenerations ? series2d.slice(0, props.maxGenerations) : series2d
      const D = sliced[0].length
      for (let i = 0; i < D; i++) {
        datasets.push({
          label: `σ_${i + 1}`,
          data: sliced.map(row => Math.max(row[i], 1e-10)),
          borderColor: viridis(i / (D - 1)),
          borderWidth: 1.8,
          pointRadius: 0,
          tension: 0.1
        })
      }
    }
  }

  const firstEntry = Object.values(props.entries)[0]
  const rawLen = Array.isArray((firstEntry?.series as any)[0])
    ? (firstEntry?.series as number[][]).length
    : (firstEntry?.series as number[]).length
  const len = props.maxGenerations ? Math.min(props.maxGenerations, rawLen) : rawLen
  const labels = Array.from({ length: len }, (_, i) => String(i))
  return { labels, datasets }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: { position: 'right' as const, labels: { boxWidth: 12 } },
    title: props.title ? { display: true, text: props.title } : undefined,
    tooltip: {
      callbacks: {
        title: (items: any[]) => 'Generación ' + items[0].label,
        label: (item: any) => `${item.dataset.label}: ${(item.raw as number).toExponential(3)}`
      }
    }
  },
  scales: {
    x: { title: { display: true, text: 'Generación' }, ticks: { maxTicksLimit: 10 } },
    y: {
      type: 'logarithmic' as const,
      title: { display: true, text: 'σ  (escala log)' }
    }
  }
}))
</script>

<template>
  <div class="relative h-[440px]">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>
