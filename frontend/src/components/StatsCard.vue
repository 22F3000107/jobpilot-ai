<template>
  <div class="card stats-card border-0 shadow-sm h-100">
    <div class="card-body">
      <p class="text-muted mb-2">{{ title }}</p>
      <h2 class="fw-bold mb-0">{{ value }}</h2>
      <small class="text-muted">{{ subtitle }}</small>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  subtitle: String,
});
</script>