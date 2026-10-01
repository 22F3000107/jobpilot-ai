import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// ==================== JOBS API ====================

export const getJobs = async (keyword = "data analyst", location = "Bengaluru") => {
  const response = await api.get("/jobs/", {
    params: {
      keyword,
      location,
    },
  });

  return response.data;
};

// ==================== PROFILE API ====================

export const getProfile = async () => {
  const response = await api.get("/profile/");
  return response.data;
};

export const saveProfile = async (profileData) => {
  const response = await api.post("/profile/", profileData);
  return response.data;
};

// ==================== SAVED JOBS API ====================

export const getSavedJobs = async () => {
  const response = await api.get("/saved-jobs/");
  return response.data;
};

export const saveJob = async (jobData) => {
  const response = await api.post("/saved-jobs/", jobData);
  return response.data;
};

export const deleteSavedJob = async (savedJobId) => {
  const response = await api.delete(`/saved-jobs/${savedJobId}`);
  return response.data;
};

// ==================== APPLICATIONS API ====================

// Get all applications
export const getApplications = async () => {
  const response = await api.get("/applications/");
  return response.data;
};

// Add a job to the application tracker
export const createApplication = async (applicationData) => {
  const response = await api.post("/applications/", applicationData);
  return response.data;
};

// Update application status or notes
export const updateApplication = async (applicationId, data) => {
  const response = await api.patch(
    `/applications/${applicationId}`,
    data
  );
  return response.data;
};

// Delete an application
export const deleteApplication = async (applicationId) => {
  const response = await api.delete(
    `/applications/${applicationId}`
  );
  return response.data;
};

export default api;