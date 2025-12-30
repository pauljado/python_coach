"""Progress manager for persisting user progress locally."""

import json
from pathlib import Path
from typing import Optional


class ProgressManager:
    """Manages saving and loading user progress to/from a local JSON file."""

    def __init__(self, save_file: Optional[str] = None):
        """Initialize the progress manager.
        
        Args:
            save_file: Path to the save file. Defaults to 'progress.json' in user's home.
        """
        if save_file:
            self.save_path = Path(save_file)
        else:
            # Store in the project directory
            self.save_path = Path(__file__).parent.parent / "progress.json"
        
        self._data = self._load()

    def _load(self) -> dict:
        """Load progress from file."""
        if self.save_path.exists():
            try:
                with open(self.save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Ensure completed_problems is a list (for JSON compatibility)
                    if "completed_problems" in data:
                        data["completed_problems"] = set(data["completed_problems"])
                    else:
                        data["completed_problems"] = set()
                    return data
            except (json.JSONDecodeError, IOError):
                return self._default_data()
        return self._default_data()

    def _default_data(self) -> dict:
        """Return default progress data structure."""
        return {
            "completed_problems": set(),
            "hint_usage": {},  # Track hints used per problem
        }

    def save(self) -> bool:
        """Save progress to file.
        
        Returns:
            True if save was successful, False otherwise.
        """
        try:
            # Convert set to list for JSON serialization
            save_data = {
                "completed_problems": list(self._data.get("completed_problems", set())),
                "hint_usage": self._data.get("hint_usage", {}),
            }
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=2)
            return True
        except IOError:
            return False

    def get_completed_problems(self) -> set[str]:
        """Get the set of completed problem IDs."""
        return self._data.get("completed_problems", set())

    def mark_completed(self, problem_id: str) -> None:
        """Mark a problem as completed.
        
        Args:
            problem_id: The ID of the completed problem.
        """
        self._data["completed_problems"].add(problem_id)
        self.save()

    def is_completed(self, problem_id: str) -> bool:
        """Check if a problem is completed.
        
        Args:
            problem_id: The ID of the problem to check.
            
        Returns:
            True if the problem is completed, False otherwise.
        """
        return problem_id in self._data.get("completed_problems", set())

    def get_hint_usage(self, problem_id: str) -> int:
        """Get how many hints have been revealed for a problem.
        
        Args:
            problem_id: The ID of the problem.
            
        Returns:
            Number of hints revealed.
        """
        return self._data.get("hint_usage", {}).get(problem_id, 0)

    def set_hint_usage(self, problem_id: str, count: int) -> None:
        """Set the hint usage count for a problem.
        
        Args:
            problem_id: The ID of the problem.
            count: Number of hints revealed.
        """
        if "hint_usage" not in self._data:
            self._data["hint_usage"] = {}
        self._data["hint_usage"][problem_id] = count
        self.save()

    def reset_progress(self) -> None:
        """Reset all progress."""
        self._data = self._default_data()
        self.save()

    def get_stats(self) -> dict:
        """Get progress statistics.
        
        Returns:
            Dictionary with progress stats.
        """
        completed = self._data.get("completed_problems", set())
        return {
            "total_completed": len(completed),
            "completed_ids": list(completed),
        }

