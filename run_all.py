#!/usr/bin/env python3
"""
CryptoSage - Run Backend & Frontend
"""

import subprocess
import time
import os
import signal
import sys
import socket
from pathlib import Path

# Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    print(f"\n{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}║         🚀 CryptoSage - Starting Backend & Frontend 🚀        ║{Colors.ENDC}")
    print(f"{Colors.BOLD}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.ENDC}")

def is_port_in_use(port):
    """Check if port is in use"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def kill_port(port):
    """Kill process using port"""
    if is_port_in_use(port):
        print_warning(f"Port {port} is in use. Killing existing process...")
        os.system(f"lsof -i :{port} | grep -v COMMAND | awk '{{print $2}}' | xargs kill -9 2>/dev/null || true")
        time.sleep(1)

def check_server(url, name):
    """Check if server is running"""
    try:
        import urllib.request
        urllib.request.urlopen(url, timeout=2)
        return True
    except:
        return False

def main():
    print_header()
    
    # Get project directory
    project_dir = Path(__file__).parent.absolute()
    os.chdir(project_dir)
    
    print_info("Checking ports...")
    kill_port(8000)
    kill_port(3000)
    print_success("Ports cleared\n")
    
    # Start Backend
    print_info("Starting Backend API Server (port 8000)...")
    backend_process = subprocess.Popen(
        ["python3", "-m", "src.api.server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=project_dir
    )
    print_success(f"Backend started (PID: {backend_process.pid})\n")
    
    # Start Frontend
    print_info("Starting Frontend Server (port 3000)...")
    frontend_process = subprocess.Popen(
        ["python3", "frontend/server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=project_dir
    )
    print_success(f"Frontend started (PID: {frontend_process.pid})\n")
    
    # Wait for servers to start
    print_info("Waiting for servers to start...")
    time.sleep(3)
    
    # Check servers
    print_info("Checking server status...\n")
    
    backend_ok = check_server("http://localhost:8000/health", "Backend")
    frontend_ok = check_server("http://localhost:3000", "Frontend")
    
    if backend_ok:
        print_success("Backend API: http://localhost:8000")
        print_success("API Docs: http://localhost:8000/docs")
    else:
        print_error("Backend failed to start")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(1)
    
    if frontend_ok:
        print_success("Frontend Dashboard: http://localhost:3000")
    else:
        print_error("Frontend failed to start")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(1)
    
    print(f"\n{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}║                  🎉 All Servers Running! 🎉                   ║{Colors.ENDC}")
    print(f"{Colors.BOLD}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
    
    print(f"{Colors.BLUE}📊 Dashboard:{Colors.ENDC}     http://localhost:3000")
    print(f"{Colors.BLUE}🔌 Backend API:{Colors.ENDC}   http://localhost:8000")
    print(f"{Colors.BLUE}📚 API Docs:{Colors.ENDC}      http://localhost:8000/docs")
    print()
    print(f"{Colors.YELLOW}🛑 Press Ctrl+C to stop servers{Colors.ENDC}\n")
    
    # Handle Ctrl+C
    def signal_handler(sig, frame):
        print(f"\n{Colors.YELLOW}Stopping servers...{Colors.ENDC}")
        backend_process.terminate()
        frontend_process.terminate()
        time.sleep(1)
        backend_process.kill()
        frontend_process.kill()
        print_success("Servers stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Wait for processes
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()

