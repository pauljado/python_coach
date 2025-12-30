"""Code execution engine module for Python Coach."""

from .code_executor import execute_code
from .solution_checker import check_solution
from .progress_manager import ProgressManager

__all__ = ["execute_code", "check_solution", "ProgressManager"]

