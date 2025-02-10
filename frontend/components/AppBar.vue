<script setup lang="ts">
import { useDisplay } from 'vuetify';

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const { mobile } = useDisplay()

const search = ref('')
</script>

<template>
  <v-app-bar
    v-if="!mobile"
    rounded
    style="display: flex; align-items: center;"
  >
    <div>
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
        class="z-1 ml-2"
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
        max-width="500"
      />
    </div>

    <div
      v-if="!user"
      class="ml-auto"
    >
      <v-btn
        variant="text"
        to="/auth/login"
        color="primary"
        prepend-icon="mdi-login"
        class="z-1"
      >
        Login
      </v-btn>

      <v-btn
        class="z-1 ml-2"
        variant="text"
        to="/auth/register"
        color="primary"
        prepend-icon="mdi-account-plus"
      >
        Register
      </v-btn>
    </div>

    <div
      v-else
      class="ml-auto"
    >
      <v-btn
        class="z-1"
        variant="text"
        to="/summary/create"
        color="secondary"
        prepend-icon="mdi-plus"
      >
        Add
      </v-btn>

      <v-btn
        class="z-1 ml-2"
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
      <div style="display: flex; justify-content: center; width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch;">
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
          v-if="!user"
          variant="text"
          to="/auth/login"
          color="primary"
        >
          Login
        </v-btn>

        <v-btn
          v-if="!user"
          variant="text"
          to="/auth/register"
          color="primary"
        >
          Register
        </v-btn>

        <v-btn
          v-if="user"
          variant="text"
          to="/auth/logout"
          color="primary"
        >
          Logout
        </v-btn>
      </div>
    </template>
  </v-app-bar>
</template>
