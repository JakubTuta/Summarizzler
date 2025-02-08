<script setup lang="ts">
const url = ref('')
const userPrompt = ref('')

const { form, valid, isValid } = useForm()

const summaryStore = useSummaryStore()

async function send() {
  if (await isValid()) {
    summaryStore.getWebsiteSummary(url.value, userPrompt.value)
  }
}
</script>

<template>
  <v-card>
    <v-card-title>
      Summarize a website
    </v-card-title>

    <v-form
      ref="form"
      v-model="valid"
      @submit.prevent="send"
    >
      <v-card-text>
        <v-text-field
          v-model="url"
          class="mt-4"
          label="Url"
          :rules="[requiredRule('URL')]"
          @keydown.enter="send"
        />

        <v-textarea
          v-model="userPrompt"
          class="mt-6"
          auto-grow
          no-resize
          rows="1"
          label="What would You like to get from this page?"
          hint="e.g. summary, main points, etc."
          persistent-hint
          :rules="[requiredRule('User Prompt')]"
        />

        <v-btn
          class="mt-6"
          type="submit"
          :color="url && userPrompt
            ? 'primary'
            : 'grey'"
        >
          <v-tooltip
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
</template>
