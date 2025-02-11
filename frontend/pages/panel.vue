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

onMounted(async () => {
  await userStore.getUser()

  if (!user.value) {
    return
  }

  const querySortBy = route.query.sortBy as 'favorites' | 'likes' | 'date' || 'date'
  const queryPrivacyStatus = route.query.privacyStatus as 'true' | 'false' | 'all' || 'all'

  sortBy.value = querySortBy
  privacyStatus.value = queryPrivacyStatus

  loadSummaries(firstLoadSummaryAmount, queryPrivacyStatus, querySortBy)

  router.replace({ query: { sortBy: sortBy.value } })
})

function loadSummaries(amount: number, privacyStatus: 'true' | 'false' | 'all' | null, sortBy: 'favorites' | 'likes' | 'date' | null) {
  if (!privacyStatus || !sortBy || summaryLoading.value) {
    return
  }

  summaryStore.getSummaries(amount, privacyStatus, true, sortBy)
}

watch(sortBy, (newValue) => {
  if (!newValue || !privacyStatus.value || summaryLoading.value || !summaries.value.length) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, privacyStatus.value, newValue)
  router.replace({ query: { sortBy: newValue } })
})

watch(privacyStatus, (newValue) => {
  if (!newValue || !sortBy.value || summaryLoading.value || !summaries.value.length) {
    return
  }

  summaryStore.clearSummaries()
  loadSummaries(summaryAmount, newValue, sortBy.value)
  router.replace({ query: { privacyStatus: newValue } })
})
</script>

<template>
  <v-container style="display: flex; align-items: center; justify-content: center; height: 100%">
    <v-card
      v-if="userLoading"
      max-width="400"
    >
      <v-card-title>
        Loading user profile...
      </v-card-title>

      <v-card-text>
        <v-skeleton-loader
          type="card"
        />
      </v-card-text>
    </v-card>

    <v-card
      v-else
      :style="`max-height: ${mobile
        ? 80
        : 90}vh; overflow-y: auto`"
    >
      <v-card-title>
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

      <v-card-text>
        <v-row v-if="summaries.length">
          <v-col
            v-for="summary in summaries"
            :key="summary.id"
            cols="12"
            md="4"
            lg="3"
          >
            <v-card
              class="my-3"
              max-width="400"
              height="230"
              elevation="24"
              :to="`/summary/${summary.id}`"
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
                </v-chip>

                <v-chip
                  v-else
                  color="success"
                >
                  Public
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
                  style="position: absolute; right: 10px; bottom: 10px;"
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
          @click="() => loadSummaries(summaryAmount, privacyStatus, sortBy)"
        >
          Load more
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>
