# 🚀 Start Here: Web Dashboard Guide

Welcome to the Bitcoin Futures Trading System with Web Dashboard!

This guide will help you get started quickly.

## 📋 What You Have

A complete, production-ready Bitcoin trading system with:
- **Backend API**: 20+ REST endpoints + WebSocket
- **Web Dashboard**: Minimalist black and white interface
- **Trading System**: Data pipeline, ML models, backtesting, risk management
- **Documentation**: Comprehensive guides for setup and deployment
- **Git Repository**: Ready to push to GitHub

## ⚡ Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
cd /Users/phucbao/Documents/Binance
pip install -e .
```

### 2. Start Backend API (Terminal 1)
```bash
python -m src.api.server
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Start Frontend Server (Terminal 2)
```bash
cd frontend
python server.py
```

Expected output:
```
Frontend server running at http://0.0.0.0:3000
```

### 4. Open Dashboard
Open your browser to:
```
http://localhost:3000
```

## 📚 Documentation Guide

### For Setup & Configuration
👉 **[WEB_DASHBOARD_SETUP.md](WEB_DASHBOARD_SETUP.md)**
- Complete setup instructions
- API endpoint documentation
- WebSocket usage
- Customization guide
- Troubleshooting

### For Deployment
👉 **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**
- Local development
- Docker deployment
- AWS, Heroku, Google Cloud
- Monitoring and maintenance
- Security checklist

### For GitHub
👉 **[PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md)**
- Step-by-step GitHub setup
- Git configuration
- Pushing to GitHub
- SSH setup
- Troubleshooting

### For Frontend Details
👉 **[frontend/README.md](frontend/README.md)**
- Dashboard features
- API reference
- Customization
- Browser support

### For System Overview
👉 **[README.md](README.md)**
- Main documentation
- System architecture
- Features overview
- Configuration

## 🎯 Dashboard Features

### Overview Tab
- Account balance and equity
- System status
- Equity curve chart
- Current positions

### Data Tab
- Start/stop data collection
- Select symbols and timeframes
- View collection status
- Feature statistics

### Models Tab
- Model training status
- Accuracy and loss metrics
- Current predictions
- Retrain button

### Backtest Tab
- Configure backtest parameters
- View results and metrics
- Equity curve visualization
- Trade history table

### Trading Tab
- Select trading mode (paper/testnet/live)
- Place orders
- View current positions
- Start/stop trading

### Risk Tab
- Calculate risk metrics
- View liquidation prices
- Position sizing recommendations
- Funding cost analysis

## 🔌 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Account Info
```bash
curl http://localhost:8000/api/trading/account
```

### Get Model Status
```bash
curl http://localhost:8000/api/models/status
```

### Run Backtest
```bash
curl -X POST http://localhost:8000/api/backtest/run \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "timeframe": "1h",
    "start_date": "2024-01-01",
    "end_date": "2024-10-20",
    "initial_capital": 100000
  }'
```

See [WEB_DASHBOARD_SETUP.md](WEB_DASHBOARD_SETUP.md) for complete API documentation.

## 🐳 Docker Deployment

```bash
# Build image
docker build -t bitcoin-trading .

# Run container
docker run -d -p 8000:8000 -p 3000:3000 bitcoin-trading

# View logs
docker logs -f <container_id>
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for more options.

## 🌐 Push to GitHub

```bash
# 1. Create repository on GitHub
# Go to https://github.com/new

# 2. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/bitcoin-futures-trading.git

# 3. Push to GitHub
git branch -M main
git push -u origin main
```

See [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md) for detailed instructions.

## 🧪 Testing

### Run Examples
```bash
python examples/01_data_collection.py
python examples/02_feature_engineering.py
python examples/03_model_training.py
python examples/04_backtesting.py
python examples/05_risk_management.py
```

### Run Tests
```bash
pytest tests/
pytest tests/ --cov=src
```

## ⚙️ Configuration

Edit `.env` with your settings:
```bash
cp .env.example .env
# Edit .env with your Binance API credentials
```

Edit `config/config.yaml` for system configuration.

## 🔧 Troubleshooting

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
1. Check if frontend server is running
2. Open browser console (F12) for errors
3. Verify API URL in `frontend/js/app.js`

See [WEB_DASHBOARD_SETUP.md](WEB_DASHBOARD_SETUP.md) for more troubleshooting.

## 📊 Project Structure

```
bitcoin-futures-trading/
├── src/
│   ├── api/              # FastAPI backend
│   ├── data/             # Data pipeline
│   ├── features/         # Feature engineering
│   ├── models/           # ML models
│   ├── backtesting/      # Backtesting
│   ├── execution/        # Order execution
│   ├── risk_management/  # Risk management
│   ├── monitoring/       # Monitoring
│   └── utils/            # Utilities
├── frontend/             # Web dashboard
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   └── server.py
├── examples/             # Example scripts
├── tests/                # Test suite
├── config/               # Configuration
└── docs/                 # Documentation
```

## 📖 Reading Order

1. **This file** (you are here)
2. [WEB_DASHBOARD_SETUP.md](WEB_DASHBOARD_SETUP.md) - Setup guide
3. [frontend/README.md](frontend/README.md) - Frontend details
4. [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment
5. [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md) - GitHub setup
6. [README.md](README.md) - Full documentation

## ⚠️ Important Notes

### Before Live Trading
1. ✅ Thoroughly backtest your strategy
2. ✅ Paper trade for at least 1 week
3. ✅ Test on testnet with small amounts
4. ✅ Monitor funding rates and liquidation risks
5. ✅ Start with 1x leverage
6. ✅ Use stop losses and position limits

### Security
- Use HTTPS in production
- Implement authentication
- Add rate limiting
- Use environment variables for secrets
- Enable proper CORS policies

## 🎓 Next Steps

### Immediate (Today)
1. ✅ Install dependencies
2. ✅ Start backend and frontend
3. ✅ Test dashboard at http://localhost:3000
4. ✅ Explore all tabs and features

### Short Term (This Week)
1. Read [WEB_DASHBOARD_SETUP.md](WEB_DASHBOARD_SETUP.md)
2. Customize dashboard styling
3. Run example scripts
4. Test API endpoints

### Medium Term (This Month)
1. Follow [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md)
2. Create GitHub repository
3. Deploy to cloud platform
4. Set up monitoring

### Long Term (Next 3 Months)
1. Add authentication
2. Connect real Binance API
3. Run backtests
4. Paper trade
5. Testnet trading
6. Live trading (carefully!)

## 📞 Support

### Documentation
- [WEB_DASHBOARD_SETUP.md](WEB_DASHBOARD_SETUP.md) - Setup guide
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment
- [frontend/README.md](frontend/README.md) - Frontend
- [README.md](README.md) - Full docs

### Troubleshooting
- Check browser console (F12)
- Check backend logs
- Review API documentation
- Check troubleshooting sections

### Resources
- [Binance API Docs](https://binance-docs.github.io/apidocs/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Chart.js Docs](https://www.chartjs.org/docs/)

## 🎉 You're Ready!

Everything is set up and ready to use. Start by:

1. **Install**: `pip install -e .`
2. **Start Backend**: `python -m src.api.server`
3. **Start Frontend**: `cd frontend && python server.py`
4. **Open Dashboard**: `http://localhost:3000`

---

**Questions? Check the documentation or troubleshooting guides.**

**Ready to deploy? Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).**

**Ready for GitHub? Follow [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md).**

---

**Good luck with your trading system! 🚀**

