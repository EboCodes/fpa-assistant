#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGS_DIR="$PROJECT_ROOT/logs"
PID_FILE="$PROJECT_ROOT/.services.pid"

mkdir -p "$LOGS_DIR"

echo "=================================================="
echo "🚀 Starting Ajala AI Educational Assistant Services"
echo "=================================================="

# 1. Check PostgreSQL
echo "--> Checking PostgreSQL service..."
if pg_isready -h localhost -p 5432 -U postgres >/dev/null 2>&1; then
    echo "  [OK] PostgreSQL is active and accepting connections."
else
    echo "  [WARN] PostgreSQL might not be running or needs authentication. Attempting start..."
    sudo systemctl start postgresql 2>/dev/null || true
    sleep 2
fi

# 2. Build Frontend for production
echo "--> Verifying frontend production bundle..."
if [ ! -d "$PROJECT_ROOT/frontend/dist" ] || [ "$1" == "--build" ]; then
    echo "  Building frontend..."
    (cd "$PROJECT_ROOT/frontend" && npm run build)
fi
echo "  [OK] Frontend production bundle ready."

# Stop any running instances first
if [ -f "$PROJECT_ROOT/stop-services.sh" ]; then
    bash "$PROJECT_ROOT/stop-services.sh" >/dev/null 2>&1 || true
fi

# 3. Start AI Microservice
echo "--> Launching Python AI Microservice on port 5001..."
AI_PYTHON="$PROJECT_ROOT/ai-service/venv/bin/python"
AI_GUNICORN="$PROJECT_ROOT/ai-service/venv/bin/gunicorn"

if [ -x "$AI_GUNICORN" ]; then
    setsid "$AI_GUNICORN" -w 2 -b 0.0.0.0:5001 --chdir "$PROJECT_ROOT/ai-service/src" main:app --timeout 90 --daemon --pid "$LOGS_DIR/gunicorn.pid" --access-logfile "$LOGS_DIR/ai-access.log" --error-logfile "$LOGS_DIR/ai-service.log"
else
    setsid "$AI_PYTHON" "$PROJECT_ROOT/ai-service/src/main.py" </dev/null >"$LOGS_DIR/ai-service.log" 2>&1 &
fi

# 4. Start Backend API & Unified Frontend
echo "--> Launching Node.js Backend API on port 5000..."
setsid bash -c "cd '$PROJECT_ROOT/backend' && NODE_ENV=production node src/server.js" </dev/null >"$LOGS_DIR/backend.log" 2>&1 &

# Optional: Start Vite dev server if requested
if [ "$1" == "--dev" ]; then
    echo "--> Starting Vite dev server on port 5173..."
    (cd "$PROJECT_ROOT/frontend" && npm run dev > "$LOGS_DIR/frontend-dev.log" 2>&1) &
    FRONTEND_PID=$!
    echo "FRONTEND_PID=$FRONTEND_PID" >> "$PID_FILE"
fi

# Wait for services to become healthy
echo "--> Waiting for services to initialize..."
for i in {1..15}; do
    AI_HEALTH=$(curl -s http://localhost:5001/health 2>/dev/null || true)
    BE_HEALTH=$(curl -s http://localhost:5000/health 2>/dev/null || true)
    if [[ "$AI_HEALTH" == *"running"* ]] && [[ "$BE_HEALTH" == *"running"* ]]; then
        echo "AI_PID=$(lsof -ti :5001 | head -n 1)" > "$PID_FILE"
        echo "BACKEND_PID=$(lsof -ti :5000 | head -n 1)" >> "$PID_FILE"
        echo "=================================================="
        echo "✅ All Services Are Live & Healthy!"
        echo "=================================================="
        echo "  Web Application: http://localhost:5000"
        echo "  Backend API:     http://localhost:5000/api"
        echo "  AI Microservice: http://localhost:5001/health"
        if [ "$1" == "--dev" ]; then
            echo "  Vite Dev Server: http://localhost:5173"
        fi
        echo "  Logs:            $LOGS_DIR/"
        echo "  Admin Login:     joshua@ajala.com (Password: Admin123!)"
        echo "=================================================="
        exit 0
    fi
    sleep 1
done

echo "⚠️ Services launched. Checking status with status-services.sh..."
bash "$PROJECT_ROOT/status-services.sh" || true
