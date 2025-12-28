"""Problem loader module for managing Python learning problems."""

import json
from pathlib import Path
from typing import Optional


class ProblemLoader:
    """Loads and manages problems from the JSON problem library."""

    def __init__(self):
        self.problems_file = Path(__file__).parent / "problems.json"
        self.problems = self._load_problems()

    def _load_problems(self) -> list[dict]:
        """Load problems from JSON file."""
        if not self.problems_file.exists():
            return []
        with open(self.problems_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_all_problems(self) -> list[dict]:
        """Return all problems."""
        return self.problems

    def get_problem_by_id(self, problem_id: str) -> Optional[dict]:
        """Get a specific problem by its ID."""
        for problem in self.problems:
            if problem["id"] == problem_id:
                return problem
        return None

    def get_problems_by_category(self, category: str) -> list[dict]:
        """Get all problems in a specific category."""
        return [p for p in self.problems if p["category"] == category]

    def get_problems_by_difficulty(self, difficulty: str) -> list[dict]:
        """Get all problems of a specific difficulty level."""
        return [p for p in self.problems if p["difficulty"] == difficulty]

    def filter_problems(
        self, category: Optional[str] = None, difficulty: Optional[str] = None
    ) -> list[dict]:
        """Filter problems by category and/or difficulty."""
        filtered = self.problems
        if category and category != "All":
            filtered = [p for p in filtered if p["category"] == category]
        if difficulty and difficulty != "All":
            filtered = [p for p in filtered if p["difficulty"] == difficulty]
        return filtered


def get_categories() -> list[str]:
    """Return all available problem categories."""
    return [
        "All",
        "Syntax",
        "Control Flow",
        "Functions",
        "Data Structures",
        "Data Handling",
        "Exception Handling",
        "Advanced",
    ]


def get_difficulties() -> list[str]:
    """Return all difficulty levels."""
    return ["All", "Beginner", "Intermediate", "Advanced"]

