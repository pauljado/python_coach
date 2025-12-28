"""Code execution engine with timeout protection for Python Coach."""

import sys
import io
import threading
import traceback
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionResult:
    """Result of code execution."""

    output: str
    error: Optional[str]
    execution_time: float
    success: bool


class TimeoutException(Exception):
    """Raised when code execution times out."""

    pass


def execute_code(code: str, timeout: float = 5.0) -> ExecutionResult:
    """
    Execute Python code safely with timeout protection.

    Args:
        code: The Python code to execute
        timeout: Maximum execution time in seconds (default: 5.0)

    Returns:
        ExecutionResult with output, error info, and execution status
    """
    output_capture = io.StringIO()
    error_capture = io.StringIO()
    result = {"output": "", "error": None, "success": False, "execution_time": 0.0}

    def run_code():
        """Inner function to run code in a thread."""
        import time

        start_time = time.time()
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        try:
            sys.stdout = output_capture
            sys.stderr = error_capture

            # Create a restricted global namespace
            exec_globals = {
                "__builtins__": __builtins__,
                "__name__": "__main__",
            }

            # Execute the code
            exec(code, exec_globals)

            result["output"] = output_capture.getvalue()
            result["success"] = True

        except Exception as e:
            result["error"] = f"{type(e).__name__}: {str(e)}"
            result["output"] = output_capture.getvalue()
            # Add traceback for debugging (simplified)
            tb_lines = traceback.format_exc().split("\n")
            # Filter to show relevant lines
            relevant_lines = []
            for line in tb_lines:
                if '<string>' in line or not line.startswith('  File'):
                    relevant_lines.append(line)
            result["error"] = "\n".join(relevant_lines).strip()

        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            result["execution_time"] = time.time() - start_time

    # Run code in a thread with timeout
    thread = threading.Thread(target=run_code)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        # Code is still running - timeout occurred
        return ExecutionResult(
            output=output_capture.getvalue(),
            error=f"Timeout: Code execution exceeded {timeout} seconds. Possible infinite loop?",
            execution_time=timeout,
            success=False,
        )

    return ExecutionResult(
        output=result["output"],
        error=result["error"],
        execution_time=result["execution_time"],
        success=result["success"],
    )


def execute_with_input(code: str, input_data: str = "", timeout: float = 5.0) -> ExecutionResult:
    """
    Execute Python code with simulated input.

    Args:
        code: The Python code to execute
        input_data: Simulated input (newline-separated for multiple inputs)
        timeout: Maximum execution time in seconds

    Returns:
        ExecutionResult with output, error info, and execution status
    """
    # Prepend input handling to the code
    input_lines = input_data.strip().split("\n") if input_data.strip() else []
    input_setup = f"""
import sys
from io import StringIO

_input_data = {input_lines!r}
_input_index = [0]

def _mock_input(prompt=''):
    if prompt:
        print(prompt, end='')
    if _input_index[0] < len(_input_data):
        result = _input_data[_input_index[0]]
        _input_index[0] += 1
        return result
    raise EOFError('No more input available')

input = _mock_input
"""
    modified_code = input_setup + "\n" + code
    return execute_code(modified_code, timeout)

