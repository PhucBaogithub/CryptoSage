# Getting Started with CryptoSage

This guide will help you get the Bitcoin Futures Trading System up and running in minutes.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (for GitHub)
- A terminal/command line

## Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to the project directory
cd /Users/phucbao/Documents/Binance

# Install the project and dependencies
pip install -e .
```

**Expected output:**
```
Successfully installed cryptosage-1.0.0
```

## Step 2: Start the Backend API (Terminal 1)

Open a new terminal and run:

```bash
python -m src.api.server
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Keep this terminal open and running.

## Step 3: Start the Frontend Server (Terminal 2)

Open another new terminal and run:

```bash
cd /Users/phucbao/Documents/Binance/frontend
python server.py
```

**Expected output:**
```
Frontend server running at http://0.0.0.0:3000
```

Keep this terminal open and running.

## Step 4: Open the Dashboard (Terminal 3)

Open your web browser and go to:

```
http://localhost:3000
```

You should see the CryptoSage dashboard with 6 tabs:
- Overview
- Data
- Models
- Backtest
- Trading
- Risk

## 🎉 You're Done!

The web dashboard is now running. You can:
- Monitor account status
- View equity curves
- Configure and run backtests
- Place trading orders
- Manage risk settings

## Troubleshooting

### Port Already in Use

If you get "Address already in use" error:

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (replace PID with the actual process ID)
kill -9 <PID>
```

### API Not Responding

Check if the backend is running:
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"ok"}`

### Dashboard Not Loading

1. Check if frontend server is running
2. Open browser console (F12) for errors
3. Verify URL is http://localhost:3000 (not https)

### Python Version Error

Check your Python version:
```bash
python --version
```

Must be 3.10 or higher. If not, install Python 3.10+.

## Configuration (Optional)

To use real Binance API credentials:

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
# BINANCE_API_KEY=your_key_here
# BINANCE_API_SECRET=your_secret_here
```

## Next Steps

### 1. Explore the Dashboard
- Click through each tab
- Try the different features
- Test the API endpoints

### 2. Run Example Scripts
```bash
python examples/01_data_collection.py
python examples/02_feature_engineering.py
python examples/03_model_training.py
python examples/04_backtesting.py
python examples/05_risk_management.py
```

### 3. Run Tests
```bash
pytest tests/
```

### 4. Read Documentation
- [README.md](README.md) - Main documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [WEB_DASHBOARD_SETUP.md](WEB_DASHBOARD_SETUP.md) - Dashboard details
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment options

## Pushing to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `CryptoSage`
3. Description: "Bitcoin Futures Trading System with Web Dashboard"
4. Choose: **Public**
5. Click "Create repository"

### Step 2: Configure Git Remote

Replace `YOUR_USERNAME` with your GitHub username:

```bash
cd /Users/phucbao/Documents/Binance

git remote add origin https://github.com/YOUR_USERNAME/CryptoSage.git
git branch -M main
git push -u origin main
```

### Step 3: Verify on GitHub

Visit: `https://github.com/YOUR_USERNAME/CryptoSage`

You should see all your files on GitHub!

## Using Your GitHub Repository

### Clone on Another Computer

```bash
git clone https://github.com/YOUR_USERNAME/CryptoSage.git
cd CryptoSage
pip install -e .
```

### Make Changes and Push

```bash
# Make changes to files
git add .
git commit -m "Description of changes"
git push
```

## Common Commands

### Stop the Servers

Press `Ctrl+C` in each terminal to stop the servers.

### View Logs

```bash
# Backend logs are printed to terminal
# Frontend logs are printed to terminal
```

### Check System Status

```bash
curl http://localhost:8000/api/status
```

### View API Documentation

```
http://localhost:8000/docs
```

(FastAPI automatically generates interactive API documentation)

## Performance Tips

- Use Chrome or Firefox for best performance
- Keep backend and frontend servers running
- Don't open too many browser tabs
- Monitor system resources if running backtests

## Security Notes

- Never commit `.env` file with real credentials
- Use environment variables for sensitive data
- In production, use HTTPS and authentication
- See DEPLOYMENT_GUIDE.md for production setup

## Getting Help

1. Check the troubleshooting section above
2. Read the documentation files
3. Review example scripts
4. Check browser console (F12) for errors
5. Check terminal output for error messages

## What's Next?

- Customize the dashboard styling
- Connect real Binance API credentials
- Run backtests with your strategy
- Paper trade to test your system
- Deploy to cloud (see DEPLOYMENT_GUIDE.md)

---

**You're all set! Enjoy using CryptoSage! 🚀**

