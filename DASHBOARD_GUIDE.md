# 📊 CryptoSage Dashboard - Complete Guide

## 🎨 New Features

### ✨ White Theme Design
- Modern, clean white background (#ffffff)
- Professional blue accent color (#3498db)
- Responsive design for all devices
- Smooth gradients and shadows

### 📈 15+ New Charts
The dashboard now includes comprehensive visualizations across all tabs:

#### Overview Tab
- **Equity Curve**: Track your portfolio growth over time
- **Daily Returns**: Visualize daily profit/loss percentages
- **Win Rate**: Pie chart showing winning vs losing trades
- **Drawdown Analysis**: Monitor maximum drawdown periods

#### Data Tab
- **Data Distribution**: Histogram of data points across ranges
- **Coin Price Comparison**: Multi-coin price trends (BTC, ETH, BNB)
- **Available Coins**: 12 cryptocurrencies to choose from

#### Models Tab
- **Long-term Predictions**: 30-day price forecasts
- **Short-term Predictions**: 24-hour price predictions
- **Model Performance**: Radar chart of accuracy metrics
- **Training History**: Training and validation loss curves

#### Backtest Tab
- **Equity Curve**: Backtest portfolio growth
- **Monthly Returns**: Monthly performance breakdown
- **Performance Metrics**: Win rate, profit factor, average trade
- **Risk Metrics**: Sortino ratio, Calmar ratio, recovery factor

#### Trading Tab
- **Position Distribution**: Pie chart of open positions
- **Real-time P&L**: Live profit/loss tracking
- **Trading Activity**: Hourly trade count
- **Current Positions**: Active trades table

#### Risk Tab
- **Risk Gauge**: Overall risk level indicator
- **Liquidation Risk**: Distance to liquidation over time
- **Funding Cost Analysis**: Daily funding costs
- **Risk Metrics Calculator**: Real-time risk calculations

## 🚀 Getting Started

### 1. Start the Backend
```bash
cd /Users/phucbao/Documents/Binance
python3 -m src.api.server
```
Backend runs on: http://localhost:8000

### 2. Start the Frontend
```bash
cd /Users/phucbao/Documents/Binance
python3 frontend/server.py
```
Frontend runs on: http://localhost:3000

### 3. Access the Dashboard
Open your browser and go to: **http://localhost:3000**

## 📱 Dashboard Tabs

### Overview
- Quick summary of trading performance
- 4 key charts showing equity, returns, win rate, and drawdown
- Real-time system status

### Data
- Select multiple cryptocurrencies (12 available)
- View data distribution and price comparisons
- Collect market data for analysis

### Models
- Train ML models for price prediction
- View long-term and short-term predictions
- Monitor model performance metrics
- Track training history

### Backtest
- Run backtests on historical data
- Select symbol, timeframe, and date range
- View detailed performance and risk metrics
- Analyze monthly returns

### Trading
- Start/stop automated trading
- Place manual orders
- Monitor current positions
- View real-time P&L and trading activity

### Risk
- Calculate liquidation prices
- Monitor funding costs
- Get position sizing recommendations
- Track distance to liquidation

## 🎯 Key Features

### Multi-Coin Support
Select from 12 cryptocurrencies:
- BTCUSDT (Bitcoin)
- ETHUSDT (Ethereum)
- BNBUSDT (Binance Coin)
- SOLUSDT (Solana)
- XRPUSDT (Ripple)
- ADAUSDT (Cardano)
- DOGEUSDT (Dogecoin)
- MATICUSDT (Polygon)
- LINKUSDT (Chainlink)
- LTCUSDT (Litecoin)
- AVAXUSDT (Avalanche)
- UNIUSDT (Uniswap)

### Real-time Updates
- WebSocket connection for live market data
- Real-time P&L tracking
- Live position updates
- Instant order execution feedback

### Risk Management
- Liquidation price calculator
- Funding cost analyzer
- Position sizing recommendations
- Risk gauge indicator

## 🔧 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
Visit: http://localhost:8000/docs

### Available Endpoints
- `/api/status` - System status
- `/api/data/collect` - Collect market data
- `/api/models/train` - Train models
- `/api/backtest/run` - Run backtest
- `/api/trading/start` - Start trading
- `/api/trading/stop` - Stop trading
- `/api/risk/metrics` - Calculate risk metrics

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Kill existing processes
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Try again
python3 -m src.api.server
```

### Frontend won't start
```bash
# Kill existing processes
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Try again
python3 frontend/server.py
```

### Charts not showing
- Refresh the page (Cmd+R or Ctrl+R)
- Check browser console for errors (F12)
- Ensure backend is running

## 📚 Documentation

- **README.md** - Project overview
- **ARCHITECTURE.md** - System design
- **DEPLOYMENT_GUIDE.md** - Production deployment
- **WEB_DASHBOARD_SETUP.md** - API reference

## 🌐 GitHub Repository

**Repository**: https://github.com/PhucBaogithub/CryptoSage

### Push Updates
```bash
cd /Users/phucbao/Documents/Binance
git add .
git commit -m "Your message"
git push origin main
```

## 💡 Tips

1. **Use Chrome/Firefox** for best compatibility
2. **Refresh page** if charts don't load immediately
3. **Check console** (F12) for any JavaScript errors
4. **Monitor logs** in terminal for backend issues
5. **Test with paper trading** before live trading

## 🎉 You're All Set!

Your CryptoSage dashboard is now:
- ✅ Running with white theme
- ✅ Displaying 15+ charts
- ✅ Supporting 12 cryptocurrencies
- ✅ Ready for trading and analysis
- ✅ Deployed on GitHub

**Happy Trading! 🚀**

