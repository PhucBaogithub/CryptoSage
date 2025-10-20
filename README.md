# CryptoSage - Bitcoin Futures Trading System

A comprehensive, production-grade system for Bitcoin price prediction and automated futures trading on Binance with a modern web dashboard.

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip install -e .
```

### 2. Start Backend API (Terminal 1)
```bash
python -m src.api.server
```

### 3. Start Frontend Server (Terminal 2)
```bash
cd frontend
python server.py
```

### 4. Open Dashboard
Open your browser to: **http://localhost:3000**

## 📊 Features

### Core Trading System
- **Long-term Price Prediction**: Temporal Fusion Transformer for daily/weekly/monthly forecasts
- **Short-term Trading Signals**: Transformer-based buy/sell signals for intraday trading
- **Automated Futures Trading**: Binance Futures API integration with paper/testnet/live modes
- **Risk Management**: Liquidation prevention, position sizing, funding optimization
- **Comprehensive Backtesting**: Walk-forward analysis with realistic simulation
- **Feature Engineering**: 50+ technical indicators and advanced features

### Web Dashboard
- **Minimalist black and white interface** for monitoring and control
- **6 Dashboard Tabs**: Overview, Data, Models, Backtest, Trading, Risk
- **Real-time Charts**: Equity curves, price movements, performance metrics
- **Account Monitoring**: Balance, equity, P&L tracking
- **Trading Controls**: Paper, testnet, and live trading modes
- **REST API**: 20+ endpoints with WebSocket support
- **Responsive Design**: Works on desktop, tablet, and mobile

### Data Pipeline
- **Multi-source data collection**: OHLCV, funding rates, open interest, order book
- **Efficient storage**: Parquet format with caching
- **Multiple timeframes**: 1m, 5m, 15m, 1h, 4h, 1d

## 📁 Project Structure

```
CryptoSage/
├── src/
│   ├── api/                     # FastAPI backend
│   ├── data/                    # Data collection and management
│   ├── features/                # Feature engineering
│   ├── models/                  # ML models (long-term & short-term)
│   ├── backtesting/             # Backtesting framework
│   ├── risk_management/         # Risk management
│   ├── execution/               # Order execution
│   ├── monitoring/              # Monitoring and metrics
│   └── utils/                   # Utilities
├── frontend/                    # Web dashboard
│   ├── index.html              # Dashboard HTML
│   ├── css/style.css           # Styling
│   ├── js/app.js               # Application logic
│   └── server.py               # Frontend server
├── tests/                       # Test suite
├── config/                      # Configuration
├── data/                        # Data storage
├── examples/                    # Example scripts
├── logs/                        # Log files
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## 📋 Installation & Setup

### Prerequisites
- Python 3.10+
- pip or conda

### Step 1: Install Dependencies
```bash
pip install -e .
```

### Step 2: Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env with your Binance API credentials (optional for testing)
```

### Step 3: Run the Web Dashboard

**Terminal 1 - Start Backend API:**
```bash
python -m src.api.server
```
Expected output: `INFO: Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Start Frontend Server:**
```bash
cd frontend
python server.py
```
Expected output: `Frontend server running at http://0.0.0.0:3000`

**Terminal 3 - Open Dashboard:**
```bash
# Open in your browser:
http://localhost:3000
```

## 🎯 Dashboard Features

### Overview Tab
- Account balance and equity
- System status indicator
- Equity curve chart
- Current positions

### Data Tab
- Start/stop data collection
- Symbol and timeframe selection
- Collection status
- Feature statistics

### Models Tab
- Model training status
- Accuracy metrics
- Current predictions
- Retrain button

### Backtest Tab
- Backtest configuration
- Performance metrics
- Equity curve visualization
- Trade history

### Trading Tab
- Trading mode selection (paper/testnet/live)
- Order placement
- Current positions
- Start/stop controls

### Risk Tab
- Risk metrics calculator
- Liquidation price calculation
- Position sizing recommendations
- Funding cost analysis

## 🔧 Configuration

Edit `config/config.yaml` to customize:
- Binance API settings
- Data collection parameters
- Model hyperparameters
- Risk management limits
- Backtesting parameters
- Execution mode (paper/testnet/live)

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=src
```

## 📚 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and design
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment instructions
- [WEB_DASHBOARD_SETUP.md](WEB_DASHBOARD_SETUP.md) - Dashboard setup and API reference
- [frontend/README.md](frontend/README.md) - Frontend documentation

## 🚀 Deploying to GitHub

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `CryptoSage`
3. Description: "Bitcoin Futures Trading System with Web Dashboard"
4. Choose visibility: **Public**
5. Click "Create repository"

### Step 2: Configure Git Remote
Replace `YOUR_USERNAME` with your GitHub username:
```bash
git remote add origin https://github.com/YOUR_USERNAME/CryptoSage.git
git branch -M main
git push -u origin main
```

### Step 3: Verify on GitHub
Visit: `https://github.com/YOUR_USERNAME/CryptoSage`

## 📊 API Endpoints

### Health & Status
- `GET /health` - Health check
- `GET /api/status` - System status

### Data Collection
- `POST /api/data/collect` - Start data collection
- `GET /api/data/status` - Get collection status
- `GET /api/data/symbols` - Get available symbols

### Models
- `POST /api/models/train` - Train models
- `GET /api/models/status` - Get training status
- `GET /api/models/predictions` - Get predictions

### Backtesting
- `POST /api/backtest/run` - Run backtest
- `GET /api/backtest/results` - Get results
- `GET /api/backtest/equity-curve` - Get equity curve
- `GET /api/backtest/trades` - Get trade history

### Trading
- `POST /api/trading/start` - Start trading
- `POST /api/trading/stop` - Stop trading
- `POST /api/trading/place-order` - Place order
- `GET /api/trading/positions` - Get positions
- `GET /api/trading/account` - Get account info

### Risk Management
- `POST /api/risk/metrics` - Calculate risk metrics
- `GET /api/risk/position-sizing` - Get position sizing

### WebSocket
- `WS /ws/market-data` - Market data stream
- `WS /ws/trading-updates` - Trading updates stream

## ⚠️ Important Warnings

**Risk Disclaimer**:
- Cryptocurrency markets are highly volatile
- Past performance does not guarantee future results
- Models can overfit historical data
- Funding costs and slippage can turn profitable signals into losses
- **Always backtest thoroughly before live trading**
- **Start with paper trading and small positions**
- **Use appropriate leverage limits and stop losses**

## ✅ Best Practices

1. Always backtest with realistic parameters
2. Use walk-forward analysis to avoid look-ahead bias
3. Monitor data drift and retrain models regularly
4. Start with paper trading before going live
5. Use conservative leverage (1-3x recommended)
6. Monitor funding rates and adjust positions accordingly
7. Implement circuit breakers for risk management
8. Log all trades for analysis and compliance

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review example scripts in `examples/` directory

---

**Built with production-grade code quality and comprehensive documentation.**

**Ready to trade? Start with the Quick Start section above! 🚀**

