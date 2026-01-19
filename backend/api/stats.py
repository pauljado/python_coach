"""Statistics API endpoints."""

from fastapi import APIRouter, Depends
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.core.dependencies import get_problem_loader, get_progress_manager
from backend.services.problem_service import ProblemService

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
async def get_stats(
    loader = Depends(get_problem_loader),
    progress_manager = Depends(get_progress_manager),
):
    """Get statistics about problems and progress."""
    service = ProblemService(loader)
    all_problems = service.get_all_problems()
    completed_ids = progress_manager.get_completed_problems()
    
    # Calculate points
    difficulty_points = {"Beginner": 1, "Intermediate": 2, "Advanced": 4}
    total_points = sum(difficulty_points.get(p.get("difficulty", "Beginner"), 1) for p in all_problems)
    earned_points = sum(
        difficulty_points.get(p.get("difficulty", "Beginner"), 1)
        for p in all_problems
        if p["id"] in completed_ids
    )
    
    # Count by difficulty
    difficulty_counts = {}
    completed_by_difficulty = {}
    for problem in all_problems:
        diff = problem.get("difficulty", "Beginner")
        difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        if problem["id"] in completed_ids:
            completed_by_difficulty[diff] = completed_by_difficulty.get(diff, 0) + 1
    
    # Count by category
    category_counts = {}
    completed_by_category = {}
    for problem in all_problems:
        cat = problem.get("category", "Unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1
        if problem["id"] in completed_ids:
            completed_by_category[cat] = completed_by_category.get(cat, 0) + 1
    
    return {
        "total_problems": len(all_problems),
        "completed_problems": len(completed_ids),
        "total_points": total_points,
        "earned_points": earned_points,
        "difficulty_stats": {
            diff: {
                "total": difficulty_counts.get(diff, 0),
                "completed": completed_by_difficulty.get(diff, 0),
            }
            for diff in ["Beginner", "Intermediate", "Advanced"]
        },
        "category_stats": {
            cat: {
                "total": category_counts.get(cat, 0),
                "completed": completed_by_category.get(cat, 0),
            }
            for cat in category_counts.keys()
        },
    }
