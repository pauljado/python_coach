# Testing Guide - Python Coach

This guide explains how to run and test the Python Coach application.

## Prerequisites

- Python 3.12+ installed
- Node.js 18+ and npm installed
- Virtual environment activated (recommended)

## Step 1: Install Backend Dependencies

From the project root directory:

```bash
# Install backend dependencies using uv
uv pip install -r backend/requirements.txt
```

Note: If using uv, you don't need to manually activate a virtual environment - `uv` manages it automatically.

## Step 2: Start the Backend Server

**Option A: Run from project root (Recommended)**

```bash
# From project root
python -m uvicorn backend.main:app --reload --port 8000
```

**Option B: Use the run script**

```bash
# From project root
python backend/run.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend is Running:**

- Open your browser and go to: http://localhost:8000/docs
- You should see the FastAPI interactive API documentation (Swagger UI)
- Try the `/api/problems` endpoint to see if it returns the problems list

## Step 3: Install Frontend Dependencies

Open a **new terminal window** (keep the backend running):

```bash
cd frontend
npm install
```

This will install all React/Next.js dependencies.

## Step 4: Start the Frontend Development Server

```bash
# Make sure you're in the frontend directory
cd frontend
npm run dev
```

You should see:
```
✓ Ready in [time]
○ Local:        http://localhost:3000
```

## Step 5: Access the Application

Open your browser and navigate to:

**Frontend Application:** http://localhost:3000

You should see:
- The Python Coach home page with all problems listed
- A sidebar with filters
- Progress tracking in the header
- Dark mode toggle button

## Testing the Application

### 1. Test Problem List Page

- ✅ Verify problems are displayed in cards
- ✅ Try filtering by category (Syntax, Control Flow, etc.)
- ✅ Try filtering by difficulty (Beginner, Intermediate, Advanced)
- ✅ Check that completed problems show a checkmark
- ✅ Verify progress stats are displayed

### 2. Test Problem Detail Page

- Click on any problem card
- You should see:
  - ✅ Problem description
  - ✅ Code editor (Monaco Editor with syntax highlighting)
  - ✅ Action buttons (Run Code, Check Solution, Get Hint)
  - ✅ Output panel (initially empty)

### 3. Test Code Execution

1. Write some Python code in the editor (try: `print("Hello, World!")`)
2. Click "Run Code" button
3. ✅ Verify output appears in the output panel
4. ✅ Check execution time is displayed

### 4. Test Solution Checking

1. Write a correct solution to a problem
2. Click "Check Solution" button
3. ✅ Verify success message appears
4. ✅ Verify confetti animation plays
5. ✅ Verify problem is marked as completed
6. ✅ Verify points are added to your score

### 5. Test Hints

1. Click "Get Hint" button
2. ✅ Verify hints appear progressively
3. ✅ Verify hint count is saved

### 6. Test Progress Persistence

1. Complete a few problems
2. Refresh the page (F5)
3. ✅ Verify your progress is still there
4. ✅ Verify completed problems still show checkmarks
5. ✅ Verify points are still tracked

### 7. Test Dark Mode

1. Click the moon/sun icon in the header
2. ✅ Verify theme switches between light and dark
3. ✅ Verify code editor theme matches

### 8. Test Navigation

1. Use "Previous" and "Next" buttons on problem page
2. ✅ Verify navigation between problems works
3. ✅ Verify "Back to Problems" returns to home page

## Testing the API Directly

You can test the backend API directly using the interactive docs:

**Swagger UI:** http://localhost:8000/docs

Or use curl/Postman:

```bash
# Get all problems
curl http://localhost:8000/api/problems

# Get a specific problem
curl http://localhost:8000/api/problems/syntax_001

# Execute code
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello!\")"}'

# Get progress
curl http://localhost:8000/api/progress

# Get stats
curl http://localhost:8000/api/stats
```

## Troubleshooting

### Backend Issues

**Error: `ModuleNotFoundError: No module named 'backend'`**

- Make sure you're running from the **project root**, not from inside the `backend` directory
- Use: `python -m uvicorn backend.main:app --reload --port 8000`

**Error: `ModuleNotFoundError: No module named 'fastapi'`**

- Install dependencies: `uv pip install -r backend/requirements.txt`

**Error: Problems not loading**

- Check that `problems/problems.json` exists
- Verify the file path in the error message

### Frontend Issues

**Error: `Cannot connect to API`**

- Make sure the backend is running on port 8000
- Check browser console for CORS errors
- Verify `.env.local` has correct API URL (optional, defaults to http://localhost:8000/api)

**Error: `npm install` fails**

- Make sure Node.js 18+ is installed
- Try deleting `node_modules` and `package-lock.json`, then run `npm install` again

**Build Errors**

- Run `npm run build` to see detailed error messages
- Check TypeScript errors with `npx tsc --noEmit`

### Port Already in Use

If port 8000 or 3000 is already in use:

**Backend:**
```bash
python -m uvicorn backend.main:app --reload --port 8001
```

**Frontend:**
Update `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8001/api
```

Then:
```bash
PORT=3001 npm run dev
```

## Expected Behavior

### On Problem Completion

- ✅ Confetti animation plays
- ✅ Success toast notification appears
- ✅ Problem card shows checkmark
- ✅ Points increase in header
- ✅ Progress bar updates
- ✅ Progress saved to `progress.json` file

### Code Editor Features

- ✅ Syntax highlighting for Python
- ✅ Line numbers
- ✅ Auto-indentation
- ✅ Dark/light theme matching app theme
- ✅ Font: JetBrains Mono or Fira Code

## Quick Test Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Problems list loads on home page
- [ ] Can filter problems by category/difficulty
- [ ] Can click on a problem to view details
- [ ] Code editor loads and accepts input
- [ ] "Run Code" executes Python code
- [ ] "Check Solution" validates code
- [ ] Hints appear when clicked
- [ ] Progress persists after page refresh
- [ ] Dark mode toggle works
- [ ] Navigation between problems works
- [ ] Confetti plays on problem completion

## Performance Notes

- First code execution may be slightly slower (Monaco Editor loading)
- Backend reloads automatically on code changes (development mode)
- Frontend hot-reloads on file changes (development mode)
