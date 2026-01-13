# Python Coach Backend

FastAPI backend for Python Coach learning platform.

## Setup

Install dependencies:

```bash
uv pip install -r requirements.txt
```

Or if you prefer pip:

```bash
pip install -r requirements.txt
```

## Running

From the project root:

```bash
python backend/run.py
```

Or:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

API documentation at `http://localhost:8000/docs`
