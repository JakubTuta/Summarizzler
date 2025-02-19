<script setup lang="ts">
const summaryStore = useSummaryStore()
const { summaries, loading } = storeToRefs(summaryStore)

const summariesPerPage = 8

onMounted(async () => {
  summaryStore.clearSummaries()
  await summaryStore.getSummaries({
    limit: summariesPerPage,
    privateParam: false,
    meOnly: false,
    sort: 'favorites',
    contentType: null,
    category: null,
  })
})
</script>

<template>
  <v-container style="display: flex; align-items: center; justify-content: center; height: 100%">
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
          class="mx-auto"
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
  </v-container>
</template>
