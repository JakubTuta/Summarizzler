<script setup lang="ts">
import { useDisplay } from 'vuetify'

definePageMeta({ middleware: ['auth'] })

const { mobile } = useDisplay()
const router = useRouter()

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

onMounted(async () => {
  if (user.value)
    return

  await userStore.getUser()

  if (!user.value)
    router.push('/login')
})

const selectedTab = ref('website')

const tabs = [
  {
    title: 'Website',
    value: 'website',
  },
  {
    title: 'Text',
    value: 'text',
  },
  {
    title: 'File',
    value: 'file',
  },
  {
    title: 'Video',
    value: 'video',
  },
]
</script>

<template>
  <v-container>
    <v-tabs
      v-model="selectedTab"
      color="secondary"
      class="mb-4"
      grow
    >
      <v-tab
        v-for="tab in tabs"
        :key="tab.value"
        :value="tab.value"
      >
        {{ tab.title }}
      </v-tab>
    </v-tabs>

    <CreateWebsite v-if="selectedTab === 'website'" />

    <CreateText v-else-if="selectedTab === 'text'" />

    <CreateFile v-else-if="selectedTab === 'file' && !mobile" />

    <CreateVideo v-else-if="selectedTab === 'video'" />
  </v-container>
</template>
