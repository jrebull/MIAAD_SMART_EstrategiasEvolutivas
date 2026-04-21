<script setup lang="ts">
const nav = [
  { to: '/',            label: 'Inicio'       },
  { to: '/problem',     label: 'Problema'     },
  { to: '/results',     label: 'Resultados'   },
  { to: '/convergence', label: 'Convergencia' },
  { to: '/sigma',       label: 'σ anisotrópica' },
  { to: '/conclusions', label: 'Conclusiones' }
]

const mobileOpen = ref(false)
</script>

<template>
  <header class="bg-uacj-blue text-white sticky top-0 z-40 shadow-md">
    <div class="container mx-auto px-4 py-3 flex items-center justify-between">
      <NuxtLink to="/" class="flex flex-col leading-tight text-white hover:text-white">
        <span class="text-xs uppercase tracking-wider opacity-80">MIAAD · UACJ</span>
        <span class="font-bold text-lg">EE: Isotropía vs Anisotropía</span>
      </NuxtLink>

      <button
        class="md:hidden text-white focus:outline-none"
        @click="mobileOpen = !mobileOpen"
        aria-label="Abrir menú"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <nav class="hidden md:flex items-center gap-1 text-sm">
        <NuxtLink
          v-for="item in nav"
          :key="item.to"
          :to="item.to"
          class="px-3 py-2 rounded-md text-white/90 hover:text-white hover:bg-white/10 transition-colors"
          active-class="bg-white/15 text-white font-semibold"
        >
          {{ item.label }}
        </NuxtLink>
      </nav>
    </div>

    <nav v-if="mobileOpen" class="md:hidden bg-uacj-blue/95 border-t border-white/10">
      <NuxtLink
        v-for="item in nav"
        :key="item.to"
        :to="item.to"
        class="block px-4 py-3 text-white/90 hover:bg-white/10 text-sm"
        active-class="bg-white/15 text-white font-semibold"
        @click="mobileOpen = false"
      >
        {{ item.label }}
      </NuxtLink>
    </nav>
  </header>
</template>
