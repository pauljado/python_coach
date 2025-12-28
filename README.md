# Python Coach

An interactive Python learning platform built with Streamlit. Learn Python through hands-on practice problems with progressive hints and instant solution checking.

## Features

- **40+ Practice Problems** - From basic syntax to advanced concepts
- **Interactive Code Editor** - Write and run Python code in your browser
- **Instant Feedback** - Check your solutions against expected outputs
- **Progressive Hints** - Get help when you're stuck without revealing the full solution
- **Multiple Categories**:
  - Syntax - Variables, operators, strings
  - Control Flow - If/else, loops, break/continue
  - Functions - Parameters, return values, recursion
  - Data Structures - Lists, dictionaries, tuples, sets
  - Data Handling - Files, JSON, parsing
  - Exception Handling - Try/except blocks
  - Advanced - Comprehensions, decorators, classes, generators

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or using uv:

```bash
uv sync
```

## Running the Application

Start the Streamlit app:

```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`.

## Usage

1. **Select a Problem** - Use the sidebar to browse problems by category or difficulty
2. **Read the Description** - Understand what the problem is asking
3. **Write Your Code** - Use the code editor to write your solution
4. **Run Your Code** - Click "Run Code" to see the output
5. **Check Solution** - Click "Check Solution" to verify correctness
6. **Get Hints** - Click "Get Hint" if you need help (hints are revealed progressively)
7. **View Solution** - If you're really stuck, expand the solution section

## Project Structure

```
python_coach/
├── main.py                 # Streamlit app entry point
├── problems/
│   ├── __init__.py
│   ├── problems.json       # Problem library
│   └── problem_loader.py   # Problem management
├── engine/
│   ├── __init__.py
│   ├── code_executor.py    # Safe code execution
│   └── solution_checker.py # Solution validation
├── ui/
│   ├── __init__.py
│   └── components.py       # UI components
├── pyproject.toml
└── README.md
```

## Adding New Problems

Problems are defined in `problems/problems.json`. Each problem has:

```json
{
  "id": "unique_id",
  "title": "Problem Title",
  "difficulty": "Beginner|Intermediate|Advanced",
  "category": "Syntax|Control Flow|Functions|...",
  "description": "Problem description...",
  "starter_code": "# Initial code template\n",
  "hints": ["Hint 1", "Hint 2", "Hint 3"],
  "solution": "# Reference solution code",
  "expected_output": "Expected output\n"
}
```

## Security Note

This application uses Python's `exec()` to run user code. It includes basic timeout protection but is intended for local/educational use. For production deployment, consider implementing additional sandboxing.

## License

MIT License

