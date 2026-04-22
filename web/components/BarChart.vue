<script setup lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  BarElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, LogarithmicScale, BarElement, Tooltip, Legend, Title)

interface Item { label: string, value: number, color: string, error?: number }

const props = defineProps<{
  items: Item[]
  yLabel: string
  logScale?: boolean
  valueFormatter?: (v: number) => string
  title?: string
}>()

const defaultFmt = (v: number) => (Math.abs(v) >= 1 || v === 0 ? v.toFixed(2) : v.toExponential(2))

const tickFmt = (v: number) => {
  if (v === 0) return '0'
  const abs = Math.abs(v)
  if (abs >= 0.01 && abs < 10000) return Number(v.toPrecision(3)).toString()
  const exp = Math.floor(Math.log10(abs))
  const mantissa = v / Math.pow(10, exp)
  const mStr = Math.abs(mantissa - 1) < 1e-9 ? '10' : `${Number(mantissa.toPrecision(2))}·10`
  const supers: Record<string, string> = { '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' }
  const expStr = String(exp).split('').map(c => supers[c] ?? c).join('')
  return `${mStr}${expStr}`
}

const chartData = computed(() => ({
  labels: props.items.map(i => i.label),
  datasets: [
    {
      label: props.yLabel,
      data: props.items.map(i => (props.logScale ? Math.max(i.value, 1e-20) : i.value)),
      backgroundColor: props.items.map(i => i.color + 'cc'),
      borderColor: props.items.map(i => i.color),
      borderWidth: 1.5,
      errorBars: props.items.map(i => ({ plus: i.error ?? 0, minus: i.error ?? 0 }))
    }
  ]
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    title: props.title ? { display: true, text: props.title } : undefined,
    tooltip: {
      callbacks: {
        label: (item: any) => {
          const fmt = props.valueFormatter ?? defaultFmt
          return `${props.yLabel}: ${fmt(props.items[item.dataIndex].value)}`
        }
      }
    }
  },
  scales: {
    y: props.logScale
      ? {
          type: 'logarithmic' as const,
          title: { display: true, text: props.yLabel },
          ticks: {
            callback: (v: number | string) => tickFmt(Number(v)),
            maxTicksLimit: 8
          }
        }
      : {
          title: { display: true, text: props.yLabel },
          beginAtZero: true,
          ticks: { callback: (v: number | string) => tickFmt(Number(v)) }
        }
  }
}))
</script>

<template>
  <div class="relative h-[400px]">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>
