<template>
  <div class="container py-4">
    <div class="card border-0 shadow-sm profile-card">
      <div class="card-body p-4 p-md-5">

        <div class="mb-4">
          <p class="text-primary fw-semibold mb-2">
            PERSONALIZE YOUR JOB SEARCH
          </p>
          <h2 class="fw-bold">My Career Profile</h2>
          <p class="text-muted">
            Tell JobPilot AI about your skills and career goals.
          </p>
        </div>

        <form @submit.prevent="handleSave">

          <!-- Personal Information -->
          <h5 class="fw-bold mb-3">Personal Information</h5>

          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <label class="form-label">Full Name *</label>
              <input
                v-model="form.full_name"
                type="text"
                class="form-control"
                placeholder="Enter your full name"
                required
              />
            </div>

            <div class="col-md-6">
              <label class="form-label">Email Address *</label>
              <input
                v-model="form.email"
                type="email"
                class="form-control"
                placeholder="Enter your email"
                required
              />
            </div>
          </div>

          <!-- Education -->
          <h5 class="fw-bold mb-3">Education</h5>

          <div class="mb-4">
            <label class="form-label">Education Details</label>
            <input
              v-model="form.education"
              type="text"
              class="form-control"
              placeholder="e.g. BS Data Science, IIT Madras"
            />
          </div>

          <!-- Skills -->
          <h5 class="fw-bold mb-3">Skills</h5>

          <div class="mb-4">
            <label class="form-label">
              Skills (separate with commas)
            </label>
            <textarea
              v-model="skillsText"
              class="form-control"
              rows="3"
              placeholder="Python, SQL, Flask, Machine Learning"
            ></textarea>
          </div>

          <!-- Preferred Roles -->
          <h5 class="fw-bold mb-3">Career Preferences</h5>

          <div class="mb-3">
            <label class="form-label">
              Preferred Job Roles (separate with commas)
            </label>
            <textarea
              v-model="rolesText"
              class="form-control"
              rows="2"
              placeholder="Data Analyst, Data Scientist, Business Analyst"
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">
              Preferred Locations (separate with commas)
            </label>
            <input
              v-model="locationsText"
              type="text"
              class="form-control"
              placeholder="Bengaluru, Remote"
            />
          </div>

          <div class="mb-4">
            <label class="form-label">Experience Level</label>
            <select
              v-model="form.experience_level"
              class="form-select"
            >
              <option value="">Select experience level</option>
              <option value="Internship">Internship</option>
              <option value="Fresher">Fresher</option>
              <option value="0-1 years">0-1 years</option>
              <option value="1-3 years">1-3 years</option>
              <option value="3+ years">3+ years</option>
            </select>
          </div>

          <!-- Status Messages -->
          <div v-if="successMessage" class="alert alert-success">
            {{ successMessage }}
          </div>

          <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
          </div>

          <!-- Submit -->
          <button
            type="submit"
            class="btn btn-primary px-4 py-2"
            :disabled="saving"
          >
            {{ saving ? "Saving..." : "Save Profile" }}
          </button>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { getProfile, saveProfile } from "../services/api";

const form = reactive({
  full_name: "",
  email: "",
  education: "",
  experience_level: "",
});

const skillsText = ref("");
const rolesText = ref("");
const locationsText = ref("");

const saving = ref(false);
const successMessage = ref("");
const errorMessage = ref("");

function toList(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

async function loadProfile() {
  try {
    const profile = await getProfile();

    form.full_name = profile.full_name || "";
    form.email = profile.email || "";
    form.education = profile.education || "";
    form.experience_level = profile.experience_level || "";

    skillsText.value = (profile.skills || []).join(", ");
    rolesText.value = (profile.preferred_roles || []).join(", ");
    locationsText.value = (profile.preferred_locations || []).join(", ");
  } catch (error) {
    if (error.response?.status !== 404) {
      errorMessage.value = "Unable to load your profile.";
    }
  }
}

async function handleSave() {
  saving.value = true;
  successMessage.value = "";
  errorMessage.value = "";

  const profileData = {
    ...form,
    skills: toList(skillsText.value),
    preferred_roles: toList(rolesText.value),
    preferred_locations: toList(locationsText.value),
  };

  try {
    const response = await saveProfile(profileData);

    successMessage.value = response.message || "Profile saved successfully!";
  } catch (error) {
    errorMessage.value =
      error.response?.data?.error || "Unable to save profile. Please try again.";
  } finally {
    saving.value = false;
  }
}

onMounted(() => {
  loadProfile();
});
</script>