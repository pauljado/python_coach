# Python Coach

A modern, interactive Python learning platform with a beautiful React/Next.js frontend and FastAPI backend. Learn Python through hands-on practice problems with progressive hints, instant solution checking, and gamification features.

## Features

- **140+ Practice Problems** - From basic syntax to advanced concepts
- **Modern Code Editor** - Monaco Editor (VS Code in browser) with syntax highlighting
- **Instant Feedback** - Real-time code execution and solution checking
- **Progressive Hints** - Get help when you're stuck
- **Gamification** - Points, progress tracking, achievements, and celebrations
- **Beautiful UI** - Modern design with dark mode support
- **Progress Persistence** - Your progress is saved locally

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Frontend
- **Next.js 14+** - React framework with App Router
- **TypeScript** - Type-safe code
- **Tailwind CSS** - Utility-first CSS
- **Monaco Editor** - VS Code editor in browser
- **Framer Motion** - Animations
- **Zustand** - State management
- **React Hot Toast** - Notifications

## Project Structure

```
python_coach/
├── backend/               # FastAPI backend
│   ├── api/              # API routes
│   ├── core/             # Core configuration
│   └── services/         # Service layer
├── frontend/             # Next.js frontend
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/              # Utilities and API client
│   └── types/            # TypeScript types
├── problems/             # Problem definitions (unchanged)
├── engine/               # Code execution engine (unchanged)
└── progress.json         # User progress (auto-generated)
```

## Installation

### Prerequisites
- Python 3.12+
- Node.js 18+ and npm

### Backend Setup

1. Install Python dependencies:

```bash
uv pip install -r backend/requirements.txt
```

Or if you prefer pip:

```bash
pip install -r backend/requirements.txt
```

Or using the existing modules, the backend will use them directly.

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

## Running the Application

### Development Mode

1. **Start the backend** (in one terminal):

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

Or:

```bash
python backend/main.py
```

The API will be available at `http://localhost:8000`

2. **Start the frontend** (in another terminal):

```bash
cd frontend
npm run dev
```

The app will be available at `http://localhost:3000`

### Environment Variables

Create a `.env.local` file in the `frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Usage

1. **Browse Problems** - View all problems on the home page, filter by category or difficulty
2. **Select a Problem** - Click on a problem card to start solving
3. **Write Code** - Use the Monaco editor to write your Python solution
4. **Run Code** - Click "Run Code" to execute and see output
5. **Check Solution** - Click "Check Solution" to verify correctness
6. **Get Hints** - Click "Get Hint" for progressive help
7. **Track Progress** - Your progress is automatically saved and displayed

## API Endpoints

- `GET /api/problems` - List all problems (with optional filters)
- `GET /api/problems/{id}` - Get specific problem
- `POST /api/execute` - Execute Python code
- `POST /api/check` - Check solution
- `GET /api/progress` - Get user progress
- `POST /api/progress/complete` - Mark problem as completed
- `GET /api/stats` - Get statistics

## Development

### Backend Development

The backend wraps existing Python modules without modifying their logic:
- `problems/problem_loader.py` - Problem management
- `engine/code_executor.py` - Code execution
- `engine/solution_checker.py` - Solution validation
- `engine/progress_manager.py` - Progress tracking

### Frontend Development

- Components are organized by feature in `components/`
- API client is in `lib/api/client.ts`
- State management uses Zustand in `lib/store/`
- Types are defined in `types/index.ts`

## Building for Production

### Frontend

```bash
cd frontend
npm run build
npm start
```

### Backend

The backend can be deployed with any ASGI server (Uvicorn, Gunicorn, etc.)

## License

MIT License
