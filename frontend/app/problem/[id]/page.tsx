/** Problem detail page */

"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Problem, ExecutionResult, CheckResult } from "@/types";
import { problemsApi, executeApi, checkApi } from "@/lib/api/client";
import { useProgressStore } from "@/lib/store/progressStore";
import { ProblemCard } from "@/components/problem/ProblemCard";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { OutputPanel } from "@/components/editor/OutputPanel";
import { ActionButtons } from "@/components/editor/ActionButtons";
import { Header } from "@/components/layout/Header";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { CheckCircle, XCircle, ChevronLeft, ChevronRight } from "lucide-react";
import toast from "react-hot-toast";
import confetti from "canvas-confetti";
import { problemsApi as getAllProblemsApi } from "@/lib/api/client";

export default function ProblemPage() {
  const params = useParams();
  const router = useRouter();
  const problemId = params.id as string;

  const [problem, setProblem] = useState<Problem | null>(null);
  const [allProblems, setAllProblems] = useState<Problem[]>([]);
  const [code, setCode] = useState("");
  const [executionResult, setExecutionResult] = useState<ExecutionResult | null>(null);
  const [checkResult, setCheckResult] = useState<CheckResult | null>(null);
  const [hintIndex, setHintIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [currentProblemIndex, setCurrentProblemIndex] = useState(-1);

  const { completedProblems, markCompleted, updateHints, fetchStats } = useProgressStore();

  useEffect(() => {
    const loadProblem = async () => {
      try {
        const [problemData, allProblemsData] = await Promise.all([
          problemsApi.getById(problemId),
          problemsApi.getAll(),
        ]);
        
        setProblem(problemData);
        setCode(problemData.starter_code || "");
        
        const all = allProblemsData.problems;
        setAllProblems(all);
        const index = all.findIndex((p: Problem) => p.id === problemId);
        setCurrentProblemIndex(index);
      } catch (error) {
        console.error("Failed to load problem:", error);
        toast.error("Failed to load problem");
      }
    };
    loadProblem();
  }, [problemId]);

  const handleRun = async () => {
    if (!code.trim()) {
      toast.error("Please write some code first");
      return;
    }

    setLoading(true);
    setCheckResult(null);
    try {
      const result = await executeApi.execute(code);
      setExecutionResult(result);
      if (result.success) {
        toast.success("Code executed successfully!");
      } else {
        toast.error("Execution failed");
      }
    } catch (error) {
      toast.error("Failed to execute code");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCheck = async () => {
    if (!code.trim()) {
      toast.error("Please write some code first");
      return;
    }

    setLoading(true);
    setExecutionResult(null);
    try {
      const result = await checkApi.check(code, problemId);
      setCheckResult(result);
      
      if (result.is_correct) {
        toast.success("Correct! 🎉");
        await markCompleted(problemId);
        await fetchStats();
        
        // Confetti animation
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 },
        });
      } else {
        toast.error("Not quite right. Keep trying!");
      }
    } catch (error) {
      toast.error("Failed to check solution");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleHint = () => {
    if (!problem) return;
    if (hintIndex < problem.hints.length) {
      setHintIndex(hintIndex + 1);
      updateHints(problemId, hintIndex + 1);
      toast.success("Hint revealed!");
    } else {
      toast("All hints have been revealed", { icon: "💡" });
    }
  };

  const navigateProblem = (direction: "prev" | "next") => {
    if (currentProblemIndex === -1) return;
    
    const newIndex = direction === "next" ? currentProblemIndex + 1 : currentProblemIndex - 1;
    if (newIndex >= 0 && newIndex < allProblems.length) {
      router.push(`/problem/${allProblems[newIndex].id}`);
    }
  };

  if (!problem) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const isCompleted = completedProblems.has(problemId);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <Header />
      
      <main className="max-w-7xl mx-auto p-8 space-y-6">
        <div className="flex items-center justify-between">
          <Button
            variant="ghost"
            onClick={() => router.push("/")}
            className="flex items-center gap-2"
          >
            <ChevronLeft className="w-4 h-4" />
            Back to Problems
          </Button>
          
          <div className="flex gap-2">
            <Button
              variant="ghost"
              onClick={() => navigateProblem("prev")}
              disabled={currentProblemIndex <= 0}
              className="flex items-center gap-2"
            >
              <ChevronLeft className="w-4 h-4" />
              Previous
            </Button>
            <Button
              variant="ghost"
              onClick={() => navigateProblem("next")}
              disabled={currentProblemIndex >= allProblems.length - 1}
              className="flex items-center gap-2"
            >
              Next
              <ChevronRight className="w-4 h-4" />
            </Button>
          </div>
        </div>

        <ProblemCard problem={problem} isCompleted={isCompleted} />

        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Your Code</h3>
            <CodeEditor value={code} onChange={(value) => setCode(value || "")} height="400px" />
          </div>

          <ActionButtons
            onRun={handleRun}
            onCheck={handleCheck}
            onHint={handleHint}
            loading={loading}
          />

          {executionResult && <OutputPanel result={executionResult} />}

          {checkResult && (
            <Card>
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  {checkResult.is_correct ? (
                    <>
                      <CheckCircle className="w-5 h-5 text-green-600" />
                      <span className="font-semibold text-green-600">{checkResult.message}</span>
                    </>
                  ) : (
                    <>
                      <XCircle className="w-5 h-5 text-red-600" />
                      <span className="font-semibold text-red-600">{checkResult.message}</span>
                    </>
                  )}
                </div>

                {checkResult.expected_output && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Your Output:</h4>
                      <pre className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 text-sm font-mono whitespace-pre-wrap">
                        {checkResult.user_output || "(empty)"}
                      </pre>
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Expected Output:</h4>
                      <pre className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 text-sm font-mono whitespace-pre-wrap">
                        {checkResult.expected_output}
                      </pre>
                    </div>
                  </div>
                )}

                {checkResult.details && (
                  <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                    <p className="text-sm text-blue-800 dark:text-blue-200">{checkResult.details}</p>
                  </div>
                )}
              </div>
            </Card>
          )}

          {problem.hints.length > 0 && (
            <Card>
              <h3 className="text-lg font-semibold mb-4">💡 Hints</h3>
              {hintIndex === 0 ? (
                <p className="text-gray-500 dark:text-gray-400 text-sm">
                  Click "Get Hint" to reveal hints
                </p>
              ) : (
                <div className="space-y-2">
                  {problem.hints.slice(0, hintIndex).map((hint, index) => (
                    <div
                      key={index}
                      className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4"
                    >
                      <p className="text-sm font-medium mb-1">Hint {index + 1}:</p>
                      <p className="text-sm text-gray-700 dark:text-gray-300">{hint}</p>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          )}

          {problem.solution && (
            <Card>
              <details className="cursor-pointer">
                <summary className="text-lg font-semibold mb-4">
                  👀 View Solution (Spoiler!)
                </summary>
                <pre className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 text-sm font-mono whitespace-pre-wrap overflow-x-auto">
                  {problem.solution}
                </pre>
              </details>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
}
