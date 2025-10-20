@echo off
REM CryptoSage - Startup Script for Windows
REM Khởi chạy CryptoSage Dashboard

setlocal enabledelayedexpansion

REM Colors (using ANSI codes)
set "BLUE=[34m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "RED=[31m"
set "NC=[0m"

REM Project directory
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%venv"

echo.
echo %BLUE%╔════════════════════════════════════════════════════════════╗%NC%
echo %BLUE%║         CryptoSage - Bitcoin Futures Trading System        ║%NC%
echo %BLUE%╚════════════════════════════════════════════════════════════╝%NC%
echo.

REM Check if virtual environment exists
if not exist "%VENV_DIR%" (
    echo %YELLOW%📦 Creating virtual environment...%NC%
    python -m venv "%VENV_DIR%"
    echo %GREEN%✓ Virtual environment created%NC%
)

REM Activate virtual environment
echo %YELLOW%🔧 Activating virtual environment...%NC%
call "%VENV_DIR%\Scripts\activate.bat"
echo %GREEN%✓ Virtual environment activated%NC%

REM Install dependencies
echo %YELLOW%📥 Installing dependencies...%NC%
pip install -q -r requirements.txt
if errorlevel 1 (
    echo %RED%✗ Failed to install dependencies%NC%
    pause
    exit /b 1
)
echo %GREEN%✓ Dependencies installed%NC%

REM Kill existing processes on ports
echo.
echo %YELLOW%🔍 Checking for existing processes...%NC%

REM Kill port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo %YELLOW%⚠️  Killing process on port 8000...%NC%
    taskkill /PID %%a /F >nul 2>&1
)

REM Kill port 3000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    echo %YELLOW%⚠️  Killing process on port 3000...%NC%
    taskkill /PID %%a /F >nul 2>&1
)

timeout /t 1 /nobreak >nul
echo %GREEN%✓ Ports cleared%NC%

REM Start backend server
echo.
echo %YELLOW%🚀 Starting Backend Server (Port 8000)...%NC%
cd /d "%PROJECT_DIR%"
start "CryptoSage Backend" python -m src.api.server
timeout /t 3 /nobreak >nul
echo %GREEN%✓ Backend started%NC%

REM Start frontend server
echo %YELLOW%🚀 Starting Frontend Server (Port 3000)...%NC%
start "CryptoSage Frontend" python frontend/server.py
timeout /t 2 /nobreak >nul
echo %GREEN%✓ Frontend started%NC%

echo.
echo %GREEN%╔════════════════════════════════════════════════════════════╗%NC%
echo %GREEN%║                  ✓ All Servers Running!                    ║%NC%
echo %GREEN%╚════════════════════════════════════════════════════════════╝%NC%
echo.
echo %BLUE%📊 Dashboard URL:     %GREEN%http://localhost:3000%NC%
echo %BLUE%📚 API Docs:          %GREEN%http://localhost:8000/docs%NC%
echo %BLUE%🏥 Health Check:      %GREEN%http://localhost:8000/health%NC%
echo.
echo %YELLOW%💡 Tips:%NC%
echo    • Close this window to stop all servers
echo    • Backend runs in a separate window
echo    • Frontend runs in a separate window
echo    • Frontend on port 3000
echo    • API on port 8000
echo.
echo %YELLOW%═══════════════════════════════════════════════════════════%NC%
echo.

pause

