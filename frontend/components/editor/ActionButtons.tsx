/** Action Buttons component */

"use client";

import { Button } from "@/components/ui/Button";
import { Play, CheckCircle, Lightbulb } from "lucide-react";

interface ActionButtonsProps {
  onRun: () => void;
  onCheck: () => void;
  onHint: () => void;
  loading?: boolean;
}

export function ActionButtons({ onRun, onCheck, onHint, loading }: ActionButtonsProps) {
  return (
    <div className="flex gap-3">
      <Button
        variant="secondary"
        onClick={onRun}
        disabled={loading}
        className="flex items-center gap-2"
      >
        <Play className="w-4 h-4" />
        Run Code
      </Button>
      
      <Button
        variant="primary"
        onClick={onCheck}
        disabled={loading}
        className="flex items-center gap-2"
      >
        <CheckCircle className="w-4 h-4" />
        Check Solution
      </Button>
      
      <Button
        variant="secondary"
        onClick={onHint}
        className="flex items-center gap-2"
      >
        <Lightbulb className="w-4 h-4" />
        Get Hint
      </Button>
    </div>
  );
}
