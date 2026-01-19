# Quick Start Guide

## Starting the Application

### 1. Start the Backend

**Important:** Run from the **project root** directory (not from inside `backend`).

In one terminal:

```bash
# From project root directory
uv pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

Or using uv run:

```bash
uv pip install -r backend/requirements.txt
uv run uvicorn backend.main:app --reload --port 8000
```

Or use the run script (also from project root):

```bash
python backend/run.py
```

The backend API will run at `http://localhost:8000`

**Verify it's working:** Open http://localhost:8000/docs in your browser to see the API documentation.

### 2. Start the Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will run at `http://localhost:3000`

## Accessing the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Environment Setup

The frontend expects the backend to be running at `http://localhost:8000/api` by default.

If you need to change this, create a `.env.local` file in the `frontend` directory:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Testing

See `TESTING.md` for detailed testing instructions and troubleshooting.

## Quick Test

1. Start backend (terminal 1): `python -m uvicorn backend.main:app --reload --port 8000`
2. Start frontend (terminal 2): `cd frontend && npm run dev`
3. Open browser: http://localhost:3000
4. Click on a problem
5. Write code: `print("Hello, World!")`
6. Click "Run Code" - you should see output
7. Click "Check Solution" - if correct, confetti plays! 🎉
