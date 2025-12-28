"""Reusable UI components for Python Coach Streamlit app."""

import streamlit as st
from typing import Optional


def render_problem_card(problem: dict) -> None:
    """Render a problem card with title, difficulty, and description."""
    # Header with title and badges
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.markdown(f"### {problem['title']}")

    with col2:
        difficulty = problem["difficulty"]
        difficulty_colors = {
            "Beginner": "🟢",
            "Intermediate": "🟡",
            "Advanced": "🔴",
        }
        st.markdown(f"{difficulty_colors.get(difficulty, '⚪')} **{difficulty}**")

    with col3:
        st.markdown(f"📁 {problem['category']}")

    # Description
    st.markdown("---")
    st.markdown(problem["description"])
    st.markdown("---")


def render_code_editor(starter_code: str, key: str) -> str:
    """
    Render a code editor text area.

    Args:
        starter_code: Initial code to display
        key: Unique key for the text area

    Returns:
        The current code in the editor
    """
    st.markdown("#### 💻 Your Code")

    code = st.text_area(
        label="Code Editor",
        value=starter_code,
        height=300,
        key=key,
        label_visibility="collapsed",
        help="Write your Python code here",
    )

    return code


def render_action_buttons() -> tuple[bool, bool, bool]:
    """
    Render action buttons for running and checking code.

    Returns:
        Tuple of (run_clicked, check_clicked, hint_clicked)
    """
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        run_clicked = st.button("▶️ Run Code", type="secondary", use_container_width=True)

    with col2:
        check_clicked = st.button("✅ Check Solution", type="primary", use_container_width=True)

    with col3:
        hint_clicked = st.button("💡 Get Hint", type="secondary", use_container_width=True)

    with col4:
        pass  # Empty column for spacing

    return run_clicked, check_clicked, hint_clicked


def render_output_area(
    output: str,
    error: Optional[str] = None,
    execution_time: Optional[float] = None,
) -> None:
    """
    Render the output area with execution results.

    Args:
        output: The program output
        error: Any error message
        execution_time: Time taken to execute
    """
    st.markdown("#### 📤 Output")

    if error:
        st.error("❌ Error occurred:")
        st.code(error, language="text")
        if output:
            st.info("Partial output before error:")
            st.code(output, language="text")
    elif output:
        st.success("✅ Execution successful!")
        st.code(output, language="text")
    else:
        st.info("No output produced. Make sure your code prints something!")

    if execution_time is not None:
        st.caption(f"⏱️ Execution time: {execution_time:.4f}s")


def render_check_result(
    is_correct: bool,
    message: str,
    user_output: str,
    expected_output: Optional[str] = None,
    details: Optional[str] = None,
) -> None:
    """
    Render the solution check result.

    Args:
        is_correct: Whether the solution is correct
        message: Main feedback message
        user_output: The user's output
        expected_output: The expected output (if any)
        details: Additional details or hints
    """
    if is_correct:
        st.success(f"🎉 {message}")
        st.balloons()
    else:
        st.error(f"❌ {message}")

    # Show comparison if both outputs are available
    if expected_output:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Your Output:**")
            st.code(user_output if user_output else "(empty)", language="text")

        with col2:
            st.markdown("**Expected Output:**")
            st.code(expected_output, language="text")

    elif user_output:
        st.markdown("**Your Output:**")
        st.code(user_output, language="text")

    if details:
        st.info(f"💡 {details}")


def render_hint_section(hints: list[str], current_hint_index: int) -> None:
    """
    Render the hint section with progressive hints.

    Args:
        hints: List of all hints
        current_hint_index: How many hints to show (0-indexed, exclusive)
    """
    if not hints:
        st.info("No hints available for this problem.")
        return

    st.markdown("#### 💡 Hints")

    if current_hint_index == 0:
        st.info("Click 'Get Hint' to reveal a hint!")
    else:
        for i in range(current_hint_index):
            if i < len(hints):
                with st.expander(f"Hint {i + 1}", expanded=(i == current_hint_index - 1)):
                    st.markdown(hints[i])

        remaining = len(hints) - current_hint_index
        if remaining > 0:
            st.caption(f"📝 {remaining} more hint(s) available")
        else:
            st.caption("✨ All hints revealed!")


