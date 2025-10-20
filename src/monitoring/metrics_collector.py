"""Metrics collection and monitoring."""

from datetime import datetime
from typing import Dict, Optional

from prometheus_client import Counter, Gauge, Histogram

from ..utils import get_logger

logger = get_logger(__name__)


class MetricsCollector:
    """Collects and exposes metrics for monitoring."""
    
    def __init__(self):
        """Initialize metrics collector."""
        # Trading metrics
        self.trades_total = Counter(
            "trades_total",
            "Total number of trades",
            ["symbol", "side"],
        )
        
        self.trades_pnl = Histogram(
            "trades_pnl",
            "Trade P&L distribution",
            ["symbol"],
            buckets=(-1000, -500, -100, -10, 0, 10, 100, 500, 1000),
        )
        
        self.position_size = Gauge(
            "position_size_usd",
            "Current position size in USD",
            ["symbol"],
        )
        
        self.leverage_used = Gauge(
            "leverage_used",
            "Current leverage used",
            ["symbol"],
        )
        
        # Market metrics
        self.price = Gauge(
            "price_usd",
            "Current price",
            ["symbol"],
        )
        
        self.volatility = Gauge(
            "volatility",
            "Current volatility",
            ["symbol"],
        )
        
        self.funding_rate = Gauge(
            "funding_rate",
            "Current funding rate",
            ["symbol"],
        )
        
        # Account metrics
        self.account_equity = Gauge(
            "account_equity_usd",
            "Account equity in USD",
        )
        
        self.account_balance = Gauge(
            "account_balance_usd",
            "Account balance in USD",
        )
        
        self.account_drawdown = Gauge(
            "account_drawdown_pct",
            "Account drawdown percentage",
        )
        
        # Model metrics
        self.model_prediction_confidence = Gauge(
            "model_prediction_confidence",
            "Model prediction confidence",
            ["model_name"],
        )
        
        self.model_accuracy = Gauge(
            "model_accuracy",
            "Model accuracy",
            ["model_name"],
        )
        
        # System metrics
        self.data_collection_latency = Histogram(
            "data_collection_latency_seconds",
            "Data collection latency",
            buckets=(0.1, 0.5, 1.0, 2.0, 5.0),
        )
        
        self.model_inference_latency = Histogram(
            "model_inference_latency_seconds",
            "Model inference latency",
            ["model_name"],
            buckets=(0.01, 0.05, 0.1, 0.5, 1.0),
        )
        
        logger.info("MetricsCollector initialized")
    
    def record_trade(
        self,
        symbol: str,
        side: str,
        quantity: float,
        entry_price: float,
        exit_price: float,
        pnl: float,
    ) -> None:
        """Record a trade.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            quantity: Trade quantity
            entry_price: Entry price
            exit_price: Exit price
            pnl: Trade P&L
        """
        self.trades_total.labels(symbol=symbol, side=side).inc()
        self.trades_pnl.labels(symbol=symbol).observe(pnl)
        
        logger.info(
            f"Trade recorded: {symbol} {side} {quantity} "
            f"@ {entry_price} -> {exit_price}, P&L: {pnl}"
        )
    
    def update_position(
        self,
        symbol: str,
        position_size_usd: float,
        leverage: float,
    ) -> None:
        """Update position metrics.
        
        Args:
            symbol: Trading pair
            position_size_usd: Position size in USD
            leverage: Leverage used
        """
        self.position_size.labels(symbol=symbol).set(position_size_usd)
        self.leverage_used.labels(symbol=symbol).set(leverage)
    
    def update_market_data(
        self,
        symbol: str,
        price: float,
        volatility: float,
        funding_rate: float,
    ) -> None:
        """Update market data metrics.
        
        Args:
            symbol: Trading pair
            price: Current price
            volatility: Current volatility
            funding_rate: Current funding rate
        """
        self.price.labels(symbol=symbol).set(price)
        self.volatility.labels(symbol=symbol).set(volatility)
        self.funding_rate.labels(symbol=symbol).set(funding_rate)
    
    def update_account(
        self,
        equity: float,
        balance: float,
        drawdown_pct: float,
    ) -> None:
        """Update account metrics.
        
        Args:
            equity: Account equity
            balance: Account balance
            drawdown_pct: Drawdown percentage
        """
        self.account_equity.set(equity)
        self.account_balance.set(balance)
        self.account_drawdown.set(drawdown_pct)
    
    def update_model_metrics(
        self,
        model_name: str,
        confidence: float,
        accuracy: float,
    ) -> None:
        """Update model metrics.
        
        Args:
            model_name: Name of the model
            confidence: Prediction confidence
            accuracy: Model accuracy
        """
        self.model_prediction_confidence.labels(model_name=model_name).set(confidence)
        self.model_accuracy.labels(model_name=model_name).set(accuracy)
    
    def record_data_collection_latency(self, latency_seconds: float) -> None:
        """Record data collection latency.
        
        Args:
            latency_seconds: Latency in seconds
        """
        self.data_collection_latency.observe(latency_seconds)
    
    def record_model_inference_latency(
        self,
        model_name: str,
        latency_seconds: float,
    ) -> None:
        """Record model inference latency.
        
        Args:
            model_name: Name of the model
            latency_seconds: Latency in seconds
        """
        self.model_inference_latency.labels(model_name=model_name).observe(latency_seconds)

