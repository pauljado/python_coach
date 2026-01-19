"""Problem service layer."""

from typing import Optional
from problems import ProblemLoader


class ProblemService:
    """Service for managing problems."""
    
    def __init__(self, loader: ProblemLoader):
        self.loader = loader
    
    def get_all_problems(self):
        """Get all problems."""
        return self.loader.get_all_problems()
    
    def get_problem(self, problem_id: str):
        """Get a specific problem by ID."""
        return self.loader.get_problem_by_id(problem_id)
    
    def filter_problems(
        self,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ):
        """Filter problems by category and/or difficulty."""
        return self.loader.filter_problems(category=category, difficulty=difficulty)
