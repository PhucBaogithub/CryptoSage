# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies

```bash
cd /Users/phucbao/Documents/Binance

# Install the package in development mode
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your Binance API credentials
# BINANCE_API_KEY=your_key_here
# BINANCE_API_SECRET=your_secret_here
```

### 3. Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/unit/test_utils.py -v
```

## Step-by-Step Workflow

### Step 1: Collect Data

```bash
python examples/01_data_collection.py
```

This will:
- Download historical OHLCV data from Binance
- Fetch funding rates and open interest
- Save data to `data/raw/` directory

**Expected output**:
```
Collecting data for symbols: ['BTCUSDT']
Collecting BTCUSDT 1h...
  Retrieved 1000 candles
  Date range: 2024-10-10 to 2024-10-20
  Price range: $42000.00 - $48000.00
  Saved to disk
```

### Step 2: Engineer Features

```bash
python examples/02_feature_engineering.py
```

This will:
- Load raw OHLCV data
- Calculate technical indicators
- Generate price, liquidity, and volatility features
- Save processed data to `data/processed/` directory

**Expected output**:
```
Loading BTCUSDT 1h data...
Loaded 1000 candles
Engineering features...
Engineered 50+ features
Saving processed data...
Saved!
```

### Step 3: Train Models

```bash
python examples/03_model_training.py
```

This will:
- Load processed features
- Prepare training/validation data
- Train long-term prediction model
- Train short-term signal model
- Save models to `models/` directory

**Expected output**:
```
Loading BTCUSDT 1h data...
Loaded 1000 candles
Preparing data for long-term model...
Training long-term model...
  Epoch 10/100, Train Loss: 0.001234
Model saved to models/long_term_model.pt
```

### Step 4: Run Backtest

```bash
python examples/04_backtesting.py
```

This will:
- Load historical data
- Generate trading signals
- Simulate trades with realistic fees and slippage
- Calculate performance metrics

**Expected output**:
```
============================================================
BACKTEST RESULTS
============================================================
Total Return: 15.32%
Annual Return: 45.96%
Sharpe Ratio: 1.45
Max Drawdown: -8.23%
Win Rate: 58.33%
Total Trades: 24
```

### Step 5: Analyze Risk

```bash
python examples/05_risk_management.py
```

This will:
- Calculate liquidation prices
- Estimate liquidation probabilities
- Compute funding costs
- Demonstrate position sizing strategies

**Expected output**:
```
============================================================
RISK MANAGEMENT EXAMPLE
============================================================
1. Liquidation Analysis:
  Liquidation Price: $35,250.00
  Distance to Liquidation: 31.20%
  Liquidation Probability (24h): 2.34%

2. Funding Cost Analysis:
  Hourly Funding Cost: $5.00
  Daily Funding Cost: $120.00
  Monthly Funding Cost: $3,600.00
```

## Common Commands

### View Configuration

```python
from src.utils import Config

config = Config()
print(config.get("binance.testnet"))  # True
print(config.get("risk_management.max_leverage"))  # 5.0
```

### Load Data

```python
from src.data import DataManager

dm = DataManager()
df = dm.load_klines("BTCUSDT", "1h", data_type="raw")
print(df.head())
```

### Engineer Features

```python
from src.features import FeatureEngineer

engineer = FeatureEngineer()
df_features = engineer.engineer_features(df)
print(df_features.columns)
```

### Calculate Risk Metrics

```python
from src.risk_management import RiskManager

rm = RiskManager()
metrics = rm.calculate_risk_metrics(
    entry_price=45000,
    current_price=46000,
    position_size_usd=50000,
    leverage=3.0,
    funding_rate=0.0001,
    volatility=0.25,
)
print(f"Liquidation Price: ${metrics.liquidation_price:,.2f}")
print(f"Max Loss: ${metrics.max_loss_usd:,.2f}")
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution**: Make sure you're running from the project root directory:
```bash
cd /Users/phucbao/Documents/Binance
python examples/01_data_collection.py
```

### Issue: "Binance API error: Invalid API key"

**Solution**: Check your `.env` file:
```bash
# Verify API credentials are set
echo $BINANCE_API_KEY
echo $BINANCE_API_SECRET

# Make sure .env is in the project root
ls -la .env
```

### Issue: "No data found"

**Solution**: Run data collection first:
```bash
python examples/01_data_collection.py
```

### Issue: "CUDA out of memory"

**Solution**: Use CPU instead:
```python
model = LongTermModel(config)
model.device = "cpu"
```

## Next Steps

1. **Customize Configuration**: Edit `config/config.yaml` for your preferences
2. **Backtest Your Strategy**: Modify signal generation in examples
3. **Paper Trade**: Set `execution.mode: paper` in config
4. **Monitor Performance**: Check logs in `logs/` directory
5. **Go Live**: Switch to testnet, then live trading

## Important Reminders

⚠️ **Before Live Trading**:
1. ✓ Thoroughly backtest your strategy
2. ✓ Paper trade for at least 1 week
3. ✓ Test on testnet with small amounts
4. ✓ Monitor funding rates and liquidation risks
5. ✓ Start with 1x leverage
6. ✓ Use stop losses and position limits

## Getting Help

- Check `README.md` for detailed documentation
- Review `ARCHITECTURE.md` for system design
- Look at example scripts in `examples/` directory
- Run tests to verify installation: `pytest tests/`
- Check logs in `logs/` directory for errors

## Performance Tips

1. **Use GPU**: Install CUDA for faster model training
2. **Cache Data**: Processed data is cached for faster loading
3. **Batch Processing**: Process multiple symbols in parallel
4. **Optimize Features**: Remove unused features to speed up training
5. **Monitor Metrics**: Use Prometheus for real-time monitoring

Good luck with your trading! 🚀

