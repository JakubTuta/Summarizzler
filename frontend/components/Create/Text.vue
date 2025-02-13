<script setup lang="ts">
const text = ref('')
const userPrompt = ref('')
const isPrivate = ref(false)
const isShowDialog = ref(false)

const { form, valid, isValid } = useForm()

const summaryStore = useSummaryStore()

async function send() {
  if (await isValid()) {
    summaryStore.createTextSummary(text.value, userPrompt.value, isPrivate.value)
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
        <v-textarea
          v-model="text"
          label="Text"
          auto-grow
          no-resize
          rows="2"
          counter="10000"
          :rules="[
            requiredRule('Text'),
            maxLengthRule(10000),
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
          :color="text && userPrompt
            ? 'primary'
            : 'grey'"
        >
          <v-tooltip
            v-if="!text || !userPrompt"
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
