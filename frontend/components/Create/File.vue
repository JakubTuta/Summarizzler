<script setup lang="ts">
const summaryStore = useSummaryStore()

const formData = ref<FormData | null>(null)
const wrongFileType = ref(false)
const userPrompt = ref('')
const isPrivate = ref(false)
const isShowDialog = ref(false)

function handleFileDrop(event: any) {
  const fileList = event.dataTransfer.files
  handleFile(fileList)
}

function handleFileChoose(event: any) {
  const fileList = event.target.files
  handleFile(fileList)
}

function handleFile(fileList: any[]) {
  if (fileList.length === 0)
    return

  const file = fileList[0]
  if (!file.name.endsWith('.pdf')) {
    wrongFileType.value = true

    return
  }

  formData.value = new FormData()
  formData.value.append('file', file)
}

function send() {
  if (!formData.value || !userPrompt.value)
    return

  formData.value.append('prompt', userPrompt.value)
  formData.value.append('isPrivate', isPrivate.value.toString())

  summaryStore.createFileSummary(formData.value)
  isShowDialog.value = true
}
</script>

<template>
  <v-card>
    <v-card-title>
      Summarize PDF
    </v-card-title>

    <v-card-text>
      <div align="center">
        <v-sheet
          class="d-flex align-center justify-center"
          min-height="220px"
          max-width="600px"
          border
          rounded
          :color="wrongFileType
            ? 'rgba(255, 0, 0, 0.05)'
            : formData && formData.get('file')
              ? 'rgba(0, 255, 0, 0.05)'
              : ''"
          @dragover.prevent
          @drop.prevent="handleFileDrop"
        >
          <div class="align-center flex-column flex justify-center">
            <v-icon
              size="48"
              class="mb-2"
            >
              mdi-cloud-upload
            </v-icon>

            <div>Drag and drop files here or</div>

            <v-btn
              color="primary"
              class="mt-2"
              @click="$refs.fileInput.click()"
            >
              Browse Files
            </v-btn>

            <input
              ref="fileInput"
              type="file"
              style="display: none"
              accept=".pdf"
              @change="handleFileChoose"
            >

            <div
              v-if="formData && formData.get('file')"
              class="mt-6"
            >
              {{ formData.get('file')!.name || '' }}
            </div>
          </div>
        </v-sheet>
      </div>

      <v-textarea
        v-model="userPrompt"
        label="User prompt"
        class="mt-6"
        auto-grow
        no-resize
        rows="1"
        hint="What would You like to get from this website? e.g. summary, main points, etc."
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
        :color="formData && userPrompt
          ? 'primary'
          : 'grey'"
        @click="send"
      >
        <v-tooltip
          v-if="!formData || !userPrompt"
          location="bottom"
          activator="parent"
        >
          You have to fill in all fields
        </v-tooltip>
        Summarize
      </v-btn>
    </v-card-text>
  </v-card>

  <v-snackbar
    v-model="wrongFileType"
    color="error"
  >
    Only PDF files are accepted!
  </v-snackbar>

  <CreateDialog v-model:is-show="isShowDialog" />
</template>
