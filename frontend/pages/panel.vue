<script setup lang="ts">
import { useDisplay } from 'vuetify'
import { categories } from '~/helpers/categories'
import { contentTypes } from '~/helpers/contentTypes'

definePageMeta({ middleware: ['auth'] })

const route = useRoute()
const router = useRouter()
const { mobile, mdAndUp, sm } = useDisplay()

const userStore = useUserStore()
const { user, loading: userLoading } = storeToRefs(userStore)

const summaryStore = useSummaryStore()
const { summaries, loading: summaryLoading, isEmpty } = storeToRefs(summaryStore)

const sortBy = ref<'favorites' | 'likes' | 'date' | null>(null)
const privacyStatus = ref<boolean | null | undefined>(undefined)
const contentType = ref<'text' | 'website' | 'pdf' | 'video' | null>(null)
const category = ref<string | null>(null)

const summaryAmount = 8

const sortItems = [
  { title: 'Date', value: 'date' },
  { title: 'Favorites', value: 'favorites' },
  { title: 'Likes', value: 'likes' },
]

const privacyItems = [
  { title: 'All', value: null },
  { title: 'Public', value: false },
  { title: 'Private', value: true },
]

onMounted(async () => {
  await userStore.getUser()

  if (!user.value) {
    return
  }

  const querySortBy = route.query.sortBy as 'favorites' | 'likes' | 'date' || 'favorites'
  const queryPrivacyStatus = route.query.private as 'true' | 'false' | null || null
  const queryContentType = route.query.contentType as 'text' | 'website' | 'pdf' | 'video' | null || null
  const queryCategory = route.query.category as string | null || null

  const isPrivate = queryPrivacyStatus !== null
    ? queryPrivacyStatus === 'true'
    : null

  sortBy.value = querySortBy
  privacyStatus.value = isPrivate
  contentType.value = queryContentType
  category.value = queryCategory

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, isPrivate, querySortBy, queryContentType, queryCategory)

  const newQueryParams = {
    sortBy: sortBy.value,
    private: isPrivate !== null
      ? isPrivate.toString()
      : null,
    contentType: contentType.value,
    category: category.value,
  }

  const cleanQueryParams = Object.fromEntries(
    Object.entries(newQueryParams).filter(([_, value]) => value !== null),
  )

  router.replace({ query: cleanQueryParams })
})

const cardHeight = computed(() => {
  if (mdAndUp.value) {
    return 70
  }

  if (sm.value) {
    return 60
  }

  return 35
})

function loadSummaries(
  amount: number,
  privacyStatus: boolean | null | undefined,
  sortBy: 'favorites' | 'likes' | 'date' | null,
  contentType: 'text' | 'website' | 'pdf' | 'video' | null,
  category: string | null,
) {
  if (!sortBy || privacyStatus === undefined || summaryLoading.value) {
    return
  }

  summaryStore.getSummaries({
    limit: amount,
    privateParam: privacyStatus,
    meOnly: true,
    sort: sortBy,
    contentType,
    category,
  })
}

function updateCategory(newCategory: string | null) {
  if (summaryLoading.value) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, privacyStatus.value, sortBy.value, contentType.value, newCategory)

  if (newCategory !== null) {
    router.replace({ query: { category: newCategory } })
  }
  else {
    const query = { ...route.query }
    delete query.category
    router.replace({ query })
  }
}

function updateContentType(newContentType: 'text' | 'website' | 'pdf' | 'video' | null) {
  if (summaryLoading.value) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, privacyStatus.value, sortBy.value, newContentType, category.value)

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

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, privacyStatus.value, newSortBy, contentType.value, category.value)

  if (newSortBy !== null) {
    router.replace({ query: { sortBy: newSortBy } })
  }
  else {
    const query = { ...route.query }
    delete query.sortBy
    router.replace({ query })
  }
}

function updatePrivacyStatus(newPrivacyStatus: boolean | null) {
  if (summaryLoading.value) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, newPrivacyStatus, sortBy.value, contentType.value, category.value)

  if (newPrivacyStatus !== null) {
    router.replace({ query: { private: newPrivacyStatus.toString() } })
  }
  else {
    const query = { ...route.query }
    delete query.private
    router.replace({ query })
  }
}
</script>

<template>
  <v-container style="display: flex; align-items: center; justify-content: center; height: 100%">
    <v-card
      v-if="userLoading"
      max-width="400"
    >
      <v-card-title class="text-h4">
        Loading user profile...
      </v-card-title>

      <v-card-text class="ma-2">
        <v-skeleton-loader
          type="card"
        />
      </v-card-text>
    </v-card>

    <v-card v-else>
      <v-card-title class="text-h4">
        Your panel
      </v-card-title>

      <v-card-subtitle>
        <v-row
          class="align-center my-1 flex justify-end"
          :no-gutters="mobile"
        >
          <v-col
            cols="12"
            sm="6"
            md="3"
          >
            <v-select
              v-model="category"
              :items="categories"
              label="Category"
              clearable
              @update:model-value="updateCategory"
            />
          </v-col>

          <v-col
            cols="12"
            sm="6"
            md="3"
          >
            <v-select
              v-model="contentType"
              :items="contentTypes"
              label="Content type"
              clearable
              @update:model-value="updateContentType"
            />
          </v-col>

          <v-col
            cols="12"
            sm="6"
            md="3"
          >
            <v-select
              v-model="sortBy"
              :items="sortItems"
              label="Sort by"
              @update:model-value="updateSortBy"
            />
          </v-col>

          <v-col
            cols="12"
            sm="6"
            md="3"
          >
            <v-select
              v-model="privacyStatus"
              :items="privacyItems"
              label="Privacy status"
              @update:model-value="updatePrivacyStatus"
            />
          </v-col>
        </v-row>
      </v-card-subtitle>

      <v-card-text :style="`max-height: ${cardHeight}vh; overflow-y: auto`">
        <v-row v-if="summaries.length">
          <v-col
            v-for="summary in summaries"
            :key="summary.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
            align="center"
          >
            <PanelCard :summary="summary" />
          </v-col>
        </v-row>

        <v-row v-if="summaryLoading">
          <v-col
            v-for="i in summaryAmount"
            :key="i"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-skeleton-loader
              class="mx-auto"
              max-width="400"
              height="230"
              type="card"
            />
          </v-col>
        </v-row>

        <div align="center">
          <v-btn
            :disabled="isEmpty || summaryLoading"
            class="mt-4"
            color="primary"
            @click="() => loadSummaries(summaryAmount, privacyStatus, sortBy, contentType, category)"
          >
            Load more
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>
