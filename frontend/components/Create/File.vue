<script setup lang="ts">
function handleDrop() {

}

function handleFileInput() {

}
</script>

<template>
  <v-card>
    <v-card-title>Drop files here</v-card-title>

    <v-card-text align="center">
      <v-sheet
        class="d-flex align-center justify-center"
        height="200"
        width="600"
        border
        rounded
        @dragover.prevent
        @drop.prevent="handleDrop"
      >
        <div class="text-center">
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
            multiple
            @change="handleFileInput"
          >
        </div>
      </v-sheet>
    </v-card-text>
  </v-card>
</template>
