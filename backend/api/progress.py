"""Progress tracking API endpoints."""

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.core.dependencies import get_progress_manager

router = APIRouter(prefix="/progress", tags=["progress"])


class ProgressUpdate(BaseModel):
    problem_id: str


class HintUpdate(BaseModel):
    problem_id: str
    hint_count: int


@router.get("")
async def get_progress(progress_manager = Depends(get_progress_manager)):
    """Get user progress."""
    completed = progress_manager.get_completed_problems()
    stats = progress_manager.get_stats()
    
    return {
        "completed_problems": list(completed),
        "stats": stats,
    }


@router.post("/complete")
async def mark_completed(
    update: ProgressUpdate,
    progress_manager = Depends(get_progress_manager),
):
    """Mark a problem as completed."""
    progress_manager.mark_completed(update.problem_id)
    return {"status": "success", "problem_id": update.problem_id}


@router.post("/hints")
async def update_hints(
    update: HintUpdate,
    progress_manager = Depends(get_progress_manager),
):
    """Update hint usage for a problem."""
    progress_manager.set_hint_usage(update.problem_id, update.hint_count)
    return {"status": "success"}


@router.delete("")
async def reset_progress(progress_manager = Depends(get_progress_manager)):
    """Reset all progress."""
    progress_manager.reset_progress()
    return {"status": "success"}
