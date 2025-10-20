# Bitcoin Futures Trading System - Complete Index

## 📚 Documentation

### Getting Started
- **[README.md](README.md)** - Main project documentation with features and installation
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide with step-by-step instructions
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Comprehensive summary of what's been built
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed system architecture and design
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - Implementation roadmap and checklists

## 🏗️ Project Structure

### Source Code (`src/`)

#### Data Pipeline (`src/data/`)
- `binance_client.py` - Binance Futures API client
  - `get_klines()` - Fetch OHLCV data
  - `get_funding_rate_history()` - Fetch funding rates
  - `get_open_interest()` - Fetch open interest
  - `get_mark_price()` - Get current mark price
  - `get_order_book()` - Get order book snapshot
  - `get_recent_trades()` - Get recent trades

- `data_manager.py` - Data storage and retrieval
  - `save_klines()` - Save OHLCV data
  - `load_klines()` - Load OHLCV data
  - `save_funding_rates()` - Save funding rates
  - `load_funding_rates()` - Load funding rates
  - `get_latest_timestamp()` - Get latest data timestamp

#### Feature Engineering (`src/features/`)
- `feature_engineer.py` - Feature extraction
  - `engineer_features()` - Generate all features
  - `_add_price_features()` - Price-based features
  - `_add_technical_indicators()` - Technical indicators
  - `_add_liquidity_features()` - Liquidity features
  - `_add_volatility_features()` - Volatility features
  - `_add_trend_features()` - Trend features
  - `add_funding_rate_features()` - Funding rate features
  - `add_open_interest_features()` - Open interest features

#### Machine Learning Models (`src/models/`)
- `base_model.py` - Abstract base class
  - `build_model()` - Build model architecture
  - `train()` - Train the model
  - `predict()` - Make predictions
  - `save_model()` - Save model to disk
  - `load_model()` - Load model from disk

- `long_term_model.py` - Long-term prediction (daily/weekly/monthly)
  - `LongTermPredictionModel` - Transformer-based model
  - `LongTermModel` - Wrapper class

- `short_term_model.py` - Short-term signals (intraday)
  - `ShortTermSignalModel` - Transformer with signal heads
  - `ShortTermModel` - Wrapper class

#### Risk Management (`src/risk_management/`)
- `risk_manager.py` - Risk calculations
  - `calculate_liquidation_price()` - Liquidation price
  - `calculate_liquidation_distance()` - Distance to liquidation
  - `estimate_liquidation_probability()` - Liquidation probability
  - `calculate_funding_cost()` - Funding costs
  - `calculate_risk_metrics()` - Comprehensive risk metrics
  - `validate_position()` - Position validation

- `position_sizer.py` - Position sizing strategies
  - `kelly_criterion()` - Kelly Criterion sizing
  - `fixed_fraction()` - Fixed fraction sizing
  - `volatility_adjusted()` - Volatility-adjusted sizing
  - `risk_based()` - Risk-based sizing
  - `leverage_adjusted()` - Leverage-adjusted sizing
  - `calculate_leverage_for_position()` - Leverage calculation

#### Backtesting (`src/backtesting/`)
- `backtest_engine.py` - Trading simulation
  - `run()` - Run backtest
  - `_calculate_pnl()` - Calculate P&L
  - `get_equity_curve()` - Get equity curve
  - `get_trades()` - Get trades

- `metrics.py` - Performance metrics
  - `BacktestMetrics` - Metrics dataclass
  - `MetricsCalculator.calculate_metrics()` - Calculate all metrics

#### Order Execution (`src/execution/`)
- `order_executor.py` - Order placement
  - `place_order()` - Place order
  - `cancel_order()` - Cancel order
  - `get_order_status()` - Get order status
  - Support for paper, testnet, and live modes

#### Monitoring (`src/monitoring/`)
- `metrics_collector.py` - Prometheus metrics
  - `record_trade()` - Record trade metrics
  - `update_position()` - Update position metrics
  - `update_market_data()` - Update market metrics
  - `update_account()` - Update account metrics
  - `update_model_metrics()` - Update model metrics

#### Utilities (`src/utils/`)
- `config.py` - Configuration management
  - `Config` - YAML config with env var support
  - `get()` - Get config value
  - `get_section()` - Get config section

- `logger.py` - Logging setup
  - `setup_logger()` - Initialize logger
  - `get_logger()` - Get logger instance

- `time_utils.py` - Time utilities
  - `get_utc_now()` - Current UTC time
  - `timestamp_to_datetime()` - Convert timestamp
  - `datetime_to_timestamp()` - Convert to timestamp
  - `timeframe_to_minutes()` - Convert timeframe
  - `get_candle_start_time()` - Get candle start
  - `parse_date()` - Parse date string
  - `format_datetime()` - Format datetime

### Examples (`examples/`)
- `01_data_collection.py` - Download data from Binance
- `02_feature_engineering.py` - Transform data into features
- `03_model_training.py` - Train ML models
- `04_backtesting.py` - Run backtest
- `05_risk_management.py` - Demonstrate risk management

### Tests (`tests/`)
- `unit/test_utils.py` - Tests for utilities
- `unit/test_risk_management.py` - Tests for risk management
- `integration/` - Integration tests (to be added)

### Configuration
- `config/config.yaml` - Main configuration file
- `.env.example` - Environment variables template

