<script setup lang="ts">
const router = useRouter()

const summaryStore = useSummaryStore()
const { previewSummaries, loading } = storeToRefs(summaryStore)

const authStore = useAuthStore()
const { user, initLoading } = storeToRefs(authStore)

const summariesPerPage = 8

watch(initLoading, (newLoading) => {
  if (newLoading)
    return

  if (user.value) {
    router.push('/panel')

    return
  }

  if (!previewSummaries.value.length) {
    summaryStore.getPreviewSummaries(summariesPerPage)
  }
}, { immediate: true })
</script>

<template>
  <div class="landing-wrapper">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="gradient-text">
            Welcome to <span class="brand-name">Summarizzer</span>
          </h1>

          <h2 class="tagline">
            Extract insights, not distractions
          </h2>

          <p class="description">
            Transform any text, PDF, or YouTube video into concise, powerful summaries.
            Save time and focus on what matters most.
          </p>

          <div class="auth-actions">
            <NuxtLink to="/auth/login">
              <v-btn
                color="primary"
                size="large"
                elevation="3"
                class="action-btn"
              >
                Get Started
              </v-btn>
            </NuxtLink>

            <NuxtLink to="/auth/register">
              <v-btn
                variant="outlined"
                color="primary"
                size="large"
                class="action-btn ml-4"
              >
                Create Account
              </v-btn>
            </NuxtLink>
          </div>
        </div>

        <div class="hero-graphic">
          <div class="document-mockup">
            <div class="mockup-header">
              <div class="mockup-icon">
                <v-icon color="primary">
                  mdi-file-document-outline
                </v-icon>
              </div>

              <div class="mockup-title">
                Research Paper.pdf
              </div>
            </div>

            <div class="mockup-line" />

            <div class="mockup-line short" />

            <div class="mockup-line" />

            <div class="mockup-line medium" />

            <div class="mockup-line short" />
          </div>

          <div class="summary-mockup">
            <div class="mockup-header">
              <div class="mockup-icon">
                <v-icon color="primary">
                  mdi-text-box-check-outline
                </v-icon>
              </div>

              <div class="mockup-title">
                Summary
              </div>
            </div>

            <div class="mockup-line medium" />

            <div class="mockup-line short" />
          </div>

          <div class="arrow">
            <v-icon
              color="primary"
              size="x-large"
            >
              mdi-arrow-right-bold
            </v-icon>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features-section">
      <h2 class="section-title">
        Why Summarizzer?
      </h2>

      <div class="features-grid">
        <div class="feature-card">
          <v-icon
            color="primary"
            size="36"
          >
            mdi-clock-fast
          </v-icon>

          <h3>Save Time</h3>

          <p>Extract key points and insights without reading entire documents or watching full videos.</p>
        </div>

        <div class="feature-card">
          <v-icon
            color="primary"
            size="36"
          >
            mdi-format-list-bulleted
          </v-icon>

          <h3>Better Comprehension</h3>

          <p>Structured summaries help you understand and retain information more effectively.</p>
        </div>

        <div class="feature-card">
          <v-icon
            color="primary"
            size="36"
          >
            mdi-share-variant
          </v-icon>

          <h3>Share Knowledge</h3>

          <p>Discover and share summaries with a growing community of knowledge seekers.</p>
        </div>
      </div>
    </div>

    <!-- Popular Summaries Section -->
    <div class="summaries-section">
      <div class="summaries-header">
        <h2 class="section-title">
          Popular Summaries
        </h2>

        <p class="summaries-subtitle">
          Explore our top-rated community summaries
        </p>
      </div>

      <v-row v-if="loading">
        <v-col
          v-for="i in summariesPerPage"
          :key="i"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          align="center"
        >
          <v-skeleton-loader
            rounded="xl"
            class="mx-auto my-3"
            max-width="350"
            height="230"
            type="card"
          />
        </v-col>
      </v-row>

      <v-row
        v-else
        class="summaries-grid"
      >
        <v-col
          v-for="summary in previewSummaries"
          :key="summary.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          align="center"
        >
          <v-card
            class="summary-card"
            max-width="350"
            height="230"
            elevation="3"
            :to="`/summary/${summary.id}`"
            align="start"
            hover
          >
            <div class="card-content">
              <v-card-title class="summary-title">
                {{ summary.title }}
              </v-card-title>

              <v-card-subtitle>
                <v-chip
                  variant="text"
                  :color="getCategoryColor(summary.category)"
                  class="category-chip"
                >
                  <v-icon
                    size="small"
                    class="mr-1"
                  >
                    mdi-tag
                  </v-icon>
                  {{ getCategory(summary.category)?.title || '' }}
                </v-chip>
              </v-card-subtitle>

              <v-card-text class="summary-preview">
                {{ summary.summary.substring(0, 100) }}...
              </v-card-text>
            </div>

            <v-card-actions class="card-footer">
              <div class="stats">
                <span class="stat-item">
                  <v-icon
                    color="amber"
                    size="small"
                  >mdi-star</v-icon>
                  {{ summary.favorites }}
                </span>

                <span class="stat-item">
                  <v-icon
                    color="success"
                    size="small"
                  >mdi-thumb-up</v-icon>
                  {{ summary.likes }}
                </span>
              </div>

              <span class="read-more">
                Read more
                <v-icon size="small">mdi-arrow-right</v-icon>
              </span>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- CTA Section -->
    <div class="cta-section">
      <div class="cta-content">
        <h2>Ready to save time and gain insights?</h2>

        <p>Join thousands of professionals and students who use Summarizzer daily.</p>

        <div class="cta-buttons">
          <NuxtLink to="/auth/login">
            <v-btn
              color="primary"
              size="large"
              elevation="3"
              class="mr-4"
            >
              Sign In
            </v-btn>
          </NuxtLink>

          <NuxtLink to="/auth/register">
            <v-btn
              variant="outlined"
              color="primary"
              size="large"
            >
              Create Account
            </v-btn>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Base Styles */
