"""Python Coach - Interactive Python Learning Platform.

A Streamlit-based web application for teaching Python through
interactive coding problems with hints and solution checking.
"""

import streamlit as st

from problems import ProblemLoader, get_categories, get_difficulties
from engine import check_solution, ProgressManager
from engine.code_executor import execute_code
from ui.components import (
    render_problem_card,
    render_code_editor,
    render_action_buttons,
    render_output_area,
    render_check_result,
    render_hint_section,
    render_sidebar,
    render_solution_toggle,
    render_welcome_message,
    render_score_header,
    render_progress_section,
    calculate_total_points,
    calculate_earned_points,
)

# Page configuration
st.set_page_config(
    page_title="Python Coach",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Code editor styling */
    .stTextArea textarea {
        font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
    }

    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 1rem;
    }

    /* Problem card styling */
    .problem-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Output area styling */
    .stCode {
        border-radius: 8px;
    }

    /* Success/error message styling */
    .stSuccess, .stError, .stInfo {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize session state variables."""
    if "problem_loader" not in st.session_state:
        st.session_state.problem_loader = ProblemLoader()

    # Initialize progress manager and load saved progress
    if "progress_manager" not in st.session_state:
        st.session_state.progress_manager = ProgressManager()

    if "current_problem_id" not in st.session_state:
        st.session_state.current_problem_id = None

    if "current_code" not in st.session_state:
        st.session_state.current_code = {}

    if "hint_index" not in st.session_state:
        # Load hint usage from saved progress
        st.session_state.hint_index = {}
        pm = st.session_state.progress_manager
        for problem_id in pm.get_completed_problems():
            saved_hints = pm.get_hint_usage(problem_id)
            if saved_hints > 0:
                st.session_state.hint_index[problem_id] = saved_hints

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "All"

    if "selected_difficulty" not in st.session_state:
        st.session_state.selected_difficulty = "All"

    if "execution_result" not in st.session_state:
        st.session_state.execution_result = None

    if "check_result" not in st.session_state:
        st.session_state.check_result = None

    # Load completed problems from saved progress
    if "completed_problems" not in st.session_state:
        st.session_state.completed_problems = st.session_state.progress_manager.get_completed_problems()

    if "reset_counter" not in st.session_state:
        st.session_state.reset_counter = {}


def get_current_code(problem_id: str, starter_code: str) -> str:
    """Get the current code for a problem, or return starter code."""
    if problem_id not in st.session_state.current_code:
        st.session_state.current_code[problem_id] = starter_code
    return st.session_state.current_code[problem_id]


def get_hint_index(problem_id: str) -> int:
    """Get the current hint index for a problem."""
    if problem_id not in st.session_state.hint_index:
        st.session_state.hint_index[problem_id] = 0
    return st.session_state.hint_index[problem_id]


def main():
    """Main application entry point."""
    initialize_session_state()

    loader = st.session_state.problem_loader
    problems = loader.get_all_problems()
    completed_ids = st.session_state.completed_problems

    # Calculate and render score header
    total_points = calculate_total_points(problems)
    earned_points = calculate_earned_points(problems, completed_ids)
    render_score_header(earned_points, total_points)

    # Render sidebar and get selections
    category, difficulty, clicked_problem_id = render_sidebar(
        categories=get_categories(),
        difficulties=get_difficulties(),
        problems=problems,
        selected_category=st.session_state.selected_category,
        selected_difficulty=st.session_state.selected_difficulty,
        completed_problem_ids=completed_ids,
    )

    # Render progress section with reset button
    reset_clicked = render_progress_section(
        earned_points=earned_points,
        total_points=total_points,
        completed_count=len(completed_ids),
        total_problems=len(problems),
    )

    # Handle reset progress
    if reset_clicked:
        st.session_state.progress_manager.reset_progress()
        st.session_state.completed_problems = set()
        st.session_state.hint_index = {}
        st.session_state.current_code = {}
        st.session_state.execution_result = None
        st.session_state.check_result = None
        st.rerun()

    # Update session state with filter selections
    st.session_state.selected_category = category
    st.session_state.selected_difficulty = difficulty

    # Update current problem if one was clicked
    if clicked_problem_id:
        st.session_state.current_problem_id = clicked_problem_id
        st.session_state.execution_result = None
        st.session_state.check_result = None
        st.rerun()

    # Get current problem
    current_problem_id = st.session_state.current_problem_id
    current_problem = loader.get_problem_by_id(current_problem_id) if current_problem_id else None

    # Main content area
    if current_problem is None:
        render_welcome_message()
    else:
        render_problem_view(current_problem)


def get_reset_counter(problem_id: str) -> int:
    """Get the reset counter for a problem (used to force code editor refresh)."""
    if problem_id not in st.session_state.reset_counter:
        st.session_state.reset_counter[problem_id] = 0
    return st.session_state.reset_counter[problem_id]


def render_problem_view(problem: dict):
    """Render the problem view with editor and controls."""
    problem_id = problem["id"]
    is_completed = problem_id in st.session_state.completed_problems

    # Problem card
    render_problem_card(problem, is_completed=is_completed)

    # Code editor
    starter_code = problem.get("starter_code", "# Write your code here\n")
    current_code = get_current_code(problem_id, starter_code)
    reset_count = get_reset_counter(problem_id)

    # Use reset_count in key to force re-render when reset is clicked
    code = render_code_editor(
        starter_code=current_code,
        key=f"code_editor_{problem_id}_{reset_count}",
    )

    # Update stored code
    st.session_state.current_code[problem_id] = code

    # Action buttons
    run_clicked, check_clicked, hint_clicked = render_action_buttons()

    # Handle button clicks
    if run_clicked:
        handle_run_code(code)

    if check_clicked:
        handle_check_solution(code, problem)

    if hint_clicked:
        handle_hint_click(problem_id, len(problem.get("hints", [])))

    # Display results
    st.markdown("---")

    # Show execution result
    if st.session_state.execution_result:
        result = st.session_state.execution_result
        render_output_area(
            output=result.output,
            error=result.error,
            execution_time=result.execution_time,
        )

    # Show check result
    if st.session_state.check_result:
        result = st.session_state.check_result
        render_check_result(
            is_correct=result.is_correct,
            message=result.message,
            user_output=result.user_output,
            expected_output=result.expected_output,
            details=result.details,
        )

    # Hints section
    st.markdown("---")
    current_hint_idx = get_hint_index(problem_id)
    render_hint_section(problem.get("hints", []), current_hint_idx)

    # Solution toggle (at the bottom)
    st.markdown("---")
    if problem.get("solution"):
        render_solution_toggle(problem["solution"])

    # Reset button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🔄 Reset Code", type="secondary"):
            # Reset code to starter code
            st.session_state.current_code[problem_id] = starter_code
            st.session_state.execution_result = None
            st.session_state.check_result = None
            st.session_state.hint_index[problem_id] = 0
            # Increment reset counter to force editor re-render with new key
            st.session_state.reset_counter[problem_id] = reset_count + 1
            st.rerun()

    with col2:
        if st.button("🗑️ Clear Output", type="secondary"):
            st.session_state.execution_result = None
            st.session_state.check_result = None
            st.rerun()


def handle_run_code(code: str):
    """Handle the Run Code button click."""
    st.session_state.check_result = None
    result = execute_code(code)
    st.session_state.execution_result = result


def handle_check_solution(code: str, problem: dict):
    """Handle the Check Solution button click."""
    st.session_state.execution_result = None
    result = check_solution(code, problem)
    st.session_state.check_result = result

    # Track completed problems and save to file
    if result.is_correct:
        problem_id = problem["id"]
        st.session_state.completed_problems.add(problem_id)
        # Save progress to file
        st.session_state.progress_manager.mark_completed(problem_id)


def handle_hint_click(problem_id: str, total_hints: int):
    """Handle the Get Hint button click."""
    current_idx = get_hint_index(problem_id)
    if current_idx < total_hints:
        new_idx = current_idx + 1
        st.session_state.hint_index[problem_id] = new_idx
        # Save hint usage
        st.session_state.progress_manager.set_hint_usage(problem_id, new_idx)


if __name__ == "__main__":
    main()
