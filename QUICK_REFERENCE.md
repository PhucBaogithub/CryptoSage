# CryptoSage - Quick Reference Guide

## 🚀 Quick Start (Copy & Paste)

### Terminal 1: Install & Start Backend
```bash
cd /Users/phucbao/Documents/Binance
pip install -e .
python -m src.api.server
```

### Terminal 2: Start Frontend
```bash
cd /Users/phucbao/Documents/Binance/frontend
python server.py
```

### Terminal 3: Open Dashboard
```
http://localhost:3000
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Main documentation & features |
| **GETTING_STARTED.md** | Step-by-step setup guide |
| **GITHUB_DEPLOYMENT.md** | Push to GitHub instructions |
| **ARCHITECTURE.md** | System design & architecture |
| **DEPLOYMENT_GUIDE.md** | Production deployment options |
| **WEB_DASHBOARD_SETUP.md** | Dashboard API reference |

## 🔧 Common Commands

### Installation
```bash
pip install -e .                    # Install dependencies
pip install -e ".[dev,data]"        # Install with dev tools
```

### Running the System
```bash
python -m src.api.server            # Start backend API
cd frontend && python server.py     # Start frontend
pytest tests/                       # Run tests
pytest tests/ --cov=src            # Run tests with coverage
```

### Git Commands
```bash
git status                          # Check status
git add .                           # Stage changes
git commit -m "message"             # Commit changes
git push                            # Push to GitHub
git log --oneline                   # View commit history
```

## 🌐 Pushing to GitHub

### One-Time Setup
```bash
# 1. Create repository at https://github.com/new
# 2. Name it: CryptoSage
# 3. Make it Public
# 4. Click Create

# 5. Configure remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/CryptoSage.git
git branch -M main
git push -u origin main
```

### After Making Changes
```bash
git add .
git commit -m "Description of changes"
git push
```

## 🎯 Dashboard Features

| Tab | Features |
|-----|----------|
| **Overview** | Account status, equity curve, positions |
| **Data** | Collect data, view statistics |
| **Models** | Train models, view predictions |
| **Backtest** | Run backtests, view results |
| **Trading** | Place orders, manage positions |
| **Risk** | Calculate metrics, position sizing |

## 🔌 API Endpoints

```
Health:           GET /health
Status:           GET /api/status
Data:             POST /api/data/collect
Models:           POST /api/models/train
Backtest:         POST /api/backtest/run
Trading:          POST /api/trading/start
Risk:             POST /api/risk/metrics
WebSocket:        WS /ws/market-data
```

## 📊 Project Structure

```
CryptoSage/
├── src/
│   ├── api/              # FastAPI backend
│   ├── data/             # Data collection
│   ├── features/         # Feature engineering
│   ├── models/           # ML models
│   ├── backtesting/      # Backtesting
│   ├── risk_management/  # Risk management
│   ├── execution/        # Order execution
│   ├── monitoring/       # Monitoring
│   └── utils/            # Utilities
├── frontend/             # Web dashboard
├── tests/                # Test suite
├── config/               # Configuration
├── examples/             # Example scripts
└── README.md             # Main documentation
```

## ⚠️ Important Notes

- **Never commit .env** with real credentials
- **Always backtest** before live trading
- **Start with paper trading** before going live
- **Use conservative leverage** (1-3x recommended)
- **Monitor funding rates** and liquidation risks

## 🆘 Troubleshooting

### Port Already in Use
```bash
lsof -i :8000
kill -9 <PID>
```

### API Not Responding
```bash
curl http://localhost:8000/health
```

### Dashboard Not Loading
- Check if both servers are running
- Open browser console (F12) for errors
- Verify URL is http://localhost:3000

### Git Authentication Failed
- Use personal access token (not password)
- Get token at: https://github.com/settings/tokens

## 📋 Checklist

- [ ] Install dependencies: `pip install -e .`
- [ ] Start backend: `python -m src.api.server`
- [ ] Start frontend: `cd frontend && python server.py`
- [ ] Open dashboard: `http://localhost:3000`
- [ ] Test all tabs and features
- [ ] Create GitHub repository
- [ ] Push to GitHub: `git push -u origin main`
- [ ] Verify on GitHub
- [ ] Share repository link

## 🔗 Useful Links

- GitHub: https://github.com/YOUR_USERNAME/CryptoSage
- Dashboard: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Binance API: https://binance-docs.github.io/apidocs/

## 📞 Quick Help

**Q: How do I run the dashboard?**
A: Follow the Quick Start section above (3 terminals)

**Q: How do I push to GitHub?**
A: Follow the "Pushing to GitHub" section above

**Q: Where's the API documentation?**
A: See WEB_DASHBOARD_SETUP.md or visit http://localhost:8000/docs

**Q: How do I configure Binance API?**
A: Edit .env file with your credentials (optional for testing)

**Q: Can I deploy to production?**
A: Yes, see DEPLOYMENT_GUIDE.md for options

## 🎓 Learning Path

1. Read README.md (overview)
2. Follow GETTING_STARTED.md (setup)
3. Explore the dashboard
4. Read ARCHITECTURE.md (how it works)
5. Run example scripts
6. Read WEB_DASHBOARD_SETUP.md (API details)
7. Deploy to GitHub (GITHUB_DEPLOYMENT.md)
8. Deploy to production (DEPLOYMENT_GUIDE.md)

## 🚀 Next Steps

1. **Today**: Get dashboard running locally
2. **This Week**: Explore features, run examples
3. **This Month**: Push to GitHub, customize
4. **Next 3 Months**: Add features, deploy, trade

---

**Everything you need is in this repository. Start with GETTING_STARTED.md! 🎉**

