# Bitcoin Futures Trading Dashboard

A minimalist, black and white web-based dashboard for the Bitcoin Futures Trading System.

## Features

### 1. Overview Tab
- **Account Status**: Display balance, equity, unrealized P&L, margin ratio
- **System Status**: Show status of all system components
- **Equity Curve**: Real-time equity curve visualization
- **Recent Positions**: Table of current open positions

### 2. Data Tab
- **Data Collection Controls**: Start/stop data collection, select symbols and timeframes
- **Data Status**: Display collection status and record count
- **Feature Statistics**: Show engineered features breakdown

### 3. Models Tab
- **Model Status**: Display training status and metrics for both models
- **Current Predictions**: Show long-term and short-term predictions
- **Retrain Button**: Trigger model retraining

### 4. Backtest Tab
- **Backtest Configuration**: Set parameters for backtesting
- **Backtest Results**: Display comprehensive performance metrics
- **Equity Curve**: Visualize backtest equity curve
- **Trade History**: Table of all trades from backtest

### 5. Trading Tab
- **Trading Mode Selection**: Choose between paper, testnet, or live
- **Order Placement**: Place new orders with size and leverage
- **Current Positions**: View all open positions
- **Start/Stop Trading**: Control trading system

### 6. Risk Tab
- **Risk Metrics Calculator**: Calculate liquidation prices and risk metrics
- **Risk Analysis**: Display liquidation distance, max loss, funding costs
- **Position Sizing**: Show recommendations for different sizing strategies

## Design

- **Color Scheme**: Pure black and white (no colors)
- **Minimalist**: Clean, professional design without unnecessary decorations
- **Responsive**: Works on desktop and mobile devices
- **Charts**: Interactive charts using Chart.js

## Installation

### Prerequisites
- Python 3.10+
- Modern web browser

### Setup

1. **Install dependencies** (if not already done):
```bash
pip install -e .
```

2. **Start the backend API server** (in one terminal):
```bash
python -m src.api.server
```

The API will be available at `http://localhost:8000`

3. **Start the frontend server** (in another terminal):
```bash
cd frontend
python server.py
```

The dashboard will be available at `http://localhost:3000`

## Usage

### Accessing the Dashboard

Open your browser and navigate to:
```
http://localhost:3000
```

### Navigation

Use the navigation buttons at the top to switch between tabs:
- **Overview**: System overview and account status
- **Data**: Data collection and feature engineering
- **Models**: Model training and predictions
- **Backtest**: Backtesting and strategy analysis
- **Trading**: Live trading controls
- **Risk**: Risk management and position sizing

### Real-time Updates

The dashboard connects to the backend via WebSocket for real-time updates:
- Market data updates every second
- Trading updates every 2 seconds
- Automatic reconnection on disconnect

## API Endpoints

The frontend communicates with the backend API at `http://localhost:8000/api`:

### Health & Status
- `GET /health` - Health check
- `GET /api/status` - System status

### Data Collection
- `POST /api/data/collect` - Start data collection
- `GET /api/data/status` - Get collection status
- `GET /api/data/symbols` - Get available symbols

### Feature Engineering
- `POST /api/features/engineer` - Engineer features
- `GET /api/features/statistics` - Get feature statistics

### Models
- `POST /api/models/train` - Train models
- `GET /api/models/status` - Get model status
- `GET /api/models/predictions` - Get predictions

### Backtesting
- `POST /api/backtest/run` - Run backtest
- `GET /api/backtest/results` - Get results
- `GET /api/backtest/equity-curve` - Get equity curve
- `GET /api/backtest/trades` - Get trades

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
- `WS /ws/market-data` - Real-time market data
- `WS /ws/trading-updates` - Real-time trading updates

## File Structure

```
frontend/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # Stylesheet (black and white)
├── js/
│   └── app.js          # Main application logic
├── server.py           # Frontend HTTP server
└── README.md           # This file
```

## Customization

### Styling

Edit `css/style.css` to customize:
- Colors (currently black and white)
- Spacing and layout
- Typography
- Responsive breakpoints

### API Configuration

Edit `js/app.js` to change:
- API base URL: `const API_BASE_URL = 'http://localhost:8000/api'`
- WebSocket URLs
- Update intervals

## Troubleshooting

### Dashboard not loading
1. Check if frontend server is running: `http://localhost:3000`
2. Check browser console for errors (F12)
3. Verify backend API is running: `http://localhost:8000/health`

### API calls failing
1. Verify backend server is running on port 8000
2. Check CORS headers in browser console
3. Verify API endpoints are correct

### WebSocket not connecting
1. Check if backend server is running
2. Verify WebSocket URLs in `js/app.js`
3. Check browser console for connection errors

### Charts not displaying
1. Verify Chart.js is loaded from CDN
2. Check browser console for errors
3. Verify data is being loaded from API

## Performance Tips

1. **Reduce Update Frequency**: Modify WebSocket intervals in `app.js`
2. **Disable Charts**: Comment out chart initialization for faster loading
3. **Use Browser DevTools**: Monitor network and performance
4. **Cache Data**: Browser automatically caches static files

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Security Notes

⚠️ **Important**: This dashboard is designed for local development and testing.

For production deployment:
1. Use HTTPS instead of HTTP
2. Implement authentication and authorization
3. Add rate limiting and DDoS protection
4. Sanitize all user inputs
5. Use environment variables for sensitive data
6. Implement proper CORS policies

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Custom chart indicators
- [ ] Export data to CSV
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Strategy backtesting UI
- [ ] Real-time notifications
- [ ] User authentication

## Support

For issues or questions:
1. Check the main README.md
2. Review ARCHITECTURE.md for system design
3. Check browser console for errors
4. Review backend logs

## License

Same as main project

