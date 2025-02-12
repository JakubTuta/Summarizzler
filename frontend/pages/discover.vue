<script setup lang="ts">
import { useDisplay } from 'vuetify'

const route = useRoute()
const router = useRouter()
const { mobile } = useDisplay()

const summaryStore = useSummaryStore()
const { summaries, loading: summaryLoading, isEmpty } = storeToRefs(summaryStore)

const sortBy = ref<'favorites' | 'likes' | 'date' | null>(null)
const contentType = ref<'text' | 'website' | 'pdf' | 'video' | null>(null)

const summaryAmount = 5

const sortItems = [
  { title: 'Date', value: 'date' },
  { title: 'Favorites', value: 'favorites' },
  { title: 'Likes', value: 'likes' },
]

const contentItems = [
  { title: 'Text', value: 'text' },
  { title: 'Website', value: 'website' },
  { title: 'PDF', value: 'pdf' },
  { title: 'Video', value: 'video' },
]

onMounted(() => {
  const querySortBy = route.query.sortBy as 'favorites' | 'likes' | 'date' || 'date'
  const queryContentType = route.query.contentType as 'text' | 'website' | 'pdf' | 'video' || null

  sortBy.value = querySortBy
  contentType.value = queryContentType

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, querySortBy, queryContentType)
  router.replace({ query: { sortBy: sortBy.value, contentType: contentType.value } })
})

watch(sortBy, (newValue, oldValue) => {
  if (!newValue || oldValue === null || summaryLoading.value) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, newValue, contentType.value)
  router.replace({ query: { sortBy: newValue } })
})

watch(contentType, (newValue, oldValue) => {
  if (!newValue || oldValue === null || summaryLoading.value) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, sortBy.value, newValue)
  router.replace({ query: { contentType: newValue } })
})

function loadSummaries(amount: number, sortBy: 'favorites' | 'likes' | 'date' | null, contentType: 'text' | 'website' | 'pdf' | 'video' | null) {
  if (!sortBy || summaryLoading.value) {
    return
  }

  summaryStore.getSummaries(amount, 'false', false, sortBy, contentType)
}

function getChipColor(contentType: string) {
  switch (contentType) {
    case 'text':
      return 'secondary'
    case 'website':
      return 'success'
    case 'pdf':
      return 'warning'
    case 'video':
      return 'error'
    default:
      return 'grey'
  }
}
</script>

<template>
  <v-container style="display: flex; align-items: center; justify-content: center; height: 100%">
    <v-card>
      <v-card-title class="text-h5">
        Discover
      </v-card-title>

      <v-card-subtitle>
        <v-row
          class="align-center my-1 flex justify-end"
        >
          <v-col
            cols="12"
            md="3"
          >
            <v-select
              v-model="contentType"
              :items="contentItems"
              label="Content type"
            />
          </v-col>

          <v-col
            cols="12"
            md="3"
          >
            <v-select
              v-model="sortBy"
              :items="sortItems"
              label="Sort by"
            />
          </v-col>
        </v-row>
      </v-card-subtitle>

      <v-card-text
        :style="`max-height: ${mobile
          ? 55
          : 70}vh; overflow-y: auto`"
      >
        <v-list>
          <v-list-item
            v-for="summary in summaries"
            :key="summary.id"
            lines="three"
            class="my-3"
            :to="`/summary/${summary.id}`"
          >
            <v-list-item-title class="text-h6 align-center justify-space-between flex">
              <span>
                {{ summary.title }}
              </span>

              <v-chip :color="getChipColor(summary.contentType)">
                {{ contentItems.find((item) => item.value === summary.contentType)?.title || '' }}
              </v-chip>
            </v-list-item-title>

            <v-list-item-subtitle>
              {{ `${summary.author?.username || ''} - ${summary.userPrompt}` }}
            </v-list-item-subtitle>

            <div class="mt-4">
              {{ summary.summary.substring(0, 200) }}
            </div>
          </v-list-item>
        </v-list>

        <v-list v-if="summaryLoading">
          <v-list-item
            v-for="i in summaryAmount"
            :key="i"
            class="my-3"
          >
            <v-skeleton-loader
              class="mx-auto"
              max-width="80%"
              type="list-item-three-line"
            />
          </v-list-item>
        </v-list>

        <v-btn
          :disabled="isEmpty || summaryLoading"
          class="mx-auto"
          color="primary"
          @click="loadSummaries(summaryAmount, sortBy, contentType)"
        >
          Load more
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>
