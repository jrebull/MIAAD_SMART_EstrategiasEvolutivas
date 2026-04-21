<script setup lang="ts">
import katex from 'katex'

const props = defineProps<{
  expression: string
  displayMode?: boolean
}>()

const rendered = computed(() =>
  katex.renderToString(props.expression, {
    throwOnError: false,
    displayMode: props.displayMode ?? false,
    strict: 'ignore'
  })
)
</script>

<template>
  <div v-if="displayMode" class="katex-display" v-html="rendered" />
  <span v-else v-html="rendered" />
</template>
