# System Architecture

## Overview

The Bitcoin Futures Trading System is built with a modular, production-grade architecture designed for scalability, maintainability, and robustness.

## Core Components

### 1. Data Pipeline (`src/data/`)

**Purpose**: Collect, store, and retrieve market data from Binance

**Components**:
- `BinanceDataClient`: REST API client for Binance Futures
  - Fetches OHLCV data across multiple timeframes
  - Retrieves funding rates and open interest
  - Gets order book snapshots and recent trades
  
- `DataManager`: Handles data persistence
  - Stores data in Parquet format for efficiency
  - Manages raw and processed data directories
  - Provides caching for fast retrieval

**Data Flow**:
```
Binance API → BinanceDataClient → DataManager → Parquet Files
```

### 2. Feature Engineering (`src/features/`)

**Purpose**: Transform raw OHLCV data into ML-ready features

**Features Generated**:
- **Price Features**: Log returns, momentum, ROC
- **Technical Indicators**: RSI, MACD, Bollinger Bands, ATR, ADX, EMA, SMA
- **Liquidity Features**: Volume analysis, OBV, VROC
- **Volatility Features**: Historical, Parkinson, Garman-Klass
- **Derivatives Features**: Funding rates, Open Interest
- **Trend Features**: Direction, Higher Highs/Lower Lows

**Output**: Feature-rich DataFrames ready for model training

### 3. Machine Learning Models (`src/models/`)

**Architecture**:

#### Long-term Model (Daily/Weekly/Monthly)
- **Type**: Temporal Fusion Transformer (TFT)
- **Input**: 168 hours of historical data (7 days)
- **Output**: Probabilistic forecasts (mean, std, skew) for 30-day horizon
- **Use Case**: Strategic position planning, macro trend identification

#### Short-term Model (Intraday)
- **Type**: Transformer with signal heads
- **Input**: 60 minutes of minute-level data
- **Output**: Signal probabilities (up/down/neutral) + confidence
- **Use Case**: Tactical entry/exit signals, high-frequency trading

**Model Pipeline**:
```
Raw Features → Preprocessing → Transformer Encoder → Output Heads → Predictions
```

### 4. Risk Management (`src/risk_management/`)

**Components**:

#### RiskManager
- Calculates liquidation prices and probabilities
- Estimates funding costs
- Validates positions against risk limits
- Provides comprehensive risk metrics

#### PositionSizer
- Kelly Criterion sizing
- Fixed fraction sizing
- Volatility-adjusted sizing
- Risk-based sizing
- Leverage-adjusted sizing

**Risk Workflow**:
```
Signal → Position Sizing → Risk Validation → Order Execution
```

### 5. Backtesting Framework (`src/backtesting/`)

**Components**:

#### BacktestEngine
- Simulates trading with realistic parameters
- Includes slippage, fees, and funding costs
- Tracks equity curve and trades
- Supports walk-forward analysis

#### MetricsCalculator
- Calculates Sharpe, Sortino, Calmar ratios
- Computes max drawdown and win rate
- Generates comprehensive performance reports

**Backtest Flow**:
```
Historical Data → Signal Generation → Position Sizing → 
Trade Simulation → Metrics Calculation → Performance Report
```

### 6. Order Execution (`src/execution/`)

**Components**:

#### OrderExecutor
- Supports multiple execution modes:
  - **Paper**: Simulated trading
  - **Testnet**: Binance testnet
  - **Live**: Production trading
- Handles order placement and cancellation
- Tracks order status

**Execution Modes**:
```
Paper Trading → Testnet → Live Trading
(Validation)   (Testing)  (Production)
```

### 7. Monitoring (`src/monitoring/`)

**Components**:

#### MetricsCollector
- Prometheus metrics for system monitoring
- Tracks trading metrics (P&L, trades, positions)
- Monitors market data (price, volatility, funding)
- Records model performance

**Monitoring Stack**:
```
Application → MetricsCollector → Prometheus → Grafana
```

### 8. Utilities (`src/utils/`)

**Components**:
- `Config`: YAML configuration with environment variable substitution
- `Logger`: Structured logging with file and console output
- `TimeUtils`: Time operations and timeframe conversions

## Data Flow Architecture

### Real-time Trading Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Real-time Data Stream                     │
│              (WebSocket from Binance Futures)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Feature Engineering                        │
│         (Calculate indicators, aggregate data)               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Model Inference                             │
│      (Long-term + Short-term predictions)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Signal Generation                            │
│         (Combine predictions into trading signals)           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Risk Management                              │
│      (Validate position, calculate sizing)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Order Execution                              │
│         (Place orders on Binance Futures)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Monitoring & Logging                         │
│      (Track metrics, log trades, alert on risks)            │
└─────────────────────────────────────────────────────────────┘
```

## Backtesting Flow

```
┌──────────────────────────────────────────────────────────────┐
│              Historical Data Loading                          │
│         (OHLCV, funding rates, open interest)                │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              Feature Engineering                              │
│         (Calculate all features for each candle)             │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│           Walk-Forward Analysis                               │
│    (Split into train/test periods, retrain models)           │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│           Signal Generation & Backtesting                     │
│    (Generate signals, simulate trades, track equity)         │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│           Performance Metrics Calculation                     │
│    (Sharpe, Sortino, max drawdown, win rate, etc.)          │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│           Results & Analysis                                  │
│    (Generate reports, visualizations, recommendations)       │
└──────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Data & Storage
- **Pandas/Polars**: Data manipulation
- **Parquet**: Efficient data storage
- **PostgreSQL/ClickHouse**: Time-series database (optional)

### Machine Learning
- **PyTorch**: Deep learning framework
- **PyTorch Lightning**: Training utilities
- **Transformers**: Pre-built transformer models
- **Scikit-learn**: ML utilities
- **XGBoost/LightGBM**: Gradient boosting

### APIs & Integrations
- **python-binance**: Binance API client
- **CCXT**: Cryptocurrency exchange library
- **aiohttp**: Async HTTP client

### Monitoring & Logging
- **Prometheus**: Metrics collection
- **Loguru**: Structured logging
- **Grafana**: Metrics visualization (optional)

### Testing
- **Pytest**: Testing framework
- **Pytest-asyncio**: Async testing

## Scalability Considerations

### Horizontal Scaling
- Separate data collection, feature engineering, and model inference
- Use message queues (Kafka) for decoupling
- Deploy models on TensorFlow Serving or TorchServe

### Vertical Scaling
- Use GPU acceleration for model training
- Implement batch processing for feature engineering
- Cache frequently accessed data

### Data Management
- Implement data retention policies
- Use time-series databases for efficient querying
- Archive old data to cold storage

## Security Considerations

1. **API Keys**: Store in environment variables, never in code
2. **Database**: Use encrypted connections, strong passwords
3. **Logging**: Sanitize sensitive data before logging
4. **Access Control**: Implement role-based access
5. **Audit Trail**: Log all trades and risk events

## Error Handling & Resilience

1. **Retry Logic**: Exponential backoff for API calls
2. **Circuit Breakers**: Stop trading on system failures
3. **Graceful Degradation**: Continue with reduced functionality
4. **Health Checks**: Monitor system health continuously
5. **Fallback Strategies**: Use simpler models if advanced ones fail

## Performance Optimization

1. **Caching**: Cache features and model predictions
2. **Vectorization**: Use NumPy/Pandas for fast computation
3. **Async I/O**: Use asyncio for concurrent API calls
4. **Model Quantization**: Reduce model size for faster inference
5. **Batch Processing**: Process multiple samples at once

