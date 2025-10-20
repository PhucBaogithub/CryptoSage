#!/usr/bin/env python3
"""
CryptoSage - Startup Script
Khởi chạy CryptoSage Dashboard (Cross-platform)
"""

import os
import sys
import subprocess
import time
import signal
import platform
from pathlib import Path

# Colors for output
class Colors:
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    NC = '\033[0m'  # No Color

def print_header():
    """Print welcome header"""
    print(f"\n{Colors.BLUE}╔════════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         CryptoSage - Bitcoin Futures Trading System        ║{Colors.NC}")
    print(f"{Colors.BLUE}╚════════════════════════════════════════════════════════════╝{Colors.NC}\n")

def check_python_version():
    """Check if Python version is 3.9 or higher"""
    if sys.version_info < (3, 9):
        print(f"{Colors.RED}✗ Python 3.9 or higher is required{Colors.NC}")
        print(f"  Current version: {sys.version}")
        sys.exit(1)
    print(f"{Colors.GREEN}✓ Python version: {sys.version.split()[0]}{Colors.NC}")

def create_venv():
    """Create virtual environment if it doesn't exist"""
    venv_dir = Path("venv")
    if not venv_dir.exists():
        print(f"{Colors.YELLOW}📦 Creating virtual environment...{Colors.NC}")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print(f"{Colors.GREEN}✓ Virtual environment created{Colors.NC}")
    else:
        print(f"{Colors.GREEN}✓ Virtual environment exists{Colors.NC}")

def install_dependencies():
    """Install required dependencies"""
    print(f"{Colors.YELLOW}📥 Installing dependencies...{Colors.NC}")
    
    # Get pip executable
    if platform.system() == "Windows":
        pip_exe = Path("venv/Scripts/pip.exe")
    else:
        pip_exe = Path("venv/bin/pip")
    
    try:
        subprocess.run(
            [str(pip_exe), "install", "-q", "-r", "requirements.txt"],
            check=True,
            capture_output=True
        )
        print(f"{Colors.GREEN}✓ Dependencies installed{Colors.NC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}✗ Failed to install dependencies{Colors.NC}")
        print(f"  Error: {e}")
        sys.exit(1)

def kill_port(port):
    """Kill process on specified port"""
    try:
        if platform.system() == "Windows":
            os.system(f"netstat -ano | findstr :{port} && taskkill /F /PID <PID> >nul 2>&1")
        else:
            os.system(f"lsof -ti:{port} | xargs kill -9 2>/dev/null || true")
        time.sleep(1)
    except Exception as e:
        print(f"  Warning: Could not kill port {port}: {e}")

def start_servers():
    """Start backend and frontend servers"""
    print(f"\n{Colors.YELLOW}🔍 Checking for existing processes...{Colors.NC}")
    kill_port(8000)
    kill_port(3000)
    print(f"{Colors.GREEN}✓ Ports cleared{Colors.NC}")
    
    # Get python executable
    if platform.system() == "Windows":
        python_exe = Path("venv/Scripts/python.exe")
    else:
        python_exe = Path("venv/bin/python")
    
    print(f"\n{Colors.YELLOW}🚀 Starting Backend Server (Port 8000)...{Colors.NC}")
    backend_process = subprocess.Popen(
        [str(python_exe), "-m", "src.api.server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"{Colors.GREEN}✓ Backend started (PID: {backend_process.pid}){Colors.NC}")
    
    time.sleep(3)
    
    print(f"{Colors.YELLOW}🚀 Starting Frontend Server (Port 3000)...{Colors.NC}")
    frontend_process = subprocess.Popen(
        [str(python_exe), "frontend/server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"{Colors.GREEN}✓ Frontend started (PID: {frontend_process.pid}){Colors.NC}")
    
    time.sleep(2)
    
    return backend_process, frontend_process

def print_info():
    """Print server information"""
    print(f"\n{Colors.GREEN}╔════════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.GREEN}║                  ✓ All Servers Running!                    ║{Colors.NC}")
    print(f"{Colors.GREEN}╚════════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.BLUE}📊 Dashboard URL:{Colors.NC}     {Colors.GREEN}http://localhost:3000{Colors.NC}")
    print(f"{Colors.BLUE}📚 API Docs:{Colors.NC}         {Colors.GREEN}http://localhost:8000/docs{Colors.NC}")
    print(f"{Colors.BLUE}🏥 Health Check:{Colors.NC}     {Colors.GREEN}http://localhost:8000/health{Colors.NC}\n")
    
    print(f"{Colors.YELLOW}💡 Tips:{Colors.NC}")
    print("   • Press Ctrl+C to stop all servers")
    print("   • Backend logs will appear below")
    print("   • Frontend runs on port 3000")
    print("   • API runs on port 8000\n")
    print(f"{Colors.YELLOW}═══════════════════════════════════════════════════════════{Colors.NC}\n")

def main():
    """Main function"""
    try:
        print_header()
        check_python_version()
        create_venv()
        install_dependencies()
        
        backend_process, frontend_process = start_servers()
        print_info()
        
        # Wait for processes
        def signal_handler(sig, frame):
            print(f"\n{Colors.YELLOW}🛑 Stopping servers...{Colors.NC}")
            backend_process.terminate()
            frontend_process.terminate()
            time.sleep(1)
            backend_process.kill()
            frontend_process.kill()
            print(f"{Colors.GREEN}✓ All servers stopped{Colors.NC}")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Keep running
        while True:
            if backend_process.poll() is not None or frontend_process.poll() is not None:
                print(f"{Colors.RED}✗ One of the servers crashed{Colors.NC}")
                break
            time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Stopping servers...{Colors.NC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.NC}")
        sys.exit(1)

if __name__ == "__main__":
    main()

