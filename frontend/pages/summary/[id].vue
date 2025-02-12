<script setup lang="ts">
import DOMPurify from 'dompurify'
import { useDisplay } from 'vuetify'
import type { ISummary } from '~/models/summary'

const route = useRoute()
const { mobile } = useDisplay()

const summaryStore = useSummaryStore()

const summaryId = ref<string | null>(null)
const summary = ref<ISummary | null>(null)
const isAuthError = ref(false)

const contentItems = [
  { title: 'Text', value: 'text' },
  { title: 'Website', value: 'website' },
  { title: 'PDF', value: 'pdf' },
  { title: 'Video', value: 'video' },
]

onMounted(async () => {
  const paramsData = route.params as { id: string }
  summaryId.value = paramsData.id

  try {
    summary.value = await summaryStore.getSummaryById(paramsData.id)
  }
  catch (error: any) {
    if (error.message === 'Unauthorized') {
      isAuthError.value = true
    }
  }
})

function getChipColor(contentType: string) {
  switch (contentType) {
    case 'text':
      return 'secondary'
    case 'website':
      return 'success'
    case 'pdf':
      return 'warning'
    case 'video':
      return 'primary'
  }
}

function formatTime(time: string) {
  const date = new Date(time)

  const day = date.getDate()
  const month = date.getMonth() + 1
  const year = date.getFullYear()
  const hours = date.getHours()
  const minutes = date.getMinutes()

  return `${day}.${month}.${year} ${hours}:${minutes}`
}
</script>

<!-- eslint-disable vue/no-v-html -->
<template>
  <v-container>
    <v-card v-if="isAuthError">
      <v-card-title>
        Unauthorized
      </v-card-title>

      <v-card-text>
        You are not authorized to view this summary.
      </v-card-text>
    </v-card>

    <v-card v-else-if="summary">
      <v-card-title class="text-h5">
        {{ summary.title }}
      </v-card-title>

      <v-card-subtitle v-if="summary.author?.username && summary.createdAt">
        {{ `By: ${summary.author.username} at ${formatTime(summary.createdAt)}` }}
      </v-card-subtitle>

      <v-card-text class="ma-2">
        <v-row class="text-subtitle-1">
          <v-col
            cols="12"
            md="6"
            :order="mobile
              ? 2
              : 1"
          >
            <v-col cols="12">
              Content type:
              <v-chip
                class="ml-2"
                :color="getChipColor(summary.contentType)"
              >
                {{ contentItems.find((item) => item.value === summary!.contentType)?.title || '' }}
              </v-chip>
            </v-col>

            <v-col cols="12">
              Tags:
              <v-chip
                v-for="tag in summary.tags"
                :key="tag"
                color="primary"
                class="my-2 ml-2"
              >
                {{ tag }}
              </v-chip>
            </v-col>
          </v-col>

          <v-col
            cols="12"
            md="6"
            :order="mobile
              ? 1
              : 2"
          >
            <v-col cols="12">
              User prompt: {{ summary.userPrompt }}
            </v-col>

            <v-col
              v-if="summary.contentType === 'website' && summary.url"
              cols="12"
            >
              Original:
              <NuxtLink
                :to="summary.url"
                external
              >
                {{ summary.url }}
              </NuxtLink>
            </v-col>
          </v-col>
        </v-row>

        <div class="text-h5 mb-6 mt-12">
          Summary
        </div>

        <div
          class="text-body-1"
          style="white-space: pre-wrap"
          v-html="DOMPurify.sanitize(summary.summary)"
        />
      </v-card-text>
    </v-card>
  </v-container>
</template>
