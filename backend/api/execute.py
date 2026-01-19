"""Code execution API endpoints."""

from pydantic import BaseModel
from fastapi import APIRouter
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engine.code_executor import execute_code

router = APIRouter(prefix="/execute", tags=["execute"])


class ExecuteRequest(BaseModel):
    code: str
    timeout: float = 5.0


@router.post("")
async def execute(request: ExecuteRequest):
    """Execute Python code and return the result."""
    result = execute_code(request.code, timeout=request.timeout)
    
    return {
        "output": result.output,
        "error": result.error,
        "execution_time": result.execution_time,
        "success": result.success,
    }
