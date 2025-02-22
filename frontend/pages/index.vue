<script setup lang="ts">
const router = useRouter()

const summaryStore = useSummaryStore()
const { summaries, loading } = storeToRefs(summaryStore)

const authStore = useAuthStore()
const { user, initLoading } = storeToRefs(authStore)

const summariesPerPage = 8

onMounted(() => {
  if (user.value)
    router.push('/panel')

  if (!initLoading.value && !user.value) {
    summaryStore.clearSummaries()
    summaryStore.getSummaries({
      limit: summariesPerPage,
      privateParam: false,
      meOnly: false,
      sort: 'favorites',
      contentType: null,
      category: null,
    })
  }
})
</script>

<template>
  <v-container style="display: flex; align-items: center; justify-content: center; height: 100%">
    <div class="w-100%">
      <div class="mb-4 w-100% flex justify-center">
        <div
          class="text-h5"
        >
          <span class="text-h4">
            Welcome to Summarizzer!
          </span>

          <p class="my-2">
            A platform to share and read summaries of books, articles, and more.
          </p>

          <p>
            To get started, sign up or log in.
          </p>
        </div>
      </div>

      <v-row v-if="loading">
        <v-col
          v-for="i in summariesPerPage"
          :key="i"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          align="center"
        >
          <v-skeleton-loader
            rounded="xl"
            class="mx-auto my-3"
            max-width="350"
            height="230"
            type="card"
          />
        </v-col>
      </v-row>

      <v-row v-else>
        <v-col
          v-for="summary in summaries"
          :key="summary.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          align="center"
        >
          <v-card
            class="my-3"
            max-width="350"
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
                variant="text"
                :color="getCategoryColor(summary.category)"
              >
                {{ getCategory(summary.category)?.title || '' }}
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
    </div>
  </v-container>
</template>
