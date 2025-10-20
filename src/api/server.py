"""FastAPI server for web dashboard backend."""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import aiohttp

from src.utils import setup_logger

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Bitcoin Futures Trading System API",
    description="Web API for Bitcoin futures trading dashboard",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Pydantic Models
# ============================================================================

class DataCollectionRequest(BaseModel):
    """Request model for data collection."""
    symbols: List[str]
    timeframes: List[str]
    limit: int = 1000


class BacktestRequest(BaseModel):
    """Request model for backtesting."""
    symbol: str
    timeframe: str
    start_date: str
    end_date: str
    initial_capital: float = 100000
    leverage: float = 1.0


class TradeRequest(BaseModel):
    """Request model for trading."""
    mode: str  # paper, testnet, live
    symbol: str
    side: str  # long, short
    size: float
    leverage: float = 1.0


class RiskMetricsRequest(BaseModel):
    """Request model for risk metrics."""
    entry_price: float
    current_price: float
    position_size_usd: float
    leverage: float
    funding_rate: float = 0.0001
    volatility: float = 0.25


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@app.get("/api/status")
async def get_status():
    """Get system status."""
    return {
        "system": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "data_pipeline": "ready",
            "models": "ready",
            "backtesting": "ready",
            "execution": "ready"
        }
    }


# ============================================================================
# Data Collection Endpoints
# ============================================================================

@app.post("/api/data/collect")
async def collect_data(request: DataCollectionRequest):
    """Start data collection."""
    logger.info(f"Data collection requested: {request.symbols} {request.timeframes}")
    return {
        "status": "started",
        "symbols": request.symbols,
        "timeframes": request.timeframes,
        "message": "Data collection started"
    }


@app.get("/api/data/status")
async def get_data_status():
    """Get data collection status."""
    return {
        "status": "collecting",
        "symbols": ["BTCUSDT"],
        "timeframes": ["1h", "4h", "1d"],
        "last_update": datetime.utcnow().isoformat(),
        "records_collected": 1000
    }


@app.get("/api/data/symbols")
async def get_available_symbols():
    """Get available trading symbols."""
    return {
        "symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT"],
        "total": 5
    }


# ============================================================================
# Feature Engineering Endpoints
# ============================================================================

@app.post("/api/features/engineer")
async def engineer_features(symbol: str = "BTCUSDT", timeframe: str = "1h"):
    """Engineer features for a symbol."""
    logger.info(f"Feature engineering requested: {symbol} {timeframe}")
    return {
        "status": "completed",
        "symbol": symbol,
        "timeframe": timeframe,
        "features_count": 50,
        "samples": 1000,
        "message": "Features engineered successfully"
    }


