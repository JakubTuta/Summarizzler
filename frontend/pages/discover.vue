<script setup lang="ts">
import { useDisplay } from 'vuetify'
import { categories, getCategory, getCategoryColor } from '~/helpers/categories'
import { contentTypes, getContentType, getContentTypeColor } from '~/helpers/contentTypes'

const route = useRoute()
const router = useRouter()
const { mobile, smAndUp } = useDisplay()

const summaryStore = useSummaryStore()
const { discoveredSummaries: summaries, loading: summaryLoading, isEmpty } = storeToRefs(summaryStore)

const sortBy = ref<'favorites' | 'likes' | 'date' | null>(null)
const contentType = ref<'text' | 'website' | 'file' | 'video' | null>(null)
const category = ref<string | null>(null)

const summaryAmount = 5

const sortItems = [
  { title: 'Date', value: 'date' },
  { title: 'Favorites', value: 'favorites' },
  { title: 'Likes', value: 'likes' },
]

onMounted(() => {
  const querySortBy = route.query.sortBy as 'favorites' | 'likes' | 'date' || 'favorites'
  const queryContentType = route.query.contentType as 'text' | 'website' | 'file' | 'video' | null || null
  const queryCategory = route.query.category as string | null || null

  sortBy.value = querySortBy
  contentType.value = queryContentType
  category.value = queryCategory

  loadSummaries(summaryAmount, querySortBy, queryContentType, queryCategory)

  const newQueryParams = {
    sortBy: sortBy.value,
    contentType: contentType.value,
    category: category.value,
  }

  const cleanQueryParams = Object.fromEntries(
    Object.entries(newQueryParams).filter(([_, value]) => value !== null),
  )

  router.replace({ query: cleanQueryParams })
})

const cardHeight = computed(() => {
  if (smAndUp.value) {
    return 70
  }

  return 55
})

function loadSummaries(
  amount: number,
  sortBy: 'favorites' | 'likes' | 'date' | null,
  contentType: 'text' | 'website' | 'file' | 'video' | null,
  category: string | null,
) {
  if (!sortBy || summaryLoading.value) {
    return
  }

  summaryStore.getDiscoverySummaries({
    limit: amount,
    sort: sortBy,
    contentType,
    category,
  })
}

function updateCategory(newCategory: string | null) {
  if (summaryLoading.value) {
    return
  }

  loadSummaries(summaryAmount, sortBy.value, contentType.value, newCategory)

  if (newCategory !== null) {
    router.replace({ query: { category: newCategory } })
  }
  else {
    const query = { ...route.query }
    delete query.category
    router.replace({ query })
  }
}

function updateContentType(newContentType: 'text' | 'website' | 'file' | 'video' | null) {
  if (summaryLoading.value) {
    return
  }

  loadSummaries(summaryAmount, sortBy.value, newContentType, category.value)

  if (newContentType !== null) {
    router.replace({ query: { contentType: newContentType } })
  }
  else {
    const query = { ...route.query }
    delete query.contentType
    router.replace({ query })
  }
}

function updateSortBy(newSortBy: 'favorites' | 'likes' | 'date' | null) {
  if (summaryLoading.value) {
    return
  }

  loadSummaries(summaryAmount, newSortBy, contentType.value, category.value)

  if (newSortBy !== null) {
    router.replace({ query: { sortBy: newSortBy } })
  }
  else {
    const query = { ...route.query }
    delete query.sortBy
    router.replace({ query })
  }
}

function formatTime(date: Date) {
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear().toString().padStart(4, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')

  return `${day}.${month}.${year} ${hours}:${minutes}`
}
</script>

<template>
  <v-container style="display: flex; align-items: center; justify-content: center; height: 100%">
    <v-card>
      <v-card-title class="text-h4">
        Discover
      </v-card-title>

      <v-card-subtitle>
        <v-row
          :no-gutters="mobile"
          class="align-center my-1 flex justify-end"
        >
          <v-col
            cols="12"
            sm="4"
            md="3"
          >
            <v-select
              v-model="category"
              :items="categories"
              label="Category"
              @update:model-value="updateCategory"
            />
          </v-col>

          <v-col
            cols="12"
            sm="4"
            md="3"
          >
            <v-select
              v-model="contentType"
              :items="contentTypes"
              label="Content type"
              @update:model-value="updateContentType"
            />
          </v-col>

          <v-col
            cols="12"
            sm="4"
            md="3"
          >
            <v-select
              v-model="sortBy"
              :items="sortItems"
              label="Sort by"
              @update:model-value="updateSortBy"
            />
          </v-col>
        </v-row>
      </v-card-subtitle>

      <v-card-text :style="`max-height: ${cardHeight}vh; overflow-y: auto`">
        <v-list>
          <v-list-item
            v-for="summary in summaries"
            :key="summary.id"
            lines="three"
            class="my-3"
            :to="`/summary/${summary.id}`"
          >
            <v-list-item-title class="text-h6 align-center justify-space-between flex">
              <span style="white-space: pre-wrap;">
                {{ summary.title }}
              </span>

              <div>
                <v-chip
                  v-if="summary.category"
                  :color="getCategoryColor(summary.category)"
                  class="mr-2"
                >
                  {{ getCategory(summary.category)?.title || '' }}
                </v-chip>

                <v-chip
                  v-if="summary.contentType"
                  :color="getContentTypeColor(summary.contentType)"
                >
                  {{ getContentType(summary.contentType)?.title || '' }}
                </v-chip>
              </div>
            </v-list-item-title>

            <v-list-item-subtitle>
              {{ `${summary.author?.username || ''} - ${formatTime(summary.createdAt)}` }}
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
              max-width="80%"
              type="list-item-three-line"
            />
          </v-list-item>
        </v-list>

        <v-btn
          :disabled="isEmpty || summaryLoading"
          class="mx-auto"
          color="primary"
          @click="loadSummaries(summaryAmount, sortBy, contentType, category)"
        >
          Load more
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>
