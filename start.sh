#!/bin/bash
# Script khởi động backend và frontend cùng lúc (Linux/Mac)

echo "========================================"
echo "Medical Chatbot - Startup Script"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found! Please install Python 3.10+"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js not found! Please install Node.js"
    exit 1
fi

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "[ERROR] Ollama not found or not running!"
    echo "Please install and start Ollama from https://ollama.ai"
    exit 1
fi

echo "[OK] All dependencies found!"
echo ""

# Start Backend
echo "Starting Backend Server..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

sleep 3

# Start Frontend
echo "Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 3

echo ""
echo "========================================"
echo "Servers are running!"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "========================================"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
