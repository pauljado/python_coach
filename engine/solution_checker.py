"""Solution checker module for validating user code against expected solutions."""

from dataclasses import dataclass
from typing import Optional
from .code_executor import execute_code, ExecutionResult


@dataclass
class CheckResult:
    """Result of solution checking."""

    is_correct: bool
    message: str
    user_output: str
    expected_output: Optional[str]
    details: Optional[str] = None


def normalize_output(output: str) -> str:
    """Normalize output for comparison (strip trailing whitespace per line, normalize newlines)."""
    lines = output.strip().split("\n")
    return "\n".join(line.rstrip() for line in lines)


def check_solution(
    user_code: str,
    problem: dict,
    timeout: float = 5.0,
) -> CheckResult:
    """
    Check if user's solution is correct.

    Args:
        user_code: The user's submitted code
        problem: The problem dictionary containing expected output/test cases
        timeout: Execution timeout in seconds

    Returns:
        CheckResult with correctness status and feedback
    """
    # Execute user's code
    result = execute_code(user_code, timeout)

    # If execution failed, return error feedback
    if not result.success:
        return CheckResult(
            is_correct=False,
            message="Your code encountered an error.",
            user_output=result.output,
            expected_output=problem.get("expected_output", ""),
            details=result.error,
        )

    # Check against expected output if provided
    expected_output = problem.get("expected_output")
    if expected_output:
        normalized_user = normalize_output(result.output)
        normalized_expected = normalize_output(expected_output)

        if normalized_user == normalized_expected:
            return CheckResult(
                is_correct=True,
                message="Correct! Your solution produces the expected output.",
                user_output=result.output,
                expected_output=expected_output,
            )
        else:
            return CheckResult(
                is_correct=False,
                message="Not quite right. Your output doesn't match the expected output.",
                user_output=result.output,
                expected_output=expected_output,
                details=_generate_diff_hint(normalized_user, normalized_expected),
            )

    # Check test cases if provided
    test_cases = problem.get("test_cases", [])
    if test_cases:
        return _check_test_cases(user_code, test_cases, result, timeout)

    # If no expected output or test cases, just check that code runs
    if result.success and result.output:
        return CheckResult(
            is_correct=True,
            message="Your code runs successfully and produces output!",
            user_output=result.output,
            expected_output=None,
            details="Note: This problem doesn't have strict output checking.",
        )

    return CheckResult(
        is_correct=True,
        message="Your code runs without errors!",
        user_output=result.output,
        expected_output=None,
    )


def _check_test_cases(
    user_code: str,
    test_cases: list,
    initial_result: ExecutionResult,
    timeout: float,
) -> CheckResult:
    """Check user code against test cases."""
    for i, test_case in enumerate(test_cases):
        check_type = test_case.get("check_type", "output")

        if check_type == "variable_exists":
            # Check if specific variables exist in the code
            variables = test_case.get("variables", [])
            missing = []
            for var in variables:
                if var not in user_code:
                    missing.append(var)
            
            if missing:
                return CheckResult(
                    is_correct=False,
                    message=f"Missing required variable(s): {', '.join(missing)}",
                    user_output=initial_result.output,
                    expected_output=None,
                    details="Make sure you've created all the required variables.",
                )

        elif check_type == "output":
            expected = test_case.get("expected", "")
            if normalize_output(initial_result.output) != normalize_output(expected):
                return CheckResult(
                    is_correct=False,
                    message=f"Test case {i + 1} failed.",
                    user_output=initial_result.output,
                    expected_output=expected,
                )

    return CheckResult(
        is_correct=True,
        message="All test cases passed!",
        user_output=initial_result.output,
        expected_output=None,
    )


def _generate_diff_hint(user_output: str, expected_output: str) -> str:
    """Generate a helpful hint about the difference between outputs."""
    user_lines = user_output.split("\n")
    expected_lines = expected_output.split("\n")

    if len(user_lines) != len(expected_lines):
        return f"Your output has {len(user_lines)} line(s), but expected {len(expected_lines)} line(s)."

    for i, (user_line, expected_line) in enumerate(zip(user_lines, expected_lines)):
        if user_line != expected_line:
            return f"Line {i + 1} differs. Got '{user_line}', expected '{expected_line}'."

    return "Check for extra whitespace or formatting differences."


def run_code_only(user_code: str, timeout: float = 5.0) -> ExecutionResult:
    """
    Just run the code without checking against expected output.

    Args:
        user_code: The code to execute
        timeout: Execution timeout

    Returns:
        ExecutionResult with output and any errors
    """
    return execute_code(user_code, timeout)

