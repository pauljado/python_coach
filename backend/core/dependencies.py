"""FastAPI dependencies."""

import sys
from pathlib import Path

# Add parent directory to path to import existing modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from problems import ProblemLoader
from engine.progress_manager import ProgressManager

# Singleton instances
_problem_loader: ProblemLoader | None = None
_progress_manager: ProgressManager | None = None


def get_problem_loader() -> ProblemLoader:
    """Get or create ProblemLoader instance."""
    global _problem_loader
    if _problem_loader is None:
        _problem_loader = ProblemLoader()
    return _problem_loader


def get_progress_manager() -> ProgressManager:
    """Get or create ProgressManager instance."""
    global _progress_manager
    if _progress_manager is None:
        _progress_manager = ProgressManager()
    return _progress_manager
