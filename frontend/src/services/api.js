import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getJobs = async () => {
  const response = await api.get("/jobs/");
  return response.data;
};

export default api;