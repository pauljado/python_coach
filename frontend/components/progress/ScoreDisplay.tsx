/** Score Display component */

"use client";

import { useProgressStore } from "@/lib/store/progressStore";
import { useEffect } from "react";

export function ScoreDisplay() {
  const stats = useProgressStore((state) => state.stats);
  const fetchStats = useProgressStore((state) => state.fetchStats);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  if (!stats) return null;

  return (
    <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg shadow-lg">
      <span className="text-xl">⭐</span>
      <div className="flex flex-col">
        <span className="text-xs opacity-90">Points</span>
        <span className="font-bold text-lg leading-none">
          {stats.earned_points} / {stats.total_points}
        </span>
      </div>
    </div>
  );
}
