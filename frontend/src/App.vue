<template>
  <div>
    <!-- Navigation -->
    <Navbar @navigate="handleNavigate" />

    <main v-if="activePage === 'dashboard'" class="container py-5">
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
  <div class="col-md-3">
    <StatsCard
      title="Jobs Found"
      :value="jobs.length"
      subtitle="Opportunities available"
    />
  </div>

  <div class="col-md-3">
    <StatsCard
      title="Applications Sent"
      :value="totalApplications"
      subtitle="Applications tracked"
    />
  </div>

  <div class="col-md-3">
    <StatsCard
      title="Interviews"
      :value="totalInterviews"
      subtitle="Interviews scheduled"
    />
  </div>

  <div class="col-md-3">
    <StatsCard
      title="Saved Jobs"
      :value="totalSavedJobs"
      subtitle="Jobs saved for later"
    />
  </div>

  <div class="col-md-3">
    <StatsCard
      title="Offers Received"
      :value="totalOffers"
      subtitle="Offers from applications"
    />
  </div>
</div>

      <!-- Reminder Summary -->
<div class="row g-4 mb-5">
  <div class="col-md-4">
    <StatsCard
      title="Overdue Reminders"
      :value="overdueReminders"
      subtitle="Follow-ups past their due date"
    />
  </div>

  <div class="col-md-4">
    <StatsCard
      title="Due Today"
      :value="remindersDueToday"
      subtitle="Follow-ups scheduled for today"
    />
  </div>

  <div class="col-md-4">
    <StatsCard
      title="Upcoming Reminders"
      :value="upcomingReminders"
      subtitle="Future follow-ups"
    />
  </div>
</div>

     <!-- Application Progress -->
<section class="card border-0 shadow-sm p-4 mb-5">
  <h3 class="fw-bold mb-4">Application Progress</h3>

  <div
    v-for="item in applicationStatusCounts"
    :key="item.status"
    class="mb-3"
  >
    <div class="d-flex justify-content-between mb-2">
      <span class="fw-semibold">{{ item.status }}</span>
      <span class="text-muted">{{ item.count }}</span>
    </div>

    <div class="progress" style="height: 10px;">
      <div
        class="progress-bar"
        role="progressbar"
        :style="{
          width: totalApplications
            ? `${(item.count / totalApplications) * 100}%`
            : '0%',
        }"
        :aria-valuenow="item.count"
        aria-valuemin="0"
        :aria-valuemax="totalApplications"
      ></div>
    </div>
  </div>
</section>

      <!-- Search -->
<section class="mb-5">
  <h3 class="fw-bold mb-3">Find Your Next Opportunity</h3>

  <div class="card border-0 shadow-sm p-3">
    <div class="row g-3">

      <!-- Keyword -->
      <div class="col-md-4">
        <input
          v-model="keyword"
          type="text"
          class="form-control"
          placeholder="Search job title or skill..."
          @input="filterJobs"
        />
      </div>

      <!-- Location -->
      <div class="col-md-3">
        <input
          v-model="location"
          type="text"
          class="form-control"
          placeholder="Search location..."
          @input="filterJobs"
        />
      </div>

      <!-- Job Type -->
      <div class="col-md-3">
        <select
          v-model="jobType"
          class="form-select"
          @change="filterJobs"
        >
          <option value="">All Job Types</option>
          <option value="Internship">Internship</option>
          <option value="Full-time">Full-time</option>
          <option value="Fresher">Fresher</option>
        </select>
      </div>

      <!-- Search Button -->
      <div class="col-md-2">
        <button
          class="btn btn-dark w-100"
          @click="filterJobs"
        >
          Search
        </button>
      </div>
     
      <div class="row mt-3">
  <div class="col-md-4">
    <label class="form-label fw-semibold">Sort Jobs By</label>
    <select v-model="sortBy" class="form-select">
      <option value="match">Highest Match</option>
      <option value="match-low">Lowest Match</option>
      <option value="title">Job Title (A–Z)</option>
    </select>
  </div>
</div>


    </div>
  </div>
