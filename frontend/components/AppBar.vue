<script setup lang="ts">
import { useDisplay } from 'vuetify'

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const summaryStore = useSummaryStore()
const { searchSummaries } = storeToRefs(summaryStore)

const { mobile, smAndDown } = useDisplay()

const search = ref('')
const loading = ref(false)

const debounceTimer = ref<NodeJS.Timeout>()

function searchFunction(value: string) {
  if (value.length < 3)
    return

  loading.value = true

  if (debounceTimer.value)
    clearTimeout(debounceTimer.value)

  debounceTimer.value = setTimeout(async () => {
    await summaryStore.searchSummary(value)
    loading.value = false
  }, 1000)
}
</script>

<template>
  <v-app-bar
    v-if="!mobile"
    rounded
    style="display: flex; align-items: center;"
  >
    <div class="ml-3">
      <v-btn
        :to="user
          ? '/panel'
          : '/'"
        variant="text"
        color="secondary"
        style="cursor: pointer;"
        class="z-1"
      >
        Home
      </v-btn>

      <v-btn
        variant="text"
        to="/discover"
        color="secondary"
        class="z-1 ml-3"
      >
        Discover
      </v-btn>
    </div>

    <div style="position: absolute; left: 0; right: 0; justify-content: center; display: flex;">
      <v-text-field
        v-model="search"
        append-inner-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
        density="comfortable"
        rounded
        :max-width="smAndDown
          ? '300px'
          : '400px'"
        @update:model-value="searchFunction"
      >
        <v-menu
          activator="parent"
          location="top"
        >
          <v-list v-if="searchSummaries.length">
            <v-list-item
              v-for="summary in searchSummaries"
              :key="summary.id"
              :to="`/summary/${summary.id}`"
            >
              <v-list-item-title>
                {{ summary.title }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <template #loader>
          <v-progress-linear
            :active="loading"
            color="primary"
            height="5"
            indeterminate
            z-2
          />
        </template>
      </v-text-field>
    </div>

    <div
      v-if="user"
      class="ml-auto mr-3"
    >
      <v-btn
        class="z-1"
        variant="text"
        to="/summary/create"
        color="secondary"
        prepend-icon="mdi-plus"
      >
        New
      </v-btn>

      <v-btn
        class="z-1 ml-3"
        variant="text"
        to="/auth/logout"
        color="primary"
        prepend-icon="mdi-logout"
      >
        Logout
      </v-btn>
    </div>
  </v-app-bar>

  <v-app-bar
    v-else
    extended
    rounded
  >
    <div style="display: flex; align-items: center; justify-content: center; width: 100%;">
      <v-text-field
        v-model="search"
        append-inner-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
        density="comfortable"
        rounded
        max-width="90%"
      />
    </div>

    <template #extension>
      <div
        class="scrollable-container mx-3"
      >
        <v-btn
          :to="user
            ? '/panel'
            : '/'"
          variant="text"
          color="secondary"
          style="cursor: pointer;"
        >
          Home
        </v-btn>

        <v-btn
          variant="text"
          to="/discover"
          color="secondary"
          class="ml-3"
        >
          Discover
        </v-btn>

        <div v-if="!user">
          <v-btn
            v-if="!user"
            variant="text"
            to="/auth/login"
            color="primary"
            prepend-icon="mdi-login"
          >
            Login
          </v-btn>

          <v-btn
            v-if="!user"
            variant="text"
            to="/auth/register"
            color="primary"
            prepend-icon="mdi-account-plus"
            class="ml-3"
          >
            Register
          </v-btn>
        </div>

        <div v-if="user">
          <v-btn
            variant="text"
            to="/summary/create"
            color="secondary"
            prepend-icon="mdi-plus"
          >
            New
          </v-btn>

          <v-btn
            variant="text"
            to="/auth/logout"
            color="primary"
            prepend-icon="mdi-logout"
          >
            Logout
          </v-btn>
        </div>
      </div>
    </template>
  </v-app-bar>
</template>

<style scoped>
.scrollable-container {
  display: flex;
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  white-space: nowrap;
  scrollbar-width: thin;
  padding-bottom: 5px;
}

.scrollable-container::-webkit-scrollbar {
  height: 6px;
}

.scrollable-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.scrollable-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}
</style>
