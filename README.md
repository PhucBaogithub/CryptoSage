# Bitcoin Futures Trading System

A comprehensive, production-grade system for Bitcoin price prediction and automated futures trading on Binance.

## Features

### 1. Long-term Price Prediction
- **Temporal Fusion Transformer (TFT)** for multi-horizon forecasting
- Predicts daily, weekly, and monthly price movements
- Outputs probabilistic forecasts (mean, std, skew)
- Interpretable attention mechanisms

### 2. Short-term Trading Signals
- **Transformer-based** signal generation for intraday trading
- Generates buy/sell/neutral signals with confidence scores
- Optimized for 5-minute to 1-hour timeframes
- Real-time inference capability

### 3. Automated Futures Trading
- **Binance Futures API** integration
- Support for paper trading, testnet, and live trading
- Automatic position sizing and leverage management
- Funding rate optimization

### 4. Risk Management
- **Liquidation prevention** with probability estimation
- **Volatility-aware position sizing** (Kelly Criterion, Fixed Fraction, Volatility-Adjusted)
- **Funding cost optimization**
- **Circuit breakers** and drawdown limits
- Real-time risk metrics

### 5. Comprehensive Backtesting
- **Walk-forward analysis** with time-series cross-validation
- Realistic simulation including:
  - Slippage modeling
  - Maker/taker fees
  - Funding payments
  - Leverage limits
  - Liquidation mechanics
- Detailed performance metrics (Sharpe, Sortino, Calmar ratios)

### 6. Feature Engineering
- **Price features**: Log returns, momentum, ROC
- **Technical indicators**: RSI, MACD, Bollinger Bands, ATR, ADX, EMA, SMA
- **Liquidity features**: Volume analysis, OBV, VROC
- **Volatility features**: Historical, Parkinson, Garman-Klass
- **Derivatives features**: Funding rates, Open Interest
- **Trend features**: Direction, Higher Highs/Lower Lows

### 7. Web Dashboard
- **Minimalist black and white interface** for monitoring and control
- **Real-time charts** for equity curves and price movements
- **Account monitoring** with balance, equity, and P&L tracking
- **Trading controls** for paper, testnet, and live modes
- **Risk management** interface with liquidation and position sizing
- **REST API** with WebSocket support for real-time updates
- **Responsive design** for desktop and mobile

### 8. Data Pipeline
- **Multi-source data collection**:
  - OHLCV data (1m, 5m, 15m, 1h, 4h, 1d)
  - Funding rates and Open Interest
  - Order book snapshots
  - Trade ticks
- **Efficient storage** with Parquet format
- **Caching** for fast retrieval

### 8. Production Monitoring
- **Prometheus metrics** for system monitoring
- **Data drift detection**
- **Model performance tracking**
- **Real-time alerts** for risk events

## Project Structure

```
btc-futures-trading/
├── src/
│   ├── __init__.py
│   ├── data/                    # Data collection and management
│   │   ├── binance_client.py   # Binance API client
│   │   └── data_manager.py     # Data storage and retrieval
│   ├── features/                # Feature engineering
│   │   └── feature_engineer.py # Feature extraction
│   ├── models/                  # ML models
│   │   ├── base_model.py       # Base model class
│   │   ├── long_term_model.py  # Long-term prediction
│   │   └── short_term_model.py # Short-term signals
│   ├── backtesting/             # Backtesting framework
│   │   ├── backtest_engine.py  # Backtest simulator
│   │   └── metrics.py          # Performance metrics
│   ├── risk_management/         # Risk management
│   │   ├── risk_manager.py     # Risk calculations
│   │   └── position_sizer.py   # Position sizing
│   ├── execution/               # Order execution
│   │   └── order_executor.py   # Order placement
│   ├── monitoring/              # Monitoring and metrics
│   │   └── metrics_collector.py # Prometheus metrics
│   └── utils/                   # Utilities
│       ├── config.py           # Configuration management
│       ├── logger.py           # Logging setup
│       └── time_utils.py       # Time utilities
├── tests/                       # Test suite
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── config/
│   └── config.yaml             # Configuration file
├── data/                        # Data storage
│   ├── raw/                    # Raw data
│   ├── processed/              # Processed data
│   └── cache/                  # Cached data
├── logs/                        # Log files
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## Installation

### Prerequisites
- Python 3.10+
- pip or conda

### Setup

1. Clone the repository:
```bash
cd /Users/phucbao/Documents/Binance
```

2. Install dependencies:
```bash
pip install -e .
```

3. Install optional dependencies for advanced features:
```bash
pip install -e ".[dev,data]"
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Binance API credentials
```

## Quick Start

### 1. Data Collection

```python
from src.data import BinanceDataClient, DataManager
from src.utils import Config