</section>

      <!-- Job Listings -->
      <section>
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h3 class="fw-bold mb-0">Recommended Jobs</h3>
          <span class="text-muted">{{ filteredJobs?.length ?? 0 }} jobs</span>
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
  v-for="job in paginatedJobs"
  :key="job.id"
  class="col-md-6 col-lg-4"
>
  <JobCard
  :job="job"
  :is-saved="savedJobIds.includes(job.id)"
  @save="handleSaveJob"
/>
</div>

    <!-- Pagination -->
<div
  v-if="totalPages > 1"
  class="d-flex justify-content-center align-items-center gap-3 mt-4"
>
  <button
    class="btn btn-outline-primary"
    @click="previousPage"
    :disabled="currentPage === 1"
  >
    ← Previous
  </button>

  <span class="fw-semibold">
    Page {{ currentPage }} of {{ totalPages }}
  </span>

  <button
    class="btn btn-outline-primary"
    @click="nextPage"
    :disabled="currentPage === totalPages"
  >
    Next →
  </button>
</div>

        </div>
      </section>

      <!-- Footer -->
      <footer class="text-center text-muted mt-5 pt-4">
        <p>JobPilot AI · Your personal job search assistant</p>
      </footer>
    </main>
    <!-- Saved Jobs Page -->
<main
  v-else-if="activePage === 'saved-jobs'"
  class="container py-5"
>
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div>
      <h1 class="fw-bold">Saved Jobs ⭐</h1>
      <p class="text-muted">
        Keep track of opportunities you want to apply for.
      </p>
    </div>

    <button
      class="btn btn-outline-primary"
      @click="loadSavedJobs"
    >
      Refresh
    </button>
  </div>

  <div v-if="savedJobsLoading" class="text-center py-5">
    <div class="spinner-border text-primary"></div>
    <p class="text-muted mt-3">Loading saved jobs...</p>
  </div>

  <div v-else-if="savedJobsError" class="alert alert-danger">
    {{ savedJobsError }}
  </div>

  <div v-else-if="savedJobs.length === 0" class="text-center py-5">
    <h4>No saved jobs yet</h4>
    <p class="text-muted">
      Visit Find Jobs and save opportunities you're interested in.
    </p>
  </div>

  <div v-else class="row g-4">
    <div
      v-for="job in savedJobs"
      :key="job.id"
      class="col-md-6 col-lg-4"
    >
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body d-flex flex-column">
          <span class="badge bg-success-subtle text-success align-self-start mb-3">
            {{ job.match_score }}% Match
          </span>

          <h5 class="fw-bold">{{ job.title }}</h5>
          <p class="text-muted mb-2">{{ job.company }}</p>

          <p class="text-muted small">
            📍 {{ job.location }} · {{ job.job_type }}
          </p>

          <div class="mb-3">
            <span
              v-for="skill in job.skills || []"
              :key="skill"
              class="badge bg-light text-dark me-2 mb-2"
            >
              {{ skill }}
            </span>
          </div>

          <div class="mt-auto">
            <button
              class="btn btn-success btn-sm me-2"
              @click="handleMarkApplied(job)"
            >
              Mark as Applied
            </button>
            <button
              class="btn btn-outline-danger btn-sm"
              @click="handleDeleteSavedJob(job.id)"
            >
              Remove

              
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>

<!-- Applications Page -->
<main
  v-else-if="activePage === 'applications'"
  class="container py-5"
