# Web Dashboard Setup Guide

Complete guide to set up and run the Bitcoin Futures Trading System web dashboard.

## Overview

The web dashboard consists of:
- **Backend API**: FastAPI server on port 8000
- **Frontend**: HTML/CSS/JavaScript on port 3000
- **WebSocket**: Real-time updates via WebSocket

## Prerequisites

- Python 3.10+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Project dependencies installed: `pip install -e .`

## Quick Start (5 Minutes)

### Terminal 1: Start Backend API

```bash
cd /Users/phucbao/Documents/Binance
python -m src.api.server
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start Frontend Server

```bash
cd /Users/phucbao/Documents/Binance/frontend
python server.py
```

Expected output:
```
Frontend server running at http://0.0.0.0:3000
Serving files from: /Users/phucbao/Documents/Binance/frontend
```

### Terminal 3: Open Dashboard

Open your browser and navigate to:
```
http://localhost:3000
```

## Detailed Setup

### Step 1: Install Dependencies

```bash
cd /Users/phucbao/Documents/Binance
pip install -e .
```

Required packages:
- fastapi>=0.100.0
- uvicorn>=0.23.0
- pydantic>=2.0.0
- python-binance>=1.0.17
- pandas>=2.0.0
- numpy>=1.24.0
- torch>=2.0.0
- loguru>=0.7.0

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_PORT=3000
```

### Step 3: Start Backend API

```bash
python -m src.api.server
```

Or with custom settings:
```bash
python -c "from src.api.server import start_server; start_server(host='0.0.0.0', port=8000, reload=True)"
```

### Step 4: Start Frontend Server

```bash
cd frontend
python server.py
```

Or with custom port:
```bash
python -c "from server import start_frontend_server; start_frontend_server(port=3000)"
```

### Step 5: Access Dashboard

Open browser to: `http://localhost:3000`

## Dashboard Features

### Overview Tab
- Account balance and equity
- System status
- Equity curve chart
- Current positions table

### Data Tab
- Start/stop data collection
- Select symbols and timeframes
- View collection status
- Feature statistics

### Models Tab
- Model training status
- Model accuracy and loss
- Current predictions
- Retrain button

### Backtest Tab
- Configure backtest parameters
- View backtest results
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

## API Endpoints

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

### Calculate Risk Metrics
```bash
curl -X POST http://localhost:8000/api/risk/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "entry_price": 45000,
    "current_price": 46000,
    "position_size_usd": 50000,
    "leverage": 3.0,
    "funding_rate": 0.0001,
    "volatility": 0.25
  }'
```

## WebSocket Connections

### Market Data Stream
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market-data');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Market data:', data);
};
```

### Trading Updates Stream
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/trading-updates');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Trading update:', data);
};
```

## Customization

### Change API Port

Edit `src/api/server.py`:
```python
if __name__ == "__main__":
    start_server(host="0.0.0.0", port=8001)  # Change port here
```

### Change Frontend Port

Edit `frontend/server.py`:
```python
if __name__ == '__main__':
    start_frontend_server(port=3001)  # Change port here
```

### Change API Base URL

Edit `frontend/js/app.js`:
```javascript
const API_BASE_URL = 'http://localhost:8001/api';  // Change URL here
```

### Customize Styling

Edit `frontend/css/style.css` to modify:
- Colors (currently black and white)
- Spacing and layout
- Typography
- Responsive breakpoints

## Troubleshooting

### Port Already in Use

If port 8000 or 3000 is already in use:

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### API Not Responding

1. Check if backend is running:
```bash
curl http://localhost:8000/health
```

2. Check logs for errors
3. Verify firewall settings

### Dashboard Not Loading

1. Check if frontend server is running
2. Open browser console (F12) for errors
3. Verify API URL in `frontend/js/app.js`

### WebSocket Connection Failed

1. Verify backend is running
2. Check WebSocket URLs in `frontend/js/app.js`
3. Check browser console for errors

### CORS Errors

The API has CORS enabled for all origins. If still getting errors:

1. Check browser console for specific error
2. Verify API is running
3. Try accessing API directly: `http://localhost:8000/api/status`

## Production Deployment

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -e .

EXPOSE 8000 3000

CMD ["sh", "-c", "python -m src.api.server & cd frontend && python server.py"]
```

Build and run:
```bash
docker build -t bitcoin-trading-dashboard .
docker run -p 8000:8000 -p 3000:3000 bitcoin-trading-dashboard
```

### Using Nginx

Create `nginx.conf`:
```nginx
upstream api {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name your-domain.com;

    location /api {
        proxy_pass http://api;
    }

    location / {
        proxy_pass http://frontend;
    }
}
```

### Using Systemd

Create `/etc/systemd/system/bitcoin-trading.service`:
```ini
[Unit]
Description=Bitcoin Trading Dashboard
After=network.target

[Service]
Type=simple
User=trading
WorkingDirectory=/home/trading/bitcoin-futures-trading
ExecStart=/usr/bin/python3 -m src.api.server
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable bitcoin-trading
sudo systemctl start bitcoin-trading
```

## Performance Optimization

### Backend
1. Use production ASGI server (Gunicorn + Uvicorn)
2. Enable caching for API responses
3. Use database for data storage
4. Implement rate limiting

### Frontend
1. Minify CSS and JavaScript
2. Enable gzip compression
3. Use CDN for static files
4. Implement lazy loading

### General
1. Use connection pooling
2. Implement caching strategies
3. Monitor performance metrics
4. Use load balancing

## Security Considerations

⚠️ **Important**: This setup is for development/testing only.

For production:
1. Use HTTPS instead of HTTP
2. Implement authentication
3. Add rate limiting
4. Sanitize user inputs
5. Use environment variables for secrets
6. Implement proper CORS policies
7. Add request validation
8. Use secure WebSocket (WSS)

## Monitoring

### Check API Health
```bash
curl http://localhost:8000/health
```

### View API Logs
```bash
# Logs are printed to console
# For file logging, modify src/utils/logger.py
```

### Monitor System Resources
```bash
# CPU and memory usage
top

# Network connections
netstat -an | grep 8000
```

## Next Steps

1. **Customize Dashboard**: Modify styling and layout
2. **Add Authentication**: Implement user login
3. **Connect Real Data**: Integrate with actual Binance API
4. **Deploy**: Use Docker or cloud platform
5. **Monitor**: Set up monitoring and alerting

## Support

For issues:
1. Check browser console (F12)
2. Check backend logs
3. Review API documentation
4. Check frontend/README.md
5. Review main README.md

## File Structure

```
/Users/phucbao/Documents/Binance/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── server.py          # FastAPI backend
│   └── ...
├── frontend/
│   ├── index.html             # Main HTML
│   ├── css/
│   │   └── style.css          # Styling
│   ├── js/
│   │   └── app.js             # Application logic
│   ├── server.py              # Frontend HTTP server
│   └── README.md              # Frontend docs
└── WEB_DASHBOARD_SETUP.md     # This file
```

---

**Your web dashboard is ready to use! 🚀**

