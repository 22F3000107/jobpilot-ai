
<template>
  <div class="card job-card border-0 shadow-sm h-100">
    <div class="card-body d-flex flex-column">
      <div class="d-flex justify-content-between align-items-start mb-3">
        <span class="badge bg-primary-subtle text-primary">
          {{ job.job_type }}
        </span>

          <span
  v-if="applicationStatus"
  class="badge ms-1"
  :class="{
    'bg-primary-subtle text-primary': applicationStatus === 'Applied',
    'bg-warning-subtle text-warning-emphasis': applicationStatus === 'Assessment',
    'bg-info-subtle text-info-emphasis': applicationStatus === 'Interview',
    'bg-success-subtle text-success': applicationStatus === 'Offer',
    'bg-danger-subtle text-danger': applicationStatus === 'Rejected'
  }"
>
  {{
    applicationStatus === "Applied"
      ? "📌 Applied"
      : applicationStatus === "Assessment"
        ? "📝 Assessment"
        : applicationStatus === "Interview"
          ? "🎯 Interview"
          : applicationStatus === "Offer"
            ? "🎉 Offer"
            : "❌ Rejected"
  }}
</span>


        <span
  v-if="job.priority"
  class="badge ms-1"
  :class="{
    'bg-success-subtle text-success': job.priority === 'high',
    'bg-warning-subtle text-warning-emphasis': job.priority === 'medium',
    'bg-danger-subtle text-danger': job.priority === 'low'
  }"
>
  {{
    job.priority === "high"
      ? "🟢 High Priority"
      : job.priority === "medium"
        ? "🟡 Medium Priority"
        : "🔴 Low Priority"
  }}
</span>

        <span class="badge bg-success-subtle text-success">
          {{ job.match_score }}% Match
        </span>
       
        <div
          v-if="job.match_breakdown"
          class="mt-3 p-2 bg-light rounded"
        >
         <div class="small fw-semibold mb-2">
          Match Breakdown
         </div>

         <div class="small d-flex justify-content-between">
  <span>Skills</span>

  <span v-if="job.match_breakdown.skills.available">
    {{ job.match_breakdown.skills.score }}/50
  </span>

  <span v-else class="text-muted">
    Not enough data
  </span>
</div>

<div
  v-if="job.match_breakdown.skills.available"
  class="mt-2"
>
  <div
    v-if="job.match_breakdown.skills.matched.length > 0"
    class="small text-success"
  >
    <strong>✓ Matched:</strong>
    {{ job.match_breakdown.skills.matched.join(", ") }}
  </div>

  <div
    v-if="job.match_breakdown.skills.unmatched.length > 0"
    class="small text-danger"
  >
    <strong>✗ Missing:</strong>
    {{ job.match_breakdown.skills.unmatched.join(", ") }}
  </div>
</div>

        <div class="small d-flex justify-content-between">
         <span>Role</span>
         <span>
          {{ job.match_breakdown.role.score }}/20
         </span>
        </div>

        <div class="small d-flex justify-content-between">
          <span>Location</span>
          <span>
          {{ job.match_breakdown.location.score }}/15
          </span>
        </div>

        <div class="small d-flex justify-content-between">
          <span>Experience</span>
          <span>
            {{ job.match_breakdown.experience.score }}/15
          </span>
      </div>
     </div>

      </div>

      <h5 class="fw-bold">{{ job.title }}</h5>

      <p class="text-muted mb-2">{{ job.company }}</p>

      <p class="text-muted small mb-1">
         📍 {{ job.location }} · {{ job.experience }}
      </p>
       <p
  v-if="job.salary_min || job.salary_max"
  class="text-muted small mb-1"
>
  💰
   <span v-if="job.salary_min && job.salary_max">
  {{ formatSalary(job.salary_min) }}
  – {{ formatSalary(job.salary_max) }}
</span>

<span v-else-if="job.salary_min">
  From {{ formatSalary(job.salary_min) }}
</span>

<span v-else>
  Up to {{ formatSalary(job.salary_max) }}
</span>
</p>
        <div v-if="job.created" class="mb-3">

  <span
    v-if="isFreshJob(job.created)"
    class="badge bg-warning-subtle text-warning-emphasis me-2"
  >
    🔥 Fresh
  </span>

  <span class="text-muted small">
    🕐 {{ getPostedLabel(job.created) }}
  </span>

</div>

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
        <button
           class="btn btn-primary btn-sm"
           @click="handleViewDetails"
        >
           View Details
        </button>

        <button
          class="btn btn-sm"
          :class="isSaved ? 'btn-success' : 'btn-outline-primary'"
          @click="handleSave"
        >
          {{ isSaved ? "✓ Saved" : "Save Job" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>

function getPostedLabel(created) {
  if (!created) {
    return "";
  }

  const postedDate = new Date(created);
  const now = new Date();

  const diffMs = now - postedDate;
  const diffDays = Math.floor(
    diffMs / (1000 * 60 * 60 * 24)
  );

  if (diffDays <= 0) {
    return "Posted today";
  }

  if (diffDays === 1) {
    return "Posted 1 day ago";
  }

  return `Posted ${diffDays} days ago`;
}

function isFreshJob(created) {
  if (!created) {
    return false;
  }

  const postedDate = new Date(created);
  const now = new Date();

  const diffMs = now - postedDate;
  const diffDays = Math.floor(
    diffMs / (1000 * 60 * 60 * 24)
  );

  return diffDays <= 3;
}

const props = defineProps({
  job: {
    type: Object,
    required: true,
  },
  isSaved: {
    type: Boolean,
    default: false,
  },
  applicationStatus: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["save", "view-details"]);

function handleSave() {
  if (props.isSaved) {
    return;
  }

  emit("save", props.job);
}

function handleViewDetails() {
  emit("view-details", props.job);
}
function formatSalary(amount) {
  if (!amount) {
    return "";
  }

  const lakh = amount / 100000;

  if (lakh >= 1) {
    return `₹${lakh % 1 === 0 ? lakh : lakh.toFixed(1)}L`;
  }

  return `₹${Math.round(amount).toLocaleString("en-IN")}`;
}
</script>