>
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div>
      <h1 class="fw-bold">My Applications 📋</h1>
      <p class="text-muted">
        Track your job applications and their progress.
      </p>
    </div>

    <button
      class="btn btn-outline-primary"
      @click="loadApplications"
    >
      Refresh
    </button>
  </div>

  <div v-if="applicationsLoading" class="text-center py-5">
    <div class="spinner-border text-primary"></div>
    <p class="text-muted mt-3">Loading applications...</p>
  </div>

  <div v-else-if="applicationsError" class="alert alert-danger">
    {{ applicationsError }}
  </div>

  <div v-else-if="applications.length === 0" class="text-center py-5">
    <h4>No applications yet</h4>
    <p class="text-muted">
      Save a job and start tracking your applications.
    </p>
  </div>

  <div v-else class="row g-4">
    <div
      v-for="application in applications"
      :key="application.id"
      class="col-md-6 col-lg-4"
    >
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body d-flex flex-column">
          <h5 class="fw-bold">{{ application.title }}</h5>

          <p class="text-muted mb-2">
            {{ application.company }}
          </p>

          <p class="text-muted small">
            📍 {{ application.location || "Location not specified" }}
          </p>

          <p class="small text-muted">
            Applied:
            {{ application.applied_at
              ? new Date(application.applied_at).toLocaleDateString()
              : "Date unavailable" }}
          </p>

          <div class="mb-3">
            <label class="form-label fw-semibold">
              Application Status
            </label>

            <select
              class="form-select"
              :value="application.status"
              @change="handleUpdateApplication(
                application.id,
                $event.target.value
              )"
            >
              <option>Applied</option>
              <option>Assessment</option>
              <option>Interview</option>
              <option>Offer</option>
              <option>Rejected</option>
            </select>
          </div>

          <!-- Application Notes -->
<div class="mb-3">
  <label class="form-label fw-semibold">
    Application Notes
  </label>

  <textarea
    v-model="application.notes"
    class="form-control"
    rows="4"
    placeholder="Add interview details, assessment deadlines, recruiter information..."
  ></textarea>

  <button
    class="btn btn-primary btn-sm mt-2"
    @click="handleSaveNotes(application)"
  >
    Save Notes
  </button>
</div>

<!-- Follow-Up Reminder -->
<div class="mb-3">
  <label class="form-label fw-semibold">
    Follow-Up Reminder
  </label>

  <input
    type="date"
    class="form-control"
    v-model="application.follow_up_date"
  />

  <button
    class="btn btn-outline-primary btn-sm mt-2"
    @click="handleSaveFollowUp(application)"
  >
    Save Reminder
  </button>
</div>

<span
  v-if="application.follow_up_date"
  class="badge mt-2"
  :class="{
    'bg-danger': getReminderStatus(application.follow_up_date) === 'Overdue',
    'bg-warning text-dark': getReminderStatus(application.follow_up_date) === 'Due Today',
    'bg-success': getReminderStatus(application.follow_up_date) === 'Upcoming'
  }"
>
  {{ getReminderStatus(application.follow_up_date) }}
</span>

<!-- Delete Application -->
<div class="mt-auto">
  <button
    class="btn btn-outline-danger btn-sm"
    @click="handleDeleteApplication(application.id)"
  >
    Delete Application
  </button>
</div>
        </div>
      </div>
    </div>
  </div>
</main>

<ProfileForm v-else-if="activePage === 'profile'" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

import Navbar from "./components/Navbar.vue";
import StatsCard from "./components/StatsCard.vue";
import JobCard from "./components/JobCard.vue";
import ProfileForm from "./components/ProfileForm.vue";


import {
  getJobs,
  getProfile,
  saveJob,
  getSavedJobs,
  deleteSavedJob,
  getApplications,
  createApplication,
  updateApplication,
  deleteApplication,
} from "./services/api";

const activePage = ref("dashboard");

const jobs = ref([]);
const profile = ref(null);
const keyword = ref("");
const location = ref("");
const jobType = ref("");
const sortBy = ref("match");
const currentPage = ref(1);
const jobsPerPage = ref(2);
const loading = ref(false);
const error = ref("");
const savedJobs = ref([]);
const savedJobIds = ref([]);
const applications = ref([]);
const totalApplications = computed(() => applications.value.length);

const totalInterviews = computed(
  () =>
    applications.value.filter((app) => app.status === "Interview").length
);

const totalOffers = computed(
  () =>
    applications.value.filter((app) => app.status === "Offer").length
);

const totalSavedJobs = computed(() => savedJobs.value.length);
const applicationsLoading = ref(false);
const applicationsError = ref("");
const savedJobsLoading = ref(false);
const savedJobsError = ref("");


async function loadJobs() {
  loading.value = true;
  error.value = "";

  try {
    const [jobsData, profileData] = await Promise.all([
      getJobs(),
      getProfile(),
    ]);

    jobs.value = Array.isArray(jobsData)
      ? jobsData
      : jobsData.jobs || [];

    profile.value = profileData;
  } catch (err) {
    console.error("Error loading dashboard data:", err);

    error.value =
      "Unable to load jobs or profile. Please check that your backend is running and your profile is saved.";
  } finally {
    loading.value = false;
  }
}

