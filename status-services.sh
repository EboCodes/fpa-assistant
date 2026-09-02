#!/usr/bin/env bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$PROJECT_ROOT/.services.pid"

echo "=================================================="
echo "📊 Ajala System Status Report"
echo "=================================================="

# 1. Database
echo -n "  PostgreSQL:      "
if pg_isready -h localhost -p 5432 -U postgres >/dev/null 2>&1; then
    echo "🟢 ONLINE (Port 5432)"
else
    echo "🔴 OFFLINE"
fi

# 2. AI Microservice
echo -n "  AI Microservice: "
AI_RES=$(curl -s --max-time 3 http://localhost:5001/health 2>/dev/null || true)
if [[ "$AI_RES" == *"running"* ]]; then
    echo "🟢 ONLINE (Port 5001) - $AI_RES"
else
    echo "🔴 OFFLINE"
fi

# 3. Backend API
echo -n "  Backend API:     "
BE_RES=$(curl -s --max-time 3 http://localhost:5000/health 2>/dev/null || true)
if [[ "$BE_RES" == *"running"* ]]; then
    echo "🟢 ONLINE (Port 5000) - $BE_RES"
else
    echo "🔴 OFFLINE"
fi

# 4. Web Application (Frontend)
echo -n "  Web Application: "
WEB_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://localhost:5000/ 2>/dev/null || true)
if [ "$WEB_CODE" == "200" ]; then
    echo "🟢 ONLINE (http://localhost:5000/)"
else
    # Check Vite dev server
    VITE_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://localhost:5173/ 2>/dev/null || true)
    if [ "$VITE_CODE" == "200" ]; then
        echo "🟢 ONLINE on Vite Dev Server (http://localhost:5173/)"
    else
        echo "🔴 OFFLINE (HTTP $WEB_CODE)"
    fi
fi

# 5. Active Knowledge Base Entries
echo -n "  KB Records:      "
KB_COUNT=$(PGPASSWORD=ayoade2004 psql -h localhost -U postgres -d educational_assistant -t -c 'SELECT count(*) FROM knowledge_base WHERE status="active"' 2>/dev/null || echo "N/A")
KB_COUNT=$(echo "$KB_COUNT" | tr -d '[:space:]')
if [ -n "$KB_COUNT" ] && [ "$KB_COUNT" != "N/A" ]; then
    echo "$KB_COUNT active entries in database"
else
    # Fallback query with single quotes
    KB_COUNT=$(PGPASSWORD=ayoade2004 psql -h localhost -U postgres -d educational_assistant -t -c "SELECT count(*) FROM knowledge_base WHERE status='active'" 2>/dev/null || echo "N/A")
    echo "$(echo "$KB_COUNT" | tr -d '[:space:]') active entries"
fi

echo "=================================================="