.landing-wrapper {
  min-height: 100vh;
  background-color: #121212;
  color: #e0e0e0;
}

/* Hero Section */
.hero-section {
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #1a1f35 0%, #0d1425 100%);
  border-radius: 0 0 40px 40px;
  margin-bottom: 3rem;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.hero-text {
  flex: 1;
  max-width: 600px;
}

.gradient-text {
  font-size: 3.2rem;
  font-weight: 700;
  background: linear-gradient(90deg, #4f8cff, #6b66ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.brand-name {
  color: #6b66ff;
}

.tagline {
  font-size: 1.8rem;
  color: #a0aec0;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #a0aec0;
  margin-bottom: 2rem;
}

.auth-actions {
  display: flex;
  margin-top: 2rem;
}

.action-btn {
  min-width: 140px;
}

/* Hero Graphic */
.hero-graphic {
  flex: 1;
  max-width: 500px;
  position: relative;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.document-mockup, .summary-mockup {
  background: #1e1e1e;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 220px;
}

.document-mockup {
  position: absolute;
  left: 0;
  top: 20px;
  z-index: 1;
}

.summary-mockup {
  position: absolute;
  right: 0;
  bottom: 20px;
  z-index: 2;
}

.arrow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3;
  background: rgba(30, 30, 30, 0.7);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.mockup-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.mockup-icon {
  margin-right: 0.5rem;
}

.mockup-title {
  font-weight: 500;
  color: #a0aec0;
}

.mockup-line {
  height: 10px;
  background: #333;
  border-radius: 5px;
  margin-bottom: 0.8rem;
  width: 100%;
}

.mockup-line.short {
  width: 60%;
}

.mockup-line.medium {
  width: 80%;
}

/* Features Section */
.features-section {
  padding: 3rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 2.2rem;
  text-align: center;
  margin-bottom: 3rem;
  color: #e0e0e0;
}

.features-grid {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.feature-card {
  background: #1e1e1e;
  padding: 2rem;
  border-radius: 16px;
  width: 300px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.feature-card h3 {
  font-size: 1.3rem;
  margin: 1rem 0;
  color: #e0e0e0;
}

.feature-card p {
  color: #a0aec0;
  line-height: 1.6;
}

/* Summaries Section */
.summaries-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.summaries-header {
  text-align: center;
  margin-bottom: 2rem;
}

.summaries-subtitle {
  color: #a0aec0;
  font-size: 1.1rem;
  margin-top: -1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: #1e1e1e;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.summary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3) !important;
}

.card-content {
  flex-grow: 1;
}

.summary-title {
  font-size: 1.2rem !important;
  line-height: 1.4;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  height: auto !important;
  white-space: normal !important;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

.category-chip {
  margin-top: 0.5rem;
  font-size: 0.85rem;
}

.summary-preview {
  color: #a0aec0;
  font-size: 0.95rem;
  line-height: 1.5;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding: 0.75rem 1rem !important;
}

.stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9rem;
}

.read-more {
  color: #4f8cff;
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
  border-radius: 40px 40px 0 0;
  margin-top: 3rem;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-content h2 {
  font-size: 2.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.cta-content p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.cta-buttons .v-btn {
  min-width: 140px;
  color: white !important;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* Responsive Design */
@media (max-width: 900px) {
  .hero-content {
    flex-direction: column;
    text-align: center;
  }

  .hero-text {
    max-width: 100%;
  }

  .auth-actions {
    justify-content: center;
  }

  .hero-graphic {
    margin-top: 3rem;
    margin-bottom: 1rem;
  }

  .document-mockup {
    left: 50%;
    transform: translateX(-90%);
  }

  .summary-mockup {
    right: 50%;
    transform: translateX(90%);
  }

  .gradient-text {
    font-size: 2.8rem;
  }

  .tagline {
    font-size: 1.5rem;
  }
}

@media (max-width: 600px) {
  .hero-section {
    padding: 3rem 1rem;
  }

  .gradient-text {
    font-size: 2.4rem;
  }

  .tagline {
    font-size: 1.3rem;
  }

  .description {
    font-size: 1rem;
  }

  .hero-graphic {
    display: none;
  }

  .features-grid {
    flex-direction: column;
    align-items: center;
  }

  .cta-content h2 {
    font-size: 1.8rem;
  }

  .cta-content p {
    font-size: 1rem;
  }
}
</style>