async function handleSaveJob(job) {
  try {
    if (savedJobIds.value.includes(job.id)) {
      return;
    }

    const response = await saveJob({
      job_id: job.id,
      title: job.title,
      company: job.company,
      location: job.location,
      job_type: job.job_type,
      skills: job.skills,
      match_score: job.match_score,
    });

    savedJobIds.value.push(job.id);

    alert(response.message);
  } catch (err) {
    console.error("Error saving job:", err);

    alert(
      err.response?.data?.message ||
      "Unable to save this job. Please try again."
    );
  }
}

async function loadSavedJobs() {
  savedJobsLoading.value = true;
  savedJobsError.value = "";

  try {
    const data = await getSavedJobs();

    savedJobs.value = Array.isArray(data)
      ? data
      : data.saved_jobs || [];

    savedJobIds.value = savedJobs.value.map(
      (job) => job.job_id
    );
  } catch (err) {
    console.error("Error loading saved jobs:", err);
    savedJobsError.value = "Unable to load saved jobs. Please try again.";
  } finally {
    savedJobsLoading.value = false;
  }
}

async function handleDeleteSavedJob(savedJobId) {
  const confirmed = window.confirm(
    "Are you sure you want to remove this saved job?"
  );

  if (!confirmed) return;

  try {
    await deleteSavedJob(savedJobId);
    savedJobs.value = savedJobs.value.filter(
      (job) => job.id !== savedJobId
    );
  } catch (err) {
    console.error("Error deleting saved job:", err);
    alert("Unable to remove this job. Please try again.");
  }
}

async function handleMarkApplied(job) {
  try {
    // Prevent duplicate applications
    const alreadyApplied = applications.value.some(
      (app) => app.job_id === job.job_id
    );

    if (alreadyApplied) {
      alert("You have already added this job to your applications.");
      return;
    }

    await createApplication({
      job_id: job.job_id,
      title: job.title,
      company: job.company,
      location: job.location,
      job_type: job.job_type,
      apply_url: job.apply_url || "",
      notes: "",
    });

    await loadApplications();

    alert("Job added to My Applications successfully!");
  } catch (error) {
    console.error("Error adding application:", error);
    alert("Failed to add this job to My Applications.");
  }
}

async function loadApplications() {
  applicationsLoading.value = true;
  applicationsError.value = "";

  try {
    const data = await getApplications();

    applications.value = Array.isArray(data)
      ? data
      : data.applications || [];
  } catch (err) {
    console.error("Error loading applications:", err);
    applicationsError.value = "Unable to load applications.";
  } finally {
    applicationsLoading.value = false;
  }
}

async function handleUpdateApplication(applicationId, status) {
  try {
    const response = await updateApplication(applicationId, { status });

    const updatedApplication = response.application;

    applications.value = applications.value.map((application) =>
      application.id === applicationId
        ? updatedApplication
        : application
    );
  } catch (err) {
    console.error("Error updating application:", err);
    alert("Unable to update application status.");
  }
}

async function handleSaveNotes(application) {
  try {
    await updateApplication(application.id, {
      notes: application.notes || "",
    });

    alert("Application notes saved successfully!");
  } catch (error) {
    console.error("Error saving application notes:", error);
    alert("Failed to save application notes.");
  }
}

async function handleSaveFollowUp(application) {
  try {
    await updateApplication(application.id, {
      follow_up_date: application.follow_up_date || null,
    });

    alert("Follow-up reminder saved successfully!");
  } catch (error) {
    console.error("Error saving follow-up reminder:", error);
    alert("Failed to save follow-up reminder.");
  }
}

async function handleDeleteApplication(applicationId) {
  const confirmed = window.confirm(
    "Are you sure you want to delete this application?"
  );

  if (!confirmed) return;

  try {
    await deleteApplication(applicationId);

    applications.value = applications.value.filter(
      (application) => application.id !== applicationId
    );
  } catch (err) {
    console.error("Error deleting application:", err);
    alert("Unable to delete this application.");
  }
}

