/** Output Panel component */

"use client";

import { ExecutionResult } from "@/types";
import { Card } from "@/components/ui/Card";
import { CheckCircle, XCircle, Clock } from "lucide-react";

interface OutputPanelProps {
  result: ExecutionResult | null;
  loading?: boolean;
}

export function OutputPanel({ result, loading }: OutputPanelProps) {
  if (loading) {
    return (
      <Card>
        <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-600"></div>
          <span>Executing code...</span>
        </div>
      </Card>
    );
  }

  if (!result) {
    return (
      <Card>
        <p className="text-gray-500 dark:text-gray-400 text-sm">
          Run your code to see output here
        </p>
      </Card>
    );
  }

  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          {result.success ? (
            <>
              <CheckCircle className="w-5 h-5 text-green-600" />
              <span className="font-semibold text-green-600">Execution Successful</span>
            </>
          ) : (
            <>
              <XCircle className="w-5 h-5 text-red-600" />
              <span className="font-semibold text-red-600">Error</span>
            </>
          )}
          <div className="ml-auto flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400">
            <Clock className="w-4 h-4" />
            <span>{result.execution_time.toFixed(3)}s</span>
          </div>
        </div>

        {result.error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <pre className="text-sm text-red-800 dark:text-red-200 whitespace-pre-wrap font-mono">
              {result.error}
            </pre>
          </div>
        )}

        {result.output && (
          <div>
            <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Output:
            </h4>
            <pre className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 text-sm font-mono whitespace-pre-wrap overflow-x-auto">
              {result.output || "(no output)"}
            </pre>
          </div>
        )}
      </div>
    </Card>
  );
}
