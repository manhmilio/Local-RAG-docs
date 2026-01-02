@echo off
REM Script khởi động backend và frontend cùng lúc (Windows)

echo ========================================
echo Medical Chatbot - Startup Script
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js
    pause
    exit /b 1
)

REM Check Ollama
ollama list >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama not found or not running!
    echo Please install and start Ollama from https://ollama.ai
    pause
    exit /b 1
)

echo [OK] All dependencies found!
echo.

REM Start Backend
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python main.py"
timeout /t 3 >nul

REM Start Frontend
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 3 >nul

echo.
echo ========================================
echo Servers are starting...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C in each terminal to stop
echo ========================================
echo.

pause