# Initialize
config = Config()
client = BinanceDataClient(
    api_key=config.get("binance.api_key"),
    api_secret=config.get("binance.api_secret"),
    testnet=config.get("binance.testnet"),
)
data_manager = DataManager()

# Collect historical data
df = client.get_klines("BTCUSDT", "1h", limit=1000)
data_manager.save_klines("BTCUSDT", "1h", df)
```

### 2. Feature Engineering

```python
from src.features import FeatureEngineer

engineer = FeatureEngineer()
df_features = engineer.engineer_features(df)
```

### 3. Model Training

```python
from src.models import LongTermModel

config = {
    "input_size": 50,
    "hidden_size": 64,
    "num_heads": 4,
    "num_layers": 2,
    "output_length": 30,
    "input_length": 168,
    "batch_size": 32,
    "epochs": 100,
}

model = LongTermModel(config)
history = model.train(X_train, y_train, X_val, y_val)
```

### 4. Backtesting

```python
from src.backtesting import BacktestEngine

engine = BacktestEngine(
    initial_capital=100000,
    leverage=3,
    taker_fee=0.0004,
)

metrics = engine.run(data, signal_generator, position_sizer)
print(metrics)
```

### 5. Live Trading

```python
from src.execution import OrderExecutor
from src.risk_management import RiskManager

executor = OrderExecutor(client, mode="testnet")
risk_manager = RiskManager(max_leverage=5)

# Place order
order = Order(
    symbol="BTCUSDT",
    side=OrderSide.BUY,
    position_side=PositionSide.LONG,
    order_type=OrderType.LIMIT,
    quantity=0.1,
    price=45000,
)

response = executor.place_order(order)
```

### 6. Web Dashboard

Start the backend API (Terminal 1):
```bash
python -m src.api.server
```

Start the frontend server (Terminal 2):
```bash
cd frontend
python server.py
```

Open dashboard in browser:
```
http://localhost:3000
```

The dashboard provides:
- Real-time account monitoring
- Trading controls (paper/testnet/live)
- Backtesting interface
- Risk management tools
- Model predictions
- Equity curve visualization
- Trade history

See [WEB_DASHBOARD_SETUP.md](WEB_DASHBOARD_SETUP.md) for detailed instructions.

## Configuration

Edit `config/config.yaml` to customize:
- Binance API settings
- Data collection parameters
- Model hyperparameters
- Risk management limits
- Backtesting parameters
- Execution mode (paper/testnet/live)

## Testing

Run tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=src
```

## Documentation

- [Data Pipeline](docs/data_pipeline.md)
- [Feature Engineering](docs/features.md)
- [Models](docs/models.md)
- [Risk Management](docs/risk_management.md)
- [Backtesting](docs/backtesting.md)
- [API Reference](docs/api_reference.md)

## Performance Metrics

The system tracks:
- **Forecasting**: MAPE, RMSE, Pinball Loss, CRPS
- **Trading**: Sharpe Ratio, Sortino Ratio, Max Drawdown, CAGR, Calmar Ratio
- **Risk**: Liquidation Probability, Funding Costs, Position Sizing

## Important Warnings

⚠️ **Risk Disclaimer**:
- Cryptocurrency markets are highly volatile
- Past performance does not guarantee future results
- Models can overfit historical data
- Funding costs and slippage can turn profitable signals into losses
- Always backtest thoroughly before live trading
- Start with paper trading and small positions
- Use appropriate leverage limits and stop losses

## Best Practices

1. **Always backtest** with realistic parameters
2. **Use walk-forward analysis** to avoid look-ahead bias
3. **Monitor data drift** and retrain models regularly
4. **Start with paper trading** before going live
5. **Use conservative leverage** (1-3x recommended)
6. **Monitor funding rates** and adjust positions accordingly
7. **Implement circuit breakers** for risk management
8. **Log all trades** for analysis and compliance

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review example scripts

## Roadmap

- [ ] WebSocket streaming for real-time data
- [ ] Advanced on-chain metrics integration
- [ ] Sentiment analysis integration
- [ ] Multi-symbol portfolio optimization
- [ ] Advanced RL-based position sizing
- [ ] Distributed backtesting
- [ ] Web dashboard for monitoring
- [ ] Mobile alerts

## Disclaimer

This software is provided for educational and research purposes only. Trading cryptocurrencies involves substantial risk of loss. The authors are not responsible for any financial losses incurred through the use of this software. Always conduct your own research and consult with financial advisors before trading.

