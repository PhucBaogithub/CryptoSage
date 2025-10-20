#!/bin/bash

# CryptoSage - Startup Script for macOS/Linux
# Khởi chạy CryptoSage Dashboard

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         CryptoSage - Bitcoin Futures Trading System        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    echo -e "${YELLOW}⚠️  Killing process on port $port...${NC}"
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
    sleep 1
}

# Check and create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install -q -r requirements.txt 2>/dev/null || {
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
}
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check and kill existing processes
echo ""
echo -e "${YELLOW}🔍 Checking for existing processes...${NC}"

if check_port 8000; then
    kill_port 8000
fi

if check_port 3000; then
    kill_port 3000
fi

echo -e "${GREEN}✓ Ports cleared${NC}"

# Start backend server
echo ""
echo -e "${YELLOW}🚀 Starting Backend Server (Port 8000)...${NC}"
cd "$PROJECT_DIR"
python3 -m src.api.server &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"

# Wait for backend to start
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Backend failed to start${NC}"
    exit 1
fi

# Start frontend server
echo -e "${YELLOW}🚀 Starting Frontend Server (Port 3000)...${NC}"
python3 frontend/server.py &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

# Wait for frontend to start
sleep 2

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✓ All Servers Running!                    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 Dashboard URL:${NC}     ${GREEN}http://localhost:3000${NC}"
echo -e "${BLUE}📚 API Docs:${NC}         ${GREEN}http://localhost:8000/docs${NC}"
echo -e "${BLUE}🏥 Health Check:${NC}     ${GREEN}http://localhost:8000/health${NC}"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo "   • Press Ctrl+C to stop all servers"
echo "   • Backend logs will appear below"
echo "   • Frontend runs on port 3000"
echo "   • API runs on port 8000"
echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    sleep 1
    echo -e "${GREEN}✓ All servers stopped${NC}"
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait

