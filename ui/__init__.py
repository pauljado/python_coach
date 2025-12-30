"""UI components module for Python Coach."""

from .components import (
    render_problem_card,
    render_code_editor,
    render_output_area,
    render_hint_section,
    render_sidebar,
    render_score_header,
    render_progress_section,
    get_problem_points,
    calculate_total_points,
    calculate_earned_points,
    DIFFICULTY_POINTS,
)

__all__ = [
    "render_problem_card",
    "render_code_editor",
    "render_output_area",
    "render_hint_section",
    "render_sidebar",
    "render_score_header",
    "render_progress_section",
    "get_problem_points",
    "calculate_total_points",
    "calculate_earned_points",
    "DIFFICULTY_POINTS",
]

