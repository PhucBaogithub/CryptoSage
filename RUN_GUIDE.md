# 🚀 CryptoSage - How to Run Backend & Frontend

## 📋 Quick Start

### Option 1: Using Python Script (Recommended)
```bash
cd /Users/phucbao/Documents/Binance
python3 run_all.py
```

### Option 2: Using Bash Script
```bash
cd /Users/phucbao/Documents/Binance
chmod +x run_all.sh
./run_all.sh
```

### Option 3: Manual (2 Terminals)

**Terminal 1 - Backend:**
```bash
cd /Users/phucbao/Documents/Binance
python3 -m src.api.server
```

**Terminal 2 - Frontend:**
```bash
cd /Users/phucbao/Documents/Binance
python3 frontend/server.py
```

---

## 🌐 Access Points

Once running, access:

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 📊 What Each Script Does

### `run_all.py` (Python Script)
✅ Automatically kills existing processes on ports 8000 & 3000  
✅ Starts backend and frontend in parallel  
✅ Checks if servers are running  
✅ Shows colored output with status  
✅ Handles Ctrl+C gracefully  
✅ Cross-platform compatible  

**Usage:**
```bash
python3 run_all.py
```

**Stop:**
```
Press Ctrl+C
```

---

### `run_all.sh` (Bash Script)
✅ Automatically kills existing processes on ports 8000 & 3000  
✅ Starts backend and frontend in parallel  
✅ Checks if servers are running  
✅ Shows colored output with status  
✅ Logs to `/tmp/backend.log` and `/tmp/frontend.log`  

**Usage:**
```bash
chmod +x run_all.sh
./run_all.sh
```

**View Logs:**
```bash
tail -f /tmp/backend.log
tail -f /tmp/frontend.log
```

**Stop:**
```bash
kill <BACKEND_PID> <FRONTEND_PID>
```

---

## 🔧 Manual Setup (2 Terminals)

### Terminal 1 - Start Backend
```bash
cd /Users/phucbao/Documents/Binance
python3 -m src.api.server
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2 - Start Frontend
```bash
cd /Users/phucbao/Documents/Binance
python3 frontend/server.py
```

Expected output:
```
Serving on http://0.0.0.0:3000
```

### Terminal 3 - Open Dashboard
```bash
open http://localhost:3000
# or
curl http://localhost:3000
```

---

## ✅ Verification

### Check Backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","timestamp":"2025-10-20T08:56:34.366343","version":"1.0.0"}
```

### Check Frontend
```bash
curl http://localhost:3000 | head -20
```

Should return HTML content.

---

## 🛑 Stopping Servers

### If using `run_all.py` or `run_all.sh`
```bash
Press Ctrl+C
```

### If using manual setup
```bash
# Terminal 1 & 2: Press Ctrl+C

# Or kill by port:
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Kill process on port 3000
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

### Backend Won't Start
```bash
# Check if Python is installed
python3 --version

# Check if dependencies are installed
pip3 list | grep fastapi

# Install dependencies
pip3 install -r requirements.txt
```

### Frontend Won't Start
```bash
# Check if Python is installed
python3 --version

# Try running directly
cd /Users/phucbao/Documents/Binance
python3 frontend/server.py
```

### Can't Connect to Dashboard
```bash
# Check if frontend is running
curl http://localhost:3000

# Check if backend is running
curl http://localhost:8000/health

# Check firewall settings
# Make sure ports 3000 and 8000 are not blocked
```

---

## 📝 Code Examples

### Python - Start Both Servers
```python
import subprocess
import time

# Start backend
backend = subprocess.Popen(["python3", "-m", "src.api.server"])

# Start frontend
frontend = subprocess.Popen(["python3", "frontend/server.py"])

# Wait for servers
time.sleep(3)

# Check if running
import urllib.request
try:
    urllib.request.urlopen("http://localhost:8000/health")
    print("✅ Backend is running")
except:
    print("❌ Backend failed")

try:
    urllib.request.urlopen("http://localhost:3000")
    print("✅ Frontend is running")
except:
    print("❌ Frontend failed")

# Keep running
try:
    backend.wait()
    frontend.wait()
except KeyboardInterrupt:
    backend.terminate()
    frontend.terminate()
```

### Bash - Start Both Servers
```bash
#!/bin/bash

# Start backend
python3 -m src.api.server > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

# Start frontend
python3 frontend/server.py > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for servers
sleep 3

# Check status
curl http://localhost:8000/health && echo "✅ Backend OK"
curl http://localhost:3000 > /dev/null && echo "✅ Frontend OK"

# Keep running
wait $BACKEND_PID $FRONTEND_PID
```

---

## 🎯 Recommended Workflow

1. **First Time Setup:**
   ```bash
   cd /Users/phucbao/Documents/Binance
   python3 run_all.py
   ```

2. **Open Dashboard:**
   ```
   http://localhost:3000
   ```

3. **View API Docs:**
   ```
   http://localhost:8000/docs
   ```

4. **Stop Servers:**
   ```
   Press Ctrl+C
   ```

---

## 📚 Additional Resources

- **README.md** - Project overview
- **DASHBOARD_GUIDE.md** - Dashboard features
- **ARCHITECTURE.md** - System design
- **WEB_DASHBOARD_SETUP.md** - API reference

---

## 🎉 You're All Set!

Your CryptoSage dashboard is ready to run. Choose your preferred method above and start trading! 🚀

