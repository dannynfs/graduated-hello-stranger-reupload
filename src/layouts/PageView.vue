<template>
  <n-notification-provider>
    <n-message-provider>
      <n-scrollbar x-scrollable style="max-height: 100vh;">
        <div style="background-color: #F8F4E7;">
          <router-view v-if="isRouterActive" />
        </div>
      </n-scrollbar>
    </n-message-provider>
  </n-notification-provider>
</template>
<script setup>

import { ref, provide, nextTick } from 'vue'
const isRouterActive = ref(true)
provide('reload', () => {
  isRouterActive.value = false
  nextTick(() => {
    isRouterActive.value = true
  })
})

</script>