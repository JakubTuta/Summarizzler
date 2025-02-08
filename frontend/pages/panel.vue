<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

onMounted(() => {
  userStore.getUser()
})
</script>

<template>
  <v-container>
    <v-card>
      {{ user }}
    </v-card>
  </v-container>
</template>