def render_sidebar(
    categories: list[str],
    difficulties: list[str],
    problems: list[dict],
    selected_category: str,
    selected_difficulty: str,
) -> tuple[str, str, Optional[str]]:
    """
    Render the sidebar with problem navigation.

    Args:
        categories: List of available categories
        difficulties: List of difficulty levels
        problems: List of all problems
        selected_category: Currently selected category
        selected_difficulty: Currently selected difficulty

    Returns:
        Tuple of (category, difficulty, selected_problem_id)
    """
    st.sidebar.title("🐍 Python Coach")
    st.sidebar.markdown("Learn Python interactively!")
    st.sidebar.markdown("---")

    # Filters
    st.sidebar.markdown("### 🔍 Filter Problems")

    category = st.sidebar.selectbox(
        "Category",
        options=categories,
        index=categories.index(selected_category) if selected_category in categories else 0,
        key="category_select",
    )

    difficulty = st.sidebar.selectbox(
        "Difficulty",
        options=difficulties,
        index=difficulties.index(selected_difficulty) if selected_difficulty in difficulties else 0,
        key="difficulty_select",
    )

    st.sidebar.markdown("---")

    # Filter problems
    filtered_problems = problems
    if category != "All":
        filtered_problems = [p for p in filtered_problems if p["category"] == category]
    if difficulty != "All":
        filtered_problems = [p for p in filtered_problems if p["difficulty"] == difficulty]

    # Problem list
    st.sidebar.markdown(f"### 📚 Problems ({len(filtered_problems)})")

    selected_problem_id = None
    for problem in filtered_problems:
        difficulty_icon = {
            "Beginner": "🟢",
            "Intermediate": "🟡",
            "Advanced": "🔴",
        }.get(problem["difficulty"], "⚪")

        if st.sidebar.button(
            f"{difficulty_icon} {problem['title']}",
            key=f"problem_{problem['id']}",
            use_container_width=True,
        ):
            selected_problem_id = problem["id"]

    return category, difficulty, selected_problem_id


def render_solution_toggle(solution: str) -> None:
    """Render a collapsible section showing the solution."""
    with st.expander("👀 View Solution (Spoiler!)"):
        st.code(solution, language="python")
        st.caption("Try to solve it yourself before looking at the solution!")


def render_welcome_message() -> None:
    """Render a welcome message when no problem is selected."""
    st.markdown(
        """
        # 🐍 Welcome to Python Coach!

        **Learn Python through interactive practice problems.**

        ### How to use:
        1. **Select a problem** from the sidebar on the left
        2. **Read the problem description** carefully
        3. **Write your code** in the editor
        4. **Run your code** to see the output
        5. **Check your solution** to verify it's correct
        6. **Get hints** if you're stuck

        ### Categories available:
        - 📝 **Syntax** - Variables, operators, strings
        - 🔄 **Control Flow** - If/else, loops
        - 🔧 **Functions** - Definition, parameters, return values
        - 📦 **Data Structures** - Lists, dictionaries, tuples, sets
        - 📁 **Data Handling** - Files, JSON, parsing
        - ⚠️ **Exception Handling** - Try/except blocks
        - 🚀 **Advanced** - Comprehensions, decorators, classes

        ---
        *Select a problem from the sidebar to get started!*
        """
    )


def render_progress_indicator(completed: int, total: int) -> None:
    """Render a simple progress indicator."""
    if total > 0:
        progress = completed / total
        st.sidebar.progress(progress)
        st.sidebar.caption(f"Progress: {completed}/{total} problems")

