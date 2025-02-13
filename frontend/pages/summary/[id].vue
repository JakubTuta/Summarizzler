<script setup lang="ts">
import DOMPurify from 'dompurify'
import { useDisplay } from 'vuetify'
import { getCategory, getCategoryColor } from '~/helpers/categories'
import { getContentType, getContentTypeColor } from '~/helpers/contentTypes'
import type { ISummary } from '~/models/summary'

const route = useRoute()
const { mobile } = useDisplay()

const summaryStore = useSummaryStore()

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const summaryId = ref<string | null>(null)
const summary = ref<ISummary | null>(null)
const isAuthError = ref(false)

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

function formatTime(date: Date) {
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear().toString().padStart(4, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')

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
      <v-card-title class="text-h4">
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
            <v-col
              v-if="summary.contentType"
              cols="12"
            >
              <span class="font-weight-bold">
                Content type:
              </span>

              <v-chip
                class="ml-2"
                :color="getContentTypeColor(summary.contentType)"
              >
                {{ getContentType(summary.contentType)?.title || '' }}
              </v-chip>
            </v-col>

            <v-col
              v-if="summary.category"
              cols="12"
            >
              <span class="font-weight-bold">
                Category:
              </span>

              <v-chip
                :color="getCategoryColor(summary.category)"
                class="my-2 ml-2"
              >
                {{ getCategory(summary.category)?.title || '' }}
              </v-chip>
            </v-col>

            <v-col
              v-if="summary.tags?.length"
              cols="12"
            >
              <span class="font-weight-bold">
                Tags:
              </span>

              <v-chip
                v-for="tag in summary.tags"
                :key="tag"
                color="secondary"
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
              <span class="font-weight-bold">
                User prompt:
              </span>
              {{ summary.userPrompt }}
            </v-col>

            <v-col
              v-if="summary.contentType === 'website' && summary.url"
              cols="12"
            >
              <span class="font-weight-bold">
                Original:
              </span>

              <NuxtLink
                :to="summary.url"
                external
              >
                {{ summary.url }}
              </NuxtLink>
            </v-col>

            <v-col cols="12">
              <v-btn
                variant="flat"
                rounded="circle"
                icon
                size="large"
              >
                <v-tooltip
                  location="bottom"
                  activator="parent"
                >
                  {{ user
                    ? 'Soon...'
                    : 'Login to favorite' }}
                </v-tooltip>

                <v-icon
                  color="yellow"
                  class="mr-2"
                >
                  mdi-star
                </v-icon>
                {{ summary.favorites }}
              </v-btn>

              <v-btn
                variant="flat"
                rounded="circle"
                icon
                size="large"
                class="mx-10"
              >
                <v-tooltip
                  location="bottom"
                  activator="parent"
                >
                  {{ user
                    ? 'Soon...'
                    : 'Login to like' }}
                </v-tooltip>

                <v-icon
                  color="success"
                  class="mr-2"
                >
                  mdi-thumb-up
                </v-icon>
                {{ summary.likes }}
              </v-btn>

              <v-btn
                variant="flat"
                rounded="circle"
                icon
                size="large"
              >
                <v-tooltip
                  location="bottom"
                  activator="parent"
                >
                  {{ user
                    ? 'Soon...'
                    : 'Login to dislike' }}
                </v-tooltip>

                <v-icon
                  color="error"
                  class="mr-2"
                >
                  mdi-thumb-up
                </v-icon>
                {{ summary.dislikes }}
              </v-btn>
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
