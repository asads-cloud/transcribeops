const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function createJob() {
  const response = await fetch(`${API_BASE_URL}/jobs`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to create job");
  }

  return response.json();
}

export async function uploadFile(jobId, file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/upload-local`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload file");
  }

  return response.json();
}

export async function getJob(jobId) {
  const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch job status");
  }

  return response.json();
}

export async function getTranscript(jobId) {
  const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/transcript`);

  if (!response.ok) {
    throw new Error("Transcript is not available yet");
  }

  return response.text();
}