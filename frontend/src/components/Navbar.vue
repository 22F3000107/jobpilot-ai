<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 py-3">
    <a
      class="navbar-brand fw-bold fs-4"
      href="#"
      @click.prevent="$emit('navigate', 'dashboard')"
    >
      JobPilot <span class="text-info">AI</span>
    </a>

    <div class="ms-auto d-flex gap-3 flex-wrap">
      <button
        class="nav-link text-white"
        @click="$emit('navigate', 'dashboard')"
      >
        Dashboard
      </button>

      <button
        class="nav-link text-white"
        @click="$emit('navigate', 'dashboard')"
      >
        Find Jobs
      </button>

      <button
        class="nav-link text-white"
        @click="$emit('navigate', 'saved-jobs')"
      >
        Saved Jobs
      </button>

      <button
        class="nav-link text-white"
        @click="$emit('navigate', 'applications')"
      >
        Applications
      </button>

      <button
        class="nav-link text-info fw-semibold"
        @click="$emit('navigate', 'profile')"
      >
        My Profile
      </button>
    </div>
  </nav>
</template>

<script setup>
defineEmits(["navigate"]);
</script>