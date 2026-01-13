/** TypeScript type definitions for Python Coach */

export interface Problem {
  id: string;
  title: string;
  difficulty: "Beginner" | "Intermediate" | "Advanced";
  category: string;
  description: string;
  starter_code: string;
  hints: string[];
  solution: string;
  expected_output?: string;
  test_cases?: any[];
}

export interface ExecutionResult {
  output: string;
  error: string | null;
  execution_time: number;
  success: boolean;
}

export interface CheckResult {
  is_correct: boolean;
  message: string;
  user_output: string;
  expected_output: string | null;
  details: string | null;
}

export interface Progress {
  completed_problems: string[];
  stats: {
    total_completed: number;
    completed_ids: string[];
  };
}

export interface Stats {
  total_problems: number;
  completed_problems: number;
  total_points: number;
  earned_points: number;
  difficulty_stats: {
    [key: string]: {
      total: number;
      completed: number;
    };
  };
  category_stats: {
    [key: string]: {
      total: number;
      completed: number;
    };
  };
}
