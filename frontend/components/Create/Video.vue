<script setup lang="ts">
const url = ref('')
const userPrompt = ref('')
const isPrivate = ref(false)
const isShowDialog = ref(false)

const { form, valid, isValid } = useForm()

const summaryStore = useSummaryStore()

async function send() {
  if (await isValid()) {
    summaryStore.createVideoSummary(url.value, userPrompt.value, isPrivate.value)
    isShowDialog.value = true
  }
}
</script>

<template>
  <v-card>
    <v-card-title>
      Summarize a text
    </v-card-title>

    <v-form
      ref="form"
      v-model="valid"
      @submit.prevent="send"
    >
      <v-card-text>
        <v-alert
          color="warning"
          class="text-h6 mb-8 mt-2 text-center"
        >
          This feature is experimental. Sometimes the data may not be accurate. In that case try again. Longer videos may take longer to summarize.
        </v-alert>

        <v-text-field
          v-model="url"
          label="YouTube video URL"
          :rules="[
            requiredRule('YouTube video URL'),
            youtubeUrlRule(),
          ]"
          @keydown.enter="send"
        />

        <v-textarea
          v-model="userPrompt"
          label="User prompt"
          class="mt-6"
          auto-grow
          no-resize
          rows="1"
          hint="What would You like to get from this text? e.g. summary, main points, etc."
          persistent-hint
          :rules="[requiredRule('User prompt')]"
          @keydown.enter="send"
        />

        <v-checkbox
          v-model="isPrivate"
          class="mt-6"
          label="Make this summary private"
        >
          <v-tooltip
            location="bottom"
            activator="parent"
          >
            Only you will be able to see this summary
          </v-tooltip>
        </v-checkbox>

        <v-btn
          class="mt-2"
          type="submit"
          :color="url && userPrompt
            ? 'primary'
            : 'grey'"
        >
          <v-tooltip
            v-if="!url || !userPrompt"
            location="bottom"
            activator="parent"
          >
            You have to fill in all fields
          </v-tooltip>
          Summarize
        </v-btn>
      </v-card-text>
    </v-form>
  </v-card>

  <CreateDialog v-model:is-show="isShowDialog" />
</template>
