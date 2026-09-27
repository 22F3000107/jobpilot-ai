<template>
  <div>
    <!-- Navigation -->
    <Navbar />

    <main class="container py-5">
      <!-- Page Header -->
      <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
        <div>
          <p class="text-primary fw-semibold mb-2">YOUR CAREER, SIMPLIFIED</p>
          <h1 class="fw-bold">Welcome to JobPilot AI 🚀</h1>
          <p class="text-muted">
            Discover opportunities and manage your job search in one place.
          </p>
        </div>

        <button class="btn btn-primary px-4" @click="loadJobs">
          Refresh Jobs
        </button>
      </div>

      <!-- Statistics -->
      <div class="row g-4 mb-5">
        <div class="col-md-4">
          <StatsCard
            title="Jobs Found"
            :value="jobs.length"
            subtitle="Opportunities available"
          />
        </div>

        <div class="col-md-4">
          <StatsCard
            title="Applications Sent"
            value="0"
            subtitle="Applications tracked"
          />
        </div>

        <div class="col-md-4">
          <StatsCard
            title="Interviews"
            value="0"
            subtitle="Interviews scheduled"
          />
        </div>
      </div>

      <!-- Search -->
      <section class="mb-5">
        <h3 class="fw-bold mb-3">Find Your Next Opportunity</h3>

        <div class="card border-0 shadow-sm p-3">
          <div class="row g-3">
            <div class="col-md-5">
              <input
                v-model="keyword"
                type="text"
                class="form-control"
                placeholder="Search job title or skill..."
                @input="filterJobs"
              />
            </div>

            <div class="col-md-5">
              <input
                v-model="location"
                type="text"
                class="form-control"
                placeholder="Search location..."
                @input="filterJobs"
              />
            </div>

            <div class="col-md-2">
              <button
                class="btn btn-dark w-100"
                @click="filterJobs"
              >
                Search
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Job Listings -->
      <section>
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h3 class="fw-bold mb-0">Recommended Jobs</h3>
          <span class="text-muted">{{ filteredJobs.length }} jobs</span>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="text-muted mt-3">Loading jobs...</p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
          <button class="btn btn-sm btn-outline-danger ms-3" @click="loadJobs">
            Try Again
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredJobs.length === 0" class="text-center py-5">
          <h5>No jobs found</h5>
          <p class="text-muted">
            Try another keyword or location.
          </p>
        </div>

        <!-- Job Cards -->
        <div v-else class="row g-4">
          <div
            v-for="job in filteredJobs"
            :key="job.id"
            class="col-md-6 col-lg-4"
          >
            <JobCard :job="job" />
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="text-center text-muted mt-5 pt-4">
        <p>JobPilot AI · Your personal job search assistant</p>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

import Navbar from "./components/Navbar.vue";
import StatsCard from "./components/StatsCard.vue";
import JobCard from "./components/JobCard.vue";

import { getJobs } from "./services/api";

const jobs = ref([]);
const keyword = ref("");
const location = ref("");
const loading = ref(false);
const error = ref("");

const filteredJobs = computed(() => {
  return jobs.value.filter((job) => {
    const searchText = keyword.value.toLowerCase().trim();
    const searchLocation = location.value.toLowerCase().trim();

    const matchesKeyword =
      !searchText ||
      job.title?.toLowerCase().includes(searchText) ||
      job.company?.toLowerCase().includes(searchText) ||
      job.skills?.some((skill) =>
        skill.toLowerCase().includes(searchText)
      );

    const matchesLocation =
      !searchLocation ||
      job.location?.toLowerCase().includes(searchLocation);

    return matchesKeyword && matchesLocation;
  });
});

async function loadJobs() {
  loading.value = true;
  error.value = "";

  try {
    const data = await getJobs();
    jobs.value = Array.isArray(data) ? data : data.jobs || [];
  } catch (err) {
    console.error("Error loading jobs:", err);
    error.value =
      "Unable to load jobs. Make sure your Flask backend is running on port 5000.";
  } finally {
    loading.value = false;
  }
}

function filterJobs() {
  // Filtering is handled automatically by filteredJobs.
}

onMounted(() => {
  loadJobs();
});
</script>