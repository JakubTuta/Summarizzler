<script setup lang="ts">
import { useDisplay } from 'vuetify'

definePageMeta({ middleware: ['auth'] })

const route = useRoute()
const router = useRouter()
const { mobile } = useDisplay()

const userStore = useUserStore()
const { user, loading: userLoading } = storeToRefs(userStore)

const summaryStore = useSummaryStore()
const { summaries, loading: summaryLoading, isEmpty } = storeToRefs(summaryStore)

const sortBy = ref<'favorites' | 'likes' | 'date' | null>(null)
const privacyStatus = ref<'true' | 'false' | 'all' | null>(null)
const contentType = ref<'text' | 'website' | 'pdf' | 'video' | null>(null)

const summaryAmount = 4
const firstLoadSummaryAmount = 2 * summaryAmount

const sortItems = [
  { title: 'Date', value: 'date' },
  { title: 'Favorites', value: 'favorites' },
  { title: 'Likes', value: 'likes' },
]

const privacyItems = [
  { title: 'All', value: 'all' },
  { title: 'Public', value: 'false' },
  { title: 'Private', value: 'true' },
]

const contentItems = [
  { title: 'Text', value: 'text' },
  { title: 'Website', value: 'website' },
  { title: 'PDF', value: 'pdf' },
  { title: 'Video', value: 'video' },
]

onMounted(async () => {
  await userStore.getUser()

  if (!user.value) {
    return
  }

  const querySortBy = route.query.sortBy as 'favorites' | 'likes' | 'date' || 'favorites'
  const queryPrivacyStatus = route.query.privacyStatus as 'true' | 'false' | 'all' || 'all'
  const queryContentType = route.query.contentType as 'text' | 'website' | 'pdf' | 'video' || null

  sortBy.value = querySortBy
  privacyStatus.value = queryPrivacyStatus
  contentType.value = queryContentType

  summaryStore.clearSummaries()
  loadSummaries(firstLoadSummaryAmount, queryPrivacyStatus, querySortBy, queryContentType)

  router.replace({
    query: {
      sortBy: sortBy.value,
      privacyStatus: privacyStatus.value,
      contentType: contentType.value,
    },
  })
})

watch(sortBy, (newValue, oldValue) => {
  if (!newValue || oldValue === null || !privacyStatus.value || summaryLoading.value) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, privacyStatus.value, newValue, contentType.value)
  router.replace({ query: { sortBy: newValue } })
})

watch(privacyStatus, (newValue, oldValue) => {
  if (!newValue || oldValue === null || !sortBy.value || summaryLoading.value) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, newValue, sortBy.value, contentType.value)
  router.replace({ query: { privacyStatus: newValue } })
})

watch(contentType, (newValue, oldValue) => {
  if (!newValue || oldValue === null || !sortBy.value || summaryLoading.value) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, privacyStatus.value, sortBy.value, newValue)
  router.replace({ query: { contentType: newValue } })
})

function loadSummaries(amount: number, privacyStatus: 'true' | 'false' | 'all' | null, sortBy: 'favorites' | 'likes' | 'date' | null, contentType: 'text' | 'website' | 'pdf' | 'video' | null) {
  if (!privacyStatus || !sortBy || summaryLoading.value) {
    return
  }

  summaryStore.getSummaries(amount, privacyStatus, true, sortBy, contentType)
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
      return 'primary'
  }
}
</script>

<template>
  <v-container style="display: flex; align-items: center; justify-content: center; height: 100%">
    <v-card
      v-if="userLoading"
      max-width="400"
    >
      <v-card-title class="text-h5">
        Loading user profile...
      </v-card-title>

      <v-card-text>
        <v-skeleton-loader
          type="card"
        />
      </v-card-text>
    </v-card>

    <v-card v-else>
      <v-card-title class="text-h5">
        Your panel
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

          <v-col
            cols="12"
            md="3"
          >
            <v-select
              v-model="privacyStatus"
              :items="privacyItems"
              label="Privacy status"
            />
          </v-col>
        </v-row>
      </v-card-subtitle>

      <v-card-text
        :style="`max-height: ${mobile
          ? 45
          : 65}vh; overflow-y: auto`"
      >
        <v-row v-if="summaries.length">
          <v-col
            v-for="summary in summaries"
            :key="summary.id"
            cols="12"
            md="4"
            lg="3"
            align="center"
          >
            <v-card
              class="my-3"
              max-width="400"
              height="230"
              elevation="24"
              :to="`/summary/${summary.id}`"
              align="start"
            >
              <v-card-title>
                {{ summary.title }}
              </v-card-title>

              <v-card-subtitle>
                <v-chip
                  v-if="summary.isPrivate"
                  color="error"
                >
                  Private

                  <v-icon class="ml-1">
                    mdi-lock-outline
                  </v-icon>
                </v-chip>

                <v-chip
                  v-else
                  color="success"
                >
                  Public

                  <v-icon class="ml-1">
                    mdi-lock-open-outline
                  </v-icon>
                </v-chip>

                <v-chip
                  class="ml-2"
                  :color="getChipColor(summary.contentType)"
                >
                  {{ contentItems.find((item) => item.value === summary.contentType)?.title || '' }}
                </v-chip>
              </v-card-subtitle>

              <v-card-text>
                {{ summary.summary.substring(0, 100) }}...
              </v-card-text>

              <v-card-actions>
                <div style="position: absolute; left: 15px; bottom: 10px; display: flex; align-items: center; justify-content: center;">
                  <span
                    class="text-yellow"
                    style="display: flex; align-items: center; justify-content: center;"
                  >
                    {{ summary.favorites }}

                    <v-icon
                      class="ml-1"
                      color="yellow"
                      size="x-small"
                    >
                      mdi-star
                    </v-icon>
                  </span>

                  <span
                    class="text-success ml-4"
                    style="display: flex; align-items: center; justify-content: center;"
                  >
                    {{ summary.likes }}

                    <v-icon
                      class="ml-1"
                      color="success"
                      size="x-small"
                    >
                      mdi-thumb-up
                    </v-icon>
                  </span>
                </div>

                <span
                  class="text-info"
                  style="position: absolute; right: 15px; bottom: 10px;"
                >
                  Read more
                </span>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <v-row v-if="summaryLoading">
          <v-col
            v-for="i in summaries.length
              ? summaryAmount
              : firstLoadSummaryAmount"
            :key="i"
            cols="12"
            md="4"
            lg="3"
          >
            <v-skeleton-loader
              class="mx-auto"
              max-width="400"
              type="card"
            />
          </v-col>
        </v-row>

        <v-btn
          :disabled="isEmpty || summaryLoading"
          class="mt-4"
          color="primary"
          @click="() => loadSummaries(summaryAmount, privacyStatus, sortBy, contentType)"
        >
          Load more
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>
