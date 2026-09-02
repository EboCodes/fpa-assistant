#!/usr/bin/env bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$PROJECT_ROOT/.services.pid"

echo "=================================================="
echo "🛑 Stopping Ajala Educational Assistant Services"
echo "=================================================="

if [ -f "$PID_FILE" ]; then
    source "$PID_FILE"
    if [ -n "$AI_PID" ] && kill -0 "$AI_PID" 2>/dev/null; then
        echo "  Stopping AI service (PID: $AI_PID)..."
        kill "$AI_PID" 2>/dev/null || true
    fi
    if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "  Stopping Backend service (PID: $BACKEND_PID)..."
        kill "$BACKEND_PID" 2>/dev/null || true
    fi
    if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo "  Stopping Frontend dev server (PID: $FRONTEND_PID)..."
        kill "$FRONTEND_PID" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
fi

# Fallback check on ports 5000 and 5001
for port in 5000 5001 5173; do
    PID=$(lsof -ti :$port 2>/dev/null || true)
    if [ -n "$PID" ]; then
        echo "  Cleaning up process on port $port (PID: $PID)..."
        kill -9 $PID 2>/dev/null || true
    fi
done

echo "✅ All services stopped."
