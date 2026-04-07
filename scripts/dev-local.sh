#!/bin/bash
# METHEAN local development without Docker
# Requires: Python 3.12+, Node 20+, PostgreSQL 16, Redis

set -e

echo "=== METHEAN Local Development ==="
echo ""

# Check dependencies
python3 --version || { echo "ERROR: Python 3.12+ required"; exit 1; }
node --version || { echo "ERROR: Node 20+ required"; exit 1; }
psql --version 2>/dev/null || echo "WARNING: PostgreSQL not found locally. Set DATABASE_URL to a remote DB."
redis-cli ping 2>/dev/null || echo "WARNING: Redis not found locally. Set REDIS_URL to a remote Redis."

# Load .env if it exists
if [ -f .env ]; then
  echo "Loading .env..."
  set -a; source .env; set +a
elif [ -f .env.example ]; then
  echo "WARNING: No .env found. Copy .env.example to .env and configure it."
  echo "  cp .env.example .env"
  exit 1
fi

# Backend setup
echo ""
echo "Setting up backend..."
cd backend

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q -r requirements.txt

# Run migrations
echo "Running migrations..."
alembic upgrade head 2>/dev/null || echo "WARNING: Migrations failed. Check DATABASE_URL."

# Start backend (background)
echo "Starting backend on :8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Frontend setup
echo ""
echo "Setting up frontend..."
cd ../frontend
npm install --silent 2>/dev/null
echo "Starting frontend on :3000..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=== METHEAN running ==="
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo "  Health:   http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
