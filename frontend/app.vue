<script setup lang="ts">
const authStore = useAuthStore()

onMounted(() => {
  authStore.init()
})
</script>

<template>
  <NuxtLayout>
    <v-app>
      <v-main>
        <AppBar />

        <NuxtPage />
      </v-main>
    </v-app>
  </NuxtLayout>
</template>
