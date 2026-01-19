/** Sidebar component */

"use client";

import { Problem } from "@/types";
import { Badge } from "@/components/ui/Badge";
import { useProgressStore } from "@/lib/store/progressStore";
import { Check } from "lucide-react";
import Link from "next/link";

interface SidebarProps {
  problems: Problem[];
  selectedCategory?: string;
  selectedDifficulty?: string;
  onCategoryChange?: (category: string) => void;
  onDifficultyChange?: (difficulty: string) => void;
}

const categories = ["All", "Syntax", "Control Flow", "Functions", "Data Structures", "Data Handling", "Exception Handling", "Advanced"];
const difficulties = ["All", "Beginner", "Intermediate", "Advanced"];

const difficultyColors = {
  Beginner: "success",
  Intermediate: "warning",
  Advanced: "danger",
} as const;

const difficultyIcons = {
  Beginner: "🟢",
  Intermediate: "🟡",
  Advanced: "🔴",
};

export function Sidebar({
  problems,
  selectedCategory = "All",
  selectedDifficulty = "All",
  onCategoryChange,
  onDifficultyChange,
}: SidebarProps) {
  const completedProblems = useProgressStore((state) => state.completedProblems);
  
  const filteredProblems = problems.filter((p) => {
    if (selectedCategory !== "All" && p.category !== selectedCategory) return false;
    if (selectedDifficulty !== "All" && p.difficulty !== selectedDifficulty) return false;
    return true;
  });

  return (
    <aside className="w-64 h-screen bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 overflow-y-auto">
      <div className="p-4 space-y-4">
        <div>
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Category
          </h2>
          <select
            value={selectedCategory}
            onChange={(e) => onCategoryChange?.(e.target.value)}
            className="w-full px-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-sm"
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>

        <div>
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Difficulty
          </h2>
          <select
            value={selectedDifficulty}
            onChange={(e) => onDifficultyChange?.(e.target.value)}
            className="w-full px-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-sm"
          >
            {difficulties.map((diff) => (
              <option key={diff} value={diff}>
                {diff}
              </option>
            ))}
          </select>
        </div>

        <div>
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Problems ({filteredProblems.length})
          </h2>
          <div className="space-y-1">
            {filteredProblems.map((problem) => {
              const isCompleted = completedProblems.has(problem.id);
              return (
                <Link
                  key={problem.id}
                  href={`/problem/${problem.id}`}
                  className="block p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors text-sm"
                >
                  <div className="flex items-center gap-2">
                    {isCompleted && <Check className="w-4 h-4 text-green-600 flex-shrink-0" />}
                    <span className="text-xs">{difficultyIcons[problem.difficulty]}</span>
                    <span className="flex-1 truncate">{problem.title}</span>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </aside>
  );
}
