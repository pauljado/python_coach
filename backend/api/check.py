"""Solution checking API endpoints."""

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engine.solution_checker import check_solution
from backend.core.dependencies import get_problem_loader
from backend.services.problem_service import ProblemService

router = APIRouter(prefix="/check", tags=["check"])


class CheckRequest(BaseModel):
    code: str
    problem_id: str
    timeout: float = 5.0


@router.post("")
async def check(
    request: CheckRequest,
    loader = Depends(get_problem_loader),
):
    """Check if user's solution is correct."""
    service = ProblemService(loader)
    problem = service.get_problem(request.problem_id)
    
    if problem is None:
        raise HTTPException(status_code=404, detail=f"Problem {request.problem_id} not found")
    
    result = check_solution(request.code, problem, timeout=request.timeout)
    
    return {
        "is_correct": result.is_correct,
        "message": result.message,
        "user_output": result.user_output,
        "expected_output": result.expected_output,
        "details": result.details,
    }
