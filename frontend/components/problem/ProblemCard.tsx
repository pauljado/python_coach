/** Problem Card component */

"use client";

import { Problem } from "@/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Check } from "lucide-react";

interface ProblemCardProps {
  problem: Problem;
  isCompleted?: boolean;
}

const difficultyColors = {
  Beginner: "success",
  Intermediate: "warning",
  Advanced: "danger",
} as const;

export function ProblemCard({ problem, isCompleted = false }: ProblemCardProps) {
  return (
    <Card className="space-y-4">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            {isCompleted && (
              <Check className="w-5 h-5 text-green-600 flex-shrink-0" />
            )}
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              {problem.title}
            </h2>
          </div>
          
          <div className="flex flex-wrap gap-2">
            <Badge variant={difficultyColors[problem.difficulty]}>
              {problem.difficulty}
            </Badge>
            <Badge variant="info">{problem.category}</Badge>
          </div>
        </div>
      </div>

      <div className="prose dark:prose-invert max-w-none">
        <div className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
          {problem.description}
        </div>
      </div>
    </Card>
  );
}