### Data Storage
- `data/raw/` - Raw OHLCV data
- `data/processed/` - Processed features
- `data/cache/` - Cached data

### Logs
- `logs/` - Application logs

## 🚀 Quick Commands

### Setup
```bash
pip install -e .                    # Install dependencies
cp .env.example .env                # Setup environment
pytest tests/                       # Run tests
```

### Run Examples
```bash
python examples/01_data_collection.py      # Collect data
python examples/02_feature_engineering.py  # Engineer features
python examples/03_model_training.py       # Train models
python examples/04_backtesting.py          # Run backtest
python examples/05_risk_management.py      # Risk analysis
```

### Main Entry Point
```bash
python main.py collect-data         # Collect data
python main.py engineer-features    # Engineer features
python main.py train-models         # Train models
python main.py backtest             # Run backtest
python main.py trade --mode paper   # Paper trading
```

## 📊 Key Classes & Functions

### Data Collection
```python
from src.data import BinanceDataClient, DataManager

client = BinanceDataClient(api_key, api_secret)
df = client.get_klines("BTCUSDT", "1h")

dm = DataManager()
dm.save_klines("BTCUSDT", "1h", df)
```

### Feature Engineering
```python
from src.features import FeatureEngineer

engineer = FeatureEngineer()
df_features = engineer.engineer_features(df)
```

### Model Training
```python
from src.models import LongTermModel, ShortTermModel

model = LongTermModel(config)
history = model.train(X_train, y_train, X_val, y_val)
predictions = model.predict(X_test)
```

### Risk Management
```python
from src.risk_management import RiskManager, PositionSizer

rm = RiskManager()
metrics = rm.calculate_risk_metrics(...)

ps = PositionSizer()
size = ps.kelly_criterion(win_rate, avg_win, avg_loss, account)
```

### Backtesting
```python
from src.backtesting import BacktestEngine

engine = BacktestEngine(initial_capital=100000)
metrics = engine.run(data, signal_generator, position_sizer)
```

### Order Execution
```python
from src.execution import OrderExecutor

executor = OrderExecutor(client, mode="paper")
response = executor.place_order(order)
```

## 📈 Features Implemented

### Data Pipeline
- ✅ Multi-timeframe OHLCV collection
- ✅ Funding rates and open interest
- ✅ Order book snapshots
- ✅ Recent trades data
- ✅ Efficient Parquet storage

### Feature Engineering
- ✅ 50+ technical indicators
- ✅ Price momentum features
- ✅ Liquidity analysis
- ✅ Volatility metrics
- ✅ Derivatives features

### Machine Learning
- ✅ Transformer architectures
- ✅ Multi-horizon forecasting
- ✅ Probabilistic outputs
- ✅ Signal generation
- ✅ Model persistence

### Risk Management
- ✅ Liquidation prevention
- ✅ Funding cost optimization
- ✅ Position sizing strategies
- ✅ Risk validation
- ✅ Comprehensive metrics

### Backtesting
- ✅ Realistic simulation
- ✅ Walk-forward analysis
- ✅ Fee and slippage modeling
- ✅ Performance metrics
- ✅ Trade logging

### Production Ready
- ✅ Multiple execution modes
- ✅ Prometheus monitoring
- ✅ Structured logging
- ✅ Error handling
- ✅ Configuration management

## 🔗 Dependencies

### Core
- torch>=2.0.0
- pandas>=2.0.0
- numpy>=1.24.0

### APIs
- python-binance>=1.0.17
- ccxt>=4.0.0
- aiohttp>=3.9.0

### ML
- transformers>=4.30.0
- xgboost>=2.0.0
- lightgbm>=4.0.0
- scikit-learn>=1.3.0

### Analysis
- ta-lib>=0.4.28
- ta>=0.10.2
- statsmodels>=0.14.0

### Monitoring
- prometheus-client>=0.18.0
- loguru>=0.7.0

### Testing
- pytest>=7.4.0
- pytest-asyncio>=0.21.0

## 📝 Configuration

Main configuration in `config/config.yaml`:
- Binance API settings
- Data collection parameters
- Model hyperparameters
- Risk management limits
- Backtesting parameters
- Execution mode

## 🧪 Testing

```bash
pytest tests/                           # Run all tests
pytest tests/unit/                      # Run unit tests
pytest tests/unit/test_utils.py -v     # Run specific test
pytest tests/ --cov=src                # Run with coverage
```

## 📖 Learning Path

1. **Start**: Read [QUICKSTART.md](QUICKSTART.md)
2. **Understand**: Review [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Explore**: Run examples in `examples/` directory
4. **Customize**: Modify `config/config.yaml`
5. **Backtest**: Run backtests with your strategy
6. **Deploy**: Follow [NEXT_STEPS.md](NEXT_STEPS.md)

## ⚠️ Important Notes

- Always backtest thoroughly before live trading
- Start with paper trading and small positions
- Use conservative leverage (1-3x recommended)
- Monitor funding rates and liquidation risks
- Keep API keys secure in `.env` file
- Review logs regularly for errors

## 🎯 Next Steps

1. Complete setup from [QUICKSTART.md](QUICKSTART.md)
2. Run all example scripts
3. Review [NEXT_STEPS.md](NEXT_STEPS.md) for improvements
4. Customize for your strategy
5. Backtest thoroughly
6. Paper trade before going live

---

**For detailed information, see the documentation files listed above.**