function normalize(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/["']/g, "")
    .trim();
}

function calculateMatchScore(job, userProfile) {
  if (!userProfile) {
    return 0;
  }

  let score = 0;

  // 1. Skills Match (60%)
  const userSkills = (userProfile.skills || []).map(normalize);
  const jobSkills = (job.skills || []).map(normalize);

  if (jobSkills.length > 0) {
    const matchingSkills = jobSkills.filter((skill) =>
      userSkills.includes(skill)
    );

    score += (matchingSkills.length / jobSkills.length) * 60;
  }

  // 2. Preferred Role Match (25%)
  const preferredRoles = (
    userProfile.preferred_roles || []
  ).map(normalize);

  const jobTitle = normalize(job.title);

  const roleMatches = preferredRoles.some(
    (role) =>
      role &&
      (jobTitle.includes(role) || role.includes(jobTitle))
  );

  if (roleMatches) {
    score += 25;
  }

  // 3. Location Match (15%)
  const preferredLocations = (
    userProfile.preferred_locations || []
  ).map(normalize);

  const jobLocation = normalize(job.location);

  const locationMatches = preferredLocations.some(
    (location) =>
      location &&
      jobLocation.includes(location)
  );

  if (locationMatches) {
    score += 15;
  }

  return Math.round(score);
}
const matchedJobs = computed(() => {
  return jobs.value.map((job) => ({
    ...job,
    match_score: calculateMatchScore(job, profile.value),
  }));
});

const filteredJobs = computed(() => {
  return (matchedJobs.value || []).filter((job) => {
    const searchText = keyword.value.toLowerCase().trim();
    const searchLocation = location.value.toLowerCase().trim();
    const selectedJobType = jobType.value.toLowerCase().trim();

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

    const matchesJobType =
      !selectedJobType ||
      job.job_type?.toLowerCase().includes(selectedJobType);

    return matchesKeyword && matchesLocation && matchesJobType;
  });
});

const sortedJobs = computed(() => {
  const jobsList = [...filteredJobs.value];

  if (sortBy.value === "match") {
    return jobsList.sort(
      (a, b) => b.match_score - a.match_score
    );
  }

  if (sortBy.value === "match-low") {
    return jobsList.sort(
      (a, b) => a.match_score - b.match_score
    );
  }

  if (sortBy.value === "title") {
    return jobsList.sort((a, b) =>
      a.title.localeCompare(b.title)
    );
  }

  return jobsList;
});

const totalPages = computed(() => {
  return Math.ceil(sortedJobs.value.length / jobsPerPage.value);
});

const paginatedJobs = computed(() => {
  const start = (currentPage.value - 1) * jobsPerPage.value;
  const end = start + jobsPerPage.value;

  return sortedJobs.value.slice(start, end);
});

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
}

function handleNavigate(page) {
  activePage.value = page;

  if (page === "saved-jobs") {
    loadSavedJobs();
  }

  if (page === "applications") {
    loadApplications();
  }
}

function getReminderStatus(dateString) {
  if (!dateString) {
    return "Not Scheduled";
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const followUpDate = new Date(`${dateString}T00:00:00`);

  if (followUpDate < today) {
    return "Overdue";
  }

  if (followUpDate.getTime() === today.getTime()) {
    return "Due Today";
  }

  return "Upcoming";
}
  const overdueReminders = computed(() =>
  applications.value.filter(
    (app) => getReminderStatus(app.follow_up_date) === "Overdue"
  ).length
);

const remindersDueToday = computed(() =>
  applications.value.filter(
    (app) => getReminderStatus(app.follow_up_date) === "Due Today"
  ).length
);

const upcomingReminders = computed(() =>
  applications.value.filter(
    (app) => getReminderStatus(app.follow_up_date) === "Upcoming"
  ).length
);

const applicationStatusCounts = computed(() => {
  const statuses = [
    "Applied",
    "Assessment",
    "Interview",
    "Offer",
    "Rejected",
  ];

  return statuses.map((status) => ({
    status,
    count: applications.value.filter(
      (app) => app.status === status
    ).length,
  }));
});

onMounted(() => {
  loadJobs();
  loadSavedJobs();
});
</script>