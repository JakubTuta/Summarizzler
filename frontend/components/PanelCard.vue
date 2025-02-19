<script setup lang="ts">
import { getContentType, getContentTypeColor } from '~/helpers/contentTypes';
import type { ISummaryPreview } from '~/models/summaryPreview';

const props = defineProps < { summary: ISummaryPreview } > ()

const { summary } = toRefs(props)
</script>

<template>
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
        :color="getContentTypeColor(summary.contentType)"
      >
        {{ getContentType(summary.contentType)?.title || '' }}
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
</template>
