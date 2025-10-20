#!/bin/bash

# ============================================================================
# CryptoSage - Run Backend & Frontend
# ============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         🚀 CryptoSage - Starting Backend & Frontend 🚀        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if ports are already in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0
    else
        return 1
    fi
}

# Kill existing processes on ports
kill_port() {
    if check_port $1; then
        echo -e "${YELLOW}⚠️  Port $1 is in use. Killing existing process...${NC}"
        lsof -i :$1 | grep -v COMMAND | awk '{print $2}' | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
}

# Kill ports if they're in use
echo -e "${BLUE}🔍 Checking ports...${NC}"
kill_port 8000
kill_port 3000
echo -e "${GREEN}✅ Ports cleared${NC}"
echo ""

# Start Backend
echo -e "${BLUE}🔌 Starting Backend API Server (port 8000)...${NC}"
python3 -m src.api.server > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# Start Frontend
echo -e "${BLUE}🎨 Starting Frontend Server (port 3000)...${NC}"
python3 frontend/server.py > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""

# Wait for servers to start
echo -e "${BLUE}⏳ Waiting for servers to start...${NC}"
sleep 3

# Check if servers are running
echo -e "${BLUE}🔍 Checking server status...${NC}"
echo ""

# Check Backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend API: http://localhost:8000${NC}"
    echo -e "${GREEN}✅ API Docs: http://localhost:8000/docs${NC}"
else
    echo -e "${RED}❌ Backend failed to start${NC}"
    echo "Check logs: tail -f /tmp/backend.log"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Check Frontend
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend Dashboard: http://localhost:3000${NC}"
else
    echo -e "${RED}❌ Frontend failed to start${NC}"
    echo "Check logs: tail -f /tmp/frontend.log"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  🎉 All Servers Running! 🎉                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${BLUE}📊 Dashboard:${NC}     http://localhost:3000"
echo -e "${BLUE}🔌 Backend API:${NC}   http://localhost:8000"
echo -e "${BLUE}📚 API Docs:${NC}      http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}📝 Logs:${NC}"
echo "   Backend:  tail -f /tmp/backend.log"
echo "   Frontend: tail -f /tmp/frontend.log"
echo ""
echo -e "${YELLOW}🛑 To stop servers:${NC}"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Keep script running
wait $BACKEND_PID $FRONTEND_PID