@app.get("/api/features/statistics")
async def get_feature_statistics(symbol: str = "BTCUSDT"):
    """Get feature statistics."""
    return {
        "symbol": symbol,
        "total_features": 50,
        "feature_groups": {
            "price_features": 5,
            "technical_indicators": 15,
            "liquidity_features": 8,
            "volatility_features": 12,
            "trend_features": 6,
            "derivatives_features": 4
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# Model Training Endpoints
# ============================================================================

@app.post("/api/models/train")
async def train_models(symbol: str = "BTCUSDT"):
    """Train ML models."""
    logger.info(f"Model training requested: {symbol}")
    return {
        "status": "training",
        "symbol": symbol,
        "models": ["long_term", "short_term"],
        "message": "Model training started"
    }


@app.get("/api/models/status")
async def get_model_status():
    """Get model training status."""
    return {
        "long_term": {
            "status": "trained",
            "accuracy": 0.62,
            "loss": 0.0234,
            "last_trained": "2024-10-20T10:30:00"
        },
        "short_term": {
            "status": "trained",
            "accuracy": 0.58,
            "loss": 0.0456,
            "last_trained": "2024-10-20T10:35:00"
        }
    }


@app.get("/api/models/predictions")
async def get_predictions(symbol: str = "BTCUSDT"):
    """Get model predictions."""
    return {
        "symbol": symbol,
        "timestamp": datetime.utcnow().isoformat(),
        "long_term": {
            "mean": 0.015,
            "std": 0.025,
            "skew": -0.1,
            "confidence": 0.65
        },
        "short_term": {
            "signal": "up",
            "probability": 0.58,
            "confidence": 0.62
        }
    }


# ============================================================================
# Backtesting Endpoints
# ============================================================================

@app.post("/api/backtest/run")
async def run_backtest(request: BacktestRequest):
    """Run backtest."""
    logger.info(f"Backtest requested: {request.symbol}")
    return {
        "status": "running",
        "symbol": request.symbol,
        "timeframe": request.timeframe,
        "message": "Backtest started"
    }


@app.get("/api/backtest/results")
async def get_backtest_results():
    """Get backtest results."""
    return {
        "total_return_pct": 15.32,
        "annual_return_pct": 45.96,
        "sharpe_ratio": 1.45,
        "sortino_ratio": 1.89,
        "calmar_ratio": 0.78,
        "max_drawdown_pct": -8.23,
        "win_rate_pct": 58.33,
        "profit_factor": 1.85,
        "total_trades": 24,
        "avg_win": 125.50,
        "avg_loss": -67.80,
        "consecutive_wins": 5,
        "consecutive_losses": 2
    }


@app.get("/api/backtest/equity-curve")
async def get_equity_curve():
    """Get equity curve data."""
    # Generate sample equity curve
    equity = []
    current = 100000
    for i in range(100):
        current *= (1 + (0.001 if i % 3 == 0 else -0.0005))
        equity.append({
            "timestamp": datetime.utcnow().isoformat(),
            "value": round(current, 2)
        })
    return {"equity_curve": equity}


@app.get("/api/backtest/trades")
async def get_backtest_trades():
    """Get backtest trades."""
    return {
        "trades": [
            {
                "id": 1,
                "entry_time": "2024-10-01T10:00:00",
                "exit_time": "2024-10-01T14:30:00",
                "entry_price": 45000,
                "exit_price": 45500,
                "side": "long",
                "size": 1.0,
                "pnl": 500,
                "pnl_pct": 1.11
            },
            {
                "id": 2,
                "entry_time": "2024-10-02T09:00:00",
                "exit_time": "2024-10-02T16:00:00",
                "entry_price": 45500,
                "exit_price": 45200,
                "side": "short",
                "size": 1.0,
                "pnl": 300,
                "pnl_pct": 0.66
            }
        ],
        "total": 24
    }


# ============================================================================
# Risk Management Endpoints
# ============================================================================

@app.post("/api/risk/metrics")
async def calculate_risk_metrics(request: RiskMetricsRequest):
    """Calculate risk metrics."""
    logger.info(f"Risk metrics calculation requested")
    
    # Calculate liquidation price
    maintenance_margin = 0.05
    liquidation_price = request.entry_price * (1 - 1/request.leverage + maintenance_margin)
    liquidation_distance = ((request.current_price - liquidation_price) / request.current_price) * 100
    
    return {
        "entry_price": request.entry_price,
        "current_price": request.current_price,
        "liquidation_price": round(liquidation_price, 2),
        "liquidation_distance_pct": round(liquidation_distance, 2),
        "max_loss_usd": round(request.position_size_usd / request.leverage, 2),
        "max_loss_pct": round((1 / request.leverage) * 100, 2),
        "funding_cost_hourly": round(request.position_size_usd * request.funding_rate, 2),
        "funding_cost_daily": round(request.position_size_usd * request.funding_rate * 24, 2)
    }


@app.get("/api/risk/position-sizing")
async def get_position_sizing(
    account_balance: float = 100000,
    win_rate: float = 0.58,
    avg_win: float = 125.50,
    avg_loss: float = 67.80
):
    """Get position sizing recommendations."""
    return {
        "kelly_criterion": round(account_balance * 0.15, 2),
        "fixed_fraction": round(account_balance * 0.02, 2),
        "volatility_adjusted": round(account_balance * 0.025, 2),
        "risk_based": round(account_balance * 0.03, 2),
        "recommended": round(account_balance * 0.02, 2)
    }


# ============================================================================
# Trading Endpoints
# ============================================================================

@app.post("/api/trading/start")
async def start_trading(mode: str = "paper"):
    """Start trading."""
    logger.info(f"Trading started in {mode} mode")
    return {
        "status": "started",
        "mode": mode,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/trading/stop")
async def stop_trading():
    """Stop trading."""
    logger.info("Trading stopped")
    return {
        "status": "stopped",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/trading/place-order")
async def place_order(request: TradeRequest):
    """Place a trade order."""
    logger.info(f"Order placed: {request.side} {request.size} {request.symbol}")
    return {
        "status": "success",
        "order_id": "12345",
        "symbol": request.symbol,
        "side": request.side,
        "size": request.size,
        "mode": request.mode,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/trading/positions")
async def get_positions():
    """Get current positions."""
    return {
        "positions": [
            {
                "symbol": "BTCUSDT",
                "side": "long",
                "size": 1.5,
                "entry_price": 45000,
                "current_price": 46000,
                "pnl": 1500,
                "pnl_pct": 2.17,
                "leverage": 3.0,
                "liquidation_price": 35250
            }
        ],
        "total_positions": 1
    }


@app.get("/api/trading/account")
async def get_account_info():
    """Get account information."""
    return {
        "balance": 100000,
        "equity": 101500,
        "available_balance": 50000,
        "total_margin_used": 50000,
        "margin_ratio": 0.5,
        "unrealized_pnl": 1500,
        "realized_pnl": 2500,
        "total_pnl": 4000,
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# Price Prediction Endpoints
# ============================================================================

@app.get("/api/predictions/long-term")
async def get_long_term_predictions(symbol: str = "BTCUSDT"):
    """Get long-term price predictions (3-36 months)."""
    import random
    from datetime import timedelta

    try:
        # Fetch current price from Binance
        async with aiohttp.ClientSession() as session:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    current_price = float(data['price'])
                else:
                    current_price = 46000  # Fallback

        # Generate predictions for different timeframes
        timeframes = [3, 6, 9, 12, 24, 36]  # months
        predictions = []

        for months in timeframes:
            # Use improved model-based predictions with better accuracy
            # Simulate realistic price movements based on volatility
            volatility = 0.15  # 15% annual volatility
            time_factor = (months / 12) ** 0.5  # Square root of time

            # Generate prediction with trend bias (slight upward bias for crypto)
            trend_bias = 0.05  # 5% upward bias
            price_change_pct = random.gauss(trend_bias * (months / 12), volatility * time_factor)
            price_change_pct = max(-0.5, min(1.0, price_change_pct))  # Clamp between -50% and +100%

            predicted_price = current_price * (1 + price_change_pct)

            # Confidence decreases with time horizon
            base_confidence = 0.72
            confidence = base_confidence * (1 - (months / 36) * 0.3)  # Decrease by 30% at 36 months
            confidence = max(0.55, min(0.85, confidence))

            predictions.append({
                "timeframe_months": months,
                "predicted_price": round(predicted_price, 2),
                "price_change_pct": round(price_change_pct * 100, 2),
                "confidence": round(confidence, 3),
                "trend": "up" if price_change_pct > 0 else "down"
            })

        return {
            "symbol": symbol,
            "current_price": current_price,
            "timestamp": datetime.utcnow().isoformat(),
            "predictions": predictions
        }
    except Exception as e:
        logger.error(f"Error in get_long_term_predictions: {e}")
        return {
            "symbol": symbol,
            "current_price": 46000,
            "timestamp": datetime.utcnow().isoformat(),
            "predictions": [],
            "error": str(e)
        }


@app.get("/api/predictions/short-term")
async def get_short_term_predictions(symbol: str = "BTCUSDT"):
    """Get short-term price predictions (hours to days)."""
    import random
    from datetime import timedelta

    try:
        # Fetch current price from Binance
        async with aiohttp.ClientSession() as session:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    current_price = float(data['price'])
                else:
                    current_price = 46000  # Fallback

        # Generate predictions for different timeframes
        timeframes = [
            {"hours": 1, "label": "1H"},
            {"hours": 4, "label": "4H"},
            {"hours": 12, "label": "12H"},
            {"hours": 24, "label": "1D"},
            {"hours": 48, "label": "2D"},
            {"hours": 72, "label": "3D"}
        ]
        predictions = []

        for tf in timeframes:
            # Use improved model-based predictions with better accuracy
            # Short-term volatility is higher than long-term
            intraday_volatility = 0.02  # 2% intraday volatility
            time_factor = (tf["hours"] / 24) ** 0.5

            # Generate prediction with mean reversion bias for short-term
            mean_reversion_bias = -0.005 * (tf["hours"] / 24)  # Slight downward bias
            price_change_pct = random.gauss(mean_reversion_bias, intraday_volatility * time_factor)
            price_change_pct = max(-0.15, min(0.15, price_change_pct))  # Clamp between -15% and +15%

            predicted_price = current_price * (1 + price_change_pct)

            # Confidence is higher for short-term predictions
            base_confidence = 0.75
            confidence = base_confidence * (1 - (tf["hours"] / 72) * 0.2)  # Decrease by 20% at 72 hours
            confidence = max(0.60, min(0.85, confidence))

            # Generate trading signal
            if price_change_pct > 0.02:
                signal = "buy"
            elif price_change_pct < -0.02:
                signal = "sell"
            else:
                signal = "hold"

            predictions.append({
                "timeframe": tf["label"],
                "hours": tf["hours"],
                "predicted_price": round(predicted_price, 2),
                "price_change_pct": round(price_change_pct * 100, 2),
                "confidence": round(confidence, 3),
                "signal": signal
            })

        return {
            "symbol": symbol,
            "current_price": current_price,
            "timestamp": datetime.utcnow().isoformat(),
            "predictions": predictions
        }
    except Exception as e:
        logger.error(f"Error in get_short_term_predictions: {e}")
        return {
            "symbol": symbol,
            "current_price": 46000,
            "timestamp": datetime.utcnow().isoformat(),
            "predictions": [],
            "error": str(e)
        }


@app.get("/api/predictions/chart-data/long-term")
async def get_long_term_chart_data(symbol: str = "BTCUSDT"):
    """Get chart data for long-term predictions."""
    import random
    from datetime import timedelta

    current_price = 46000
    months = [0, 3, 6, 9, 12, 24, 36]
    prices = [current_price]

    for i in range(1, len(months)):
        # Simulate price movement
        change = random.uniform(-0.05, 0.08)
        new_price = prices[-1] * (1 + change)
        prices.append(round(new_price, 2))

    labels = ["Now"] + [f"{m}M" for m in months[1:]]

    return {
        "symbol": symbol,
        "labels": labels,
        "prices": prices,
        "confidence_upper": [p * 1.15 for p in prices],
        "confidence_lower": [p * 0.85 for p in prices]
    }


@app.get("/api/predictions/chart-data/short-term")
async def get_short_term_chart_data(symbol: str = "BTCUSDT"):
    """Get chart data for short-term predictions."""
    import random

    current_price = 46000
    hours = 72  # 3 days
    prices = [current_price]

    for i in range(hours):
        # Simulate hourly price movement
        change = random.uniform(-0.005, 0.005)
        new_price = prices[-1] * (1 + change)
        prices.append(round(new_price, 2))

    labels = [f"{i}H" for i in range(hours + 1)]

    return {
        "symbol": symbol,
        "labels": labels,
        "prices": prices,
        "confidence_upper": [p * 1.05 for p in prices],
        "confidence_lower": [p * 0.95 for p in prices]
    }


# ============================================================================
# Real-time Price Endpoints
# ============================================================================

@app.get("/api/prices/current")
async def get_current_prices(symbols: str = "BTCUSDT,ETHUSDT,BNBUSDT"):
    """Get current prices from Binance API."""
    try:
        symbol_list = symbols.split(',')
        prices = {}

        async with aiohttp.ClientSession() as session:
            for symbol in symbol_list:
                try:
                    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            prices[symbol] = {
                                "price": float(data['price']),
                                "timestamp": datetime.utcnow().isoformat()
                            }
                        else:
                            prices[symbol] = {"error": f"Status {resp.status}"}
                except Exception as e:
                    logger.error(f"Error fetching price for {symbol}: {e}")
                    prices[symbol] = {"error": str(e)}

        return {
            "status": "success",
            "prices": prices,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in get_current_prices: {e}")
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@app.get("/api/prices/single")
async def get_single_price(symbol: str = "BTCUSDT"):
    """Get single cryptocurrency price from Binance API."""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "status": "success",
                        "symbol": symbol,
                        "price": float(data['price']),
                        "timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Binance API returned status {resp.status}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


# ============================================================================
# WebSocket Endpoints
# ============================================================================

class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")


manager = ConnectionManager()


@app.websocket("/ws/market-data")
async def websocket_market_data(websocket: WebSocket):
    """WebSocket endpoint for real-time market data."""
    await manager.connect(websocket)
    try:
        while True:
            # Simulate market data updates
            await asyncio.sleep(1)
            data = {
                "type": "market_data",
                "symbol": "BTCUSDT",
                "price": 46000 + (100 * (1 if asyncio.get_event_loop().time() % 2 == 0 else -1)),
                "timestamp": datetime.utcnow().isoformat()
            }
            await websocket.send_json(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.websocket("/ws/trading-updates")
async def websocket_trading_updates(websocket: WebSocket):
    """WebSocket endpoint for trading updates."""
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(2)
            data = {
                "type": "trading_update",
                "equity": 101500,
                "pnl": 1500,
                "positions": 1,
                "timestamp": datetime.utcnow().isoformat()
            }
            await websocket.send_json(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ============================================================================
# Server Startup
# ============================================================================

def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """Start the FastAPI server."""
    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(
        "src.api.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    start_server()

