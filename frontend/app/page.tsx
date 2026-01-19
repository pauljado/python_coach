/** Home/Dashboard page */

"use client";

import { useEffect, useState } from "react";
import { Problem } from "@/types";
import { problemsApi } from "@/lib/api/client";
import { useProgressStore } from "@/lib/store/progressStore";
import { ProblemCard } from "@/components/problem/ProblemCard";
import { Header } from "@/components/layout/Header";
import { Sidebar } from "@/components/layout/Sidebar";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Card } from "@/components/ui/Card";
import Link from "next/link";

export default function HomePage() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [filteredProblems, setFilteredProblems] = useState<Problem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [selectedDifficulty, setSelectedDifficulty] = useState("All");
  const [loading, setLoading] = useState(true);
  
  const { completedProblems, stats, fetchProgress, fetchStats } = useProgressStore();

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await problemsApi.getAll();
        setProblems(data.problems);
        setFilteredProblems(data.problems);
        await fetchProgress();
        await fetchStats();
      } catch (error) {
        console.error("Failed to load problems:", error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [fetchProgress, fetchStats]);

  useEffect(() => {
    let filtered = problems;
    if (selectedCategory !== "All") {
      filtered = filtered.filter((p) => p.category === selectedCategory);
    }
    if (selectedDifficulty !== "All") {
      filtered = filtered.filter((p) => p.difficulty === selectedDifficulty);
    }
    setFilteredProblems(filtered);
  }, [problems, selectedCategory, selectedDifficulty]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <Header />
      
      <div className="flex">
        <Sidebar
          problems={problems}
          selectedCategory={selectedCategory}
          selectedDifficulty={selectedDifficulty}
          onCategoryChange={setSelectedCategory}
          onDifficultyChange={setSelectedDifficulty}
        />
        
        <main className="flex-1 p-8">
          <div className="max-w-7xl mx-auto space-y-6">
            {stats && (
              <Card className="p-6">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-bold">Your Progress</h2>
                    <div className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                      ⭐ {stats.earned_points} / {stats.total_points}
                    </div>
                  </div>
                  <ProgressBar
                    value={(stats.completed_problems / stats.total_problems) * 100}
                    variant="gradient"
                    showLabel
                  />
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {stats.completed_problems} of {stats.total_problems} problems completed
                  </div>
                </div>
              </Card>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredProblems.map((problem) => (
                <Link key={problem.id} href={`/problem/${problem.id}`}>
                  <ProblemCard
                    problem={problem}
                    isCompleted={completedProblems.has(problem.id)}
                  />
                </Link>
              ))}
            </div>

            {filteredProblems.length === 0 && (
              <Card className="p-12 text-center">
                <p className="text-gray-500 dark:text-gray-400">
                  No problems found with the selected filters.
                </p>
              </Card>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
