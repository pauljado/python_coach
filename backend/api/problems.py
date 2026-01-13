"""Problems API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from problems import ProblemLoader
from backend.core.dependencies import get_problem_loader
from backend.services.problem_service import ProblemService

router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("")
async def list_problems(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    loader: ProblemLoader = Depends(get_problem_loader),
):
    """List all problems, optionally filtered by category and/or difficulty."""
    service = ProblemService(loader)
    
    if category or difficulty:
        problems = service.filter_problems(category=category, difficulty=difficulty)
    else:
        problems = service.get_all_problems()
    
    return {"problems": problems, "total": len(problems)}


@router.get("/{problem_id}")
async def get_problem(
    problem_id: str,
    loader: ProblemLoader = Depends(get_problem_loader),
):
    """Get a specific problem by ID."""
    service = ProblemService(loader)
    problem = service.get_problem(problem_id)
    
    if problem is None:
        raise HTTPException(status_code=404, detail=f"Problem {problem_id} not found")
    
    return problem
