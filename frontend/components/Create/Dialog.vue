<script setup lang="ts">
const router = useRouter()

const summaryStore = useSummaryStore()
const { loading, recentlyCreatedId, recentlyError } = storeToRefs(summaryStore)

const isShow = defineModel<boolean>('isShow', { default: false })

function goToSummary() {
  if (!loading.value && recentlyCreatedId.value) {
    router.push(`/summary/${recentlyCreatedId.value}`)
  }
}

function getFullUrl() {
  return window.location.href.replace('/create', `/${recentlyCreatedId.value}`)
}
</script>

<template>
  <v-dialog
    v-model="isShow"
    max-width="400"
    persistent
  >
    <v-card>
      <v-card-title>
        Creating a new summary
      </v-card-title>

      <v-divider />

      <v-card-text>
        <div v-if="loading">
          Creating summary. Please wait...
        </div>

        <div v-else-if="!loading && recentlyError">
          <p>
            An error occurred while creating summary.
          </p>

          <p>
            Error: {{ recentlyError }}
          </p>
        </div>

        <div v-else-if="!loading && recentlyCreatedId">
          <p>
            Summary created successfully.
          </p>

          <p>
            <NuxtLink :to="`/summary/${recentlyCreatedId}`">
              {{ getFullUrl() }}
            </NuxtLink>
          </p>
        </div>
      </v-card-text>

      <v-divider />

      <v-card-actions>
        <v-btn
          color="error"
          variant="text"
          @click="isShow = false"
        >
          Close
        </v-btn>

        <v-btn
          :color="loading
            ? 'grey'
            : 'primary'"
          variant="text"
          :disabled="Boolean(!loading && recentlyError)"
          @click="goToSummary"
        >
          Go to summary
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
