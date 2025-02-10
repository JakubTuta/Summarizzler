<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const summaryStore = useSummaryStore()
const { summaries, loading: summaryLoading } = storeToRefs(summaryStore)

const summaryAmount = 8

onMounted(() => {
  userStore.getUser()
})

watch(user, (newUser) => {
  if (!newUser) {
    return
  }

  summaryStore.getSummaries(summaryAmount, 'all', true)
}, { immediate: true })
</script>

<template>
  <v-container style="display: flex; align-items: center; justify-content: center; height: 100%">
    <v-row v-if="summaryLoading">
      <v-col
        v-for="i in 8"
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

    <v-row v-else>
      <v-col
        v-for="summary in summaries"
        :key="summary.id"
        cols="12"
        md="4"
        lg="3"
      >
        <v-card
          class="my-2"
          max-width="400"
          height="200"
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
            <div style="position: absolute; left: 10px; bottom: 10px; display: flex; align-items: center; justify-content: center;">
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
