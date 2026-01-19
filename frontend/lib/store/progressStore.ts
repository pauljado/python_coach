/** Zustand store for progress management */

import { create } from "zustand";
import { Progress, Stats } from "@/types";
import { progressApi, statsApi } from "@/lib/api/client";

interface ProgressStore {
  completedProblems: Set<string>;
  stats: Stats | null;
  loading: boolean;
  fetchProgress: () => Promise<void>;
  fetchStats: () => Promise<void>;
  markCompleted: (problemId: string) => Promise<void>;
  updateHints: (problemId: string, hintCount: number) => Promise<void>;
  resetProgress: () => Promise<void>;
}

export const useProgressStore = create<ProgressStore>((set, get) => ({
  completedProblems: new Set<string>(),
  stats: null,
  loading: false,

  fetchProgress: async () => {
    set({ loading: true });
    try {
      const data = await progressApi.get();
      set({
        completedProblems: new Set(data.completed_problems || []),
        loading: false,
      });
    } catch (error) {
      console.error("Failed to fetch progress:", error);
      set({ loading: false });
    }
  },

  fetchStats: async () => {
    try {
      const data = await statsApi.get();
      set({ stats: data });
    } catch (error) {
      console.error("Failed to fetch stats:", error);
    }
  },

  markCompleted: async (problemId: string) => {
    try {
      await progressApi.markComplete(problemId);
      set((state) => {
        const newSet = new Set(state.completedProblems);
        newSet.add(problemId);
        return { completedProblems: newSet };
      });
      // Refresh stats
      get().fetchStats();
    } catch (error) {
      console.error("Failed to mark problem as completed:", error);
    }
  },

  updateHints: async (problemId: string, hintCount: number) => {
    try {
      await progressApi.updateHints(problemId, hintCount);
    } catch (error) {
      console.error("Failed to update hints:", error);
    }
  },

  resetProgress: async () => {
    try {
      await progressApi.reset();
      set({
        completedProblems: new Set<string>(),
        stats: null,
      });
      get().fetchStats();
    } catch (error) {
      console.error("Failed to reset progress:", error);
    }
  },
}));
