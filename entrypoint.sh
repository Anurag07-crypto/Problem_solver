#!/bin/bash
set -e

echo "=== Problem Solver Application Startup ==="

# Configuration
BACKEND_PORT=${BACKEND_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-8501}

# Function to wait for service
wait_for_service() {
    local port=$1
    local max_attempts=30
    local attempt=1
    
    echo "Waiting for localhost:$port to respond..."
    while [ $attempt -le $max_attempts ]; do
        if nc -z localhost $port 2>/dev/null || curl -s http://localhost:$port > /dev/null 2>&1; then
            echo "✓ Service on port $port is ready!"
            return 0
        fi
        echo "  Attempt $attempt/$max_attempts..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "⚠ Warning: Service on port $port did not respond in time (continuing anyway)"
    return 0
}

# Start FastAPI backend in background
echo ""
echo "Starting FastAPI Backend on port $BACKEND_PORT..."
nohup uv run python Backend/backend.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to be ready
sleep 3
wait_for_service $BACKEND_PORT

# Show backend startup messages
echo ""
echo "Backend initialization in progress (this may take a few minutes on first run)..."
echo ""

# Start Streamlit frontend
echo "Starting Streamlit Frontend on port $FRONTEND_PORT..."
uv run streamlit run Frontend/Home.py \
    --server.address=0.0.0.0 \
    --server.port=$FRONTEND_PORT \
    --logger.level=info

# Cleanup
trap "kill $BACKEND_PID 2>/dev/null" EXIT
