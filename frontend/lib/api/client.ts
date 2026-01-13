/** API client for backend communication */

import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Problems API
export const problemsApi = {
  getAll: async (category?: string, difficulty?: string) => {
    const params = new URLSearchParams();
    if (category) params.append("category", category);
    if (difficulty) params.append("difficulty", difficulty);
    const response = await client.get(`/problems?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await client.get(`/problems/${id}`);
    return response.data;
  },
};

// Execute API
export const executeApi = {
  execute: async (code: string, timeout: number = 5.0) => {
    const response = await client.post("/execute", { code, timeout });
    return response.data;
  },
};

// Check API
export const checkApi = {
  check: async (code: string, problemId: string, timeout: number = 5.0) => {
    const response = await client.post("/check", { code, problem_id: problemId, timeout });
    return response.data;
  },
};

// Progress API
export const progressApi = {
  get: async () => {
    const response = await client.get("/progress");
    return response.data;
  },
  markComplete: async (problemId: string) => {
    const response = await client.post("/progress/complete", { problem_id: problemId });
    return response.data;
  },
  updateHints: async (problemId: string, hintCount: number) => {
    const response = await client.post("/progress/hints", {
      problem_id: problemId,
      hint_count: hintCount,
    });
    return response.data;
  },
  reset: async () => {
    const response = await client.delete("/progress");
    return response.data;
  },
};

// Stats API
export const statsApi = {
  get: async () => {
    const response = await client.get("/stats");
    return response.data;
  },
};
