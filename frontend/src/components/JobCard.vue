<template>
  <div class="card job-card border-0 shadow-sm h-100">
    <div class="card-body d-flex flex-column">

      <div class="d-flex justify-content-between align-items-start mb-3">
        <span class="badge bg-primary-subtle text-primary">
          {{ job.job_type }}
        </span>

        <span class="badge bg-success-subtle text-success">
          {{ job.match_score }}% Match
        </span>
      </div>

      <h5 class="fw-bold">{{ job.title }}</h5>

      <p class="text-muted mb-2">{{ job.company }}</p>

      <p class="text-muted small mb-3">
        📍 {{ job.location }} · {{ job.experience }}
      </p>

      <div class="mb-3">
        <span
          v-for="skill in job.skills"
          :key="skill"
          class="badge bg-light text-dark me-2 mb-2"
        >
          {{ skill }}
        </span>
      </div>

      <div class="mt-auto d-flex gap-2">
        <a
          :href="job.apply_url"
          target="_blank"
          rel="noopener noreferrer"
          class="btn btn-primary btn-sm"
        >
          View Job
        </a>

        <button class="btn btn-outline-secondary btn-sm">
          Save Job
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
defineProps({
  job: {
    type: Object,
    required: true,
  },
});
</script>