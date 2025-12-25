#!/bin/bash
# Start all services for House Price Prediction App

echo "Starting House Price Prediction App..."
echo ""

# Detect OS and set Python/Celery paths
if [ -f "venv/Scripts/python.exe" ]; then
    PYTHON_CMD="venv/Scripts/python.exe"
    CELERY_CMD="venv/Scripts/celery.exe"
elif [ -f "venv/bin/python" ]; then
    PYTHON_CMD="venv/bin/python"
    CELERY_CMD="venv/bin/celery"
else
    echo "Virtual environment not found!"
    exit 1
fi

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "Redis is not running! Please start Redis: redis-server"
    exit 1
fi

# Navigate to backend
cd backend/house_price_project || exit 1

# Setup database
"../../$PYTHON_CMD" manage.py makemigrations --noinput 2>/dev/null
"../../$PYTHON_CMD" manage.py migrate --noinput || exit 1

# Start Celery worker in background
if [ -f "../../$CELERY_CMD" ]; then
    "../../$CELERY_CMD" -A house_price_project worker --loglevel=info -P solo > /dev/null 2>&1 &
else
    "../../$PYTHON_CMD" -m celery -A house_price_project worker --loglevel=info -P solo > /dev/null 2>&1 &
fi
CELERY_WORKER_PID=$!

# Start Celery beat in background
if [ -f "../../$CELERY_CMD" ]; then
    "../../$CELERY_CMD" -A house_price_project beat --loglevel=info > /dev/null 2>&1 &
else
    "../../$PYTHON_CMD" -m celery -A house_price_project beat --loglevel=info > /dev/null 2>&1 &
fi
CELERY_BEAT_PID=$!

# Start frontend in background
cd ../../frontend || exit 1
npm run dev > /tmp/vite.log 2>&1 &
FRONTEND_PID=$!
sleep 5
FRONTEND_URL=$(grep -oE 'http://localhost:[0-9]+' /tmp/vite.log 2>/dev/null | head -1)
if [ -z "$FRONTEND_URL" ]; then
    # Fallback: check common ports
    if netstat -an 2>/dev/null | grep -q ":5173" || lsof -i :5173 2>/dev/null | grep -q LISTEN; then
        FRONTEND_URL="http://localhost:5173"
    elif netstat -an 2>/dev/null | grep -q ":5174" || lsof -i :5174 2>/dev/null | grep -q LISTEN; then
        FRONTEND_URL="http://localhost:5174"
    else
        FRONTEND_URL="http://localhost:5173"
    fi
fi

# Go back to backend and start Django in foreground
cd ../backend/house_price_project || exit 1

echo "All services started!"
echo "Django: http://localhost:8000"
echo "Frontend: $FRONTEND_URL"
echo "Press Ctrl+C to stop"
echo ""

# Cleanup function
cleanup() {
    kill $CELERY_WORKER_PID 2>/dev/null
    kill $CELERY_BEAT_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    pkill -f "manage.py runserver" 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Django in foreground (keeps script running, Ctrl+C to stop)
"../../$PYTHON_CMD" manage.py runserver 8000
