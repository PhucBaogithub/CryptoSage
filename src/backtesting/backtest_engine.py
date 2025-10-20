"""Backtesting engine for strategy evaluation."""

from datetime import datetime
from typing import Callable, Dict, List, Optional

import numpy as np
import pandas as pd

from ..utils import get_logger
from .metrics import BacktestMetrics, MetricsCalculator

logger = get_logger(__name__)


class BacktestEngine:
    """Backtesting engine for evaluating trading strategies."""
    
    def __init__(
        self,
        initial_capital: float = 100000,
        maker_fee: float = 0.0002,
        taker_fee: float = 0.0004,
        slippage_pct: float = 0.01,
        leverage: float = 1.0,
    ):
        """Initialize backtest engine.
        
        Args:
            initial_capital: Initial capital in USD
            maker_fee: Maker fee rate
            taker_fee: Taker fee rate
            slippage_pct: Slippage as percentage
            leverage: Leverage to use
        """
        self.initial_capital = initial_capital
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee
        self.slippage_pct = slippage_pct
        self.leverage = leverage
        
        self.equity = initial_capital
        self.trades: List[Dict] = []
        self.equity_curve: List[float] = [initial_capital]
        self.timestamps: List[datetime] = []
        
        logger.info(
            f"BacktestEngine initialized: capital={initial_capital}, "
            f"leverage={leverage}, fees={taker_fee}"
        )
    
    def run(
        self,
        data: pd.DataFrame,
        signal_generator: Callable,
        position_sizer: Callable,
    ) -> BacktestMetrics:
        """Run backtest.
        
        Args:
            data: DataFrame with OHLCV data
            signal_generator: Function that generates trading signals
            position_sizer: Function that calculates position size
            
        Returns:
            BacktestMetrics object
        """
        self.equity = self.initial_capital
        self.trades = []
        self.equity_curve = [self.initial_capital]
        self.timestamps = [data.index[0]]
        
        position = None
        entry_price = None
        entry_time = None
        
        for i in range(1, len(data)):
            current_row = data.iloc[i]
            current_price = current_row["close"]
            current_time = data.index[i]
            
            # Generate signal
            signal = signal_generator(data.iloc[:i+1])
            
            # Close position if signal changes
            if position is not None and signal != position:
                exit_price = current_price * (1 - self.slippage_pct / 100)
                pnl = self._calculate_pnl(
                    position, entry_price, exit_price, position_size=self.equity * self.leverage
                )
                
                self.trades.append({
                    "entry_time": entry_time,
                    "exit_time": current_time,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "position": position,
                    "pnl": pnl,
                })
                
                self.equity += pnl
                position = None
                entry_price = None
                entry_time = None
            
            # Open new position
            if position is None and signal != 0:
                entry_price = current_price * (1 + self.slippage_pct / 100)
                position = signal
                entry_time = current_time
            
            # Update equity curve
            if position is not None:
                unrealized_pnl = self._calculate_pnl(
                    position, entry_price, current_price, position_size=self.equity * self.leverage
                )
                current_equity = self.equity + unrealized_pnl
            else:
                current_equity = self.equity
            
            self.equity_curve.append(current_equity)
            self.timestamps.append(current_time)
        
        # Close final position
        if position is not None:
            exit_price = data.iloc[-1]["close"]
            pnl = self._calculate_pnl(
                position, entry_price, exit_price, position_size=self.equity * self.leverage
            )
            
            self.trades.append({
                "entry_time": entry_time,
                "exit_time": data.index[-1],
                "entry_price": entry_price,
                "exit_price": exit_price,
                "position": position,
                "pnl": pnl,
            })
            
            self.equity += pnl
        
        # Calculate metrics
        equity_series = pd.Series(self.equity_curve, index=self.timestamps)
        metrics = MetricsCalculator.calculate_metrics(equity_series, self.trades)
        
        logger.info(f"Backtest completed: {metrics}")
        return metrics
    
    def _calculate_pnl(
        self,
        position: int,
        entry_price: float,
        exit_price: float,
        position_size: float,
    ) -> float:
        """Calculate P&L for a trade.
        
        Args:
            position: 1 for long, -1 for short
            entry_price: Entry price
            exit_price: Exit price
            position_size: Position size in USD
            
        Returns:
            P&L in USD
        """
        if position == 1:  # Long
            price_change = exit_price - entry_price
        else:  # Short
            price_change = entry_price - exit_price
        
        # Calculate return
        return_pct = price_change / entry_price
        
        # Calculate P&L
        pnl = position_size * return_pct
        
        # Subtract fees
        fees = position_size * self.taker_fee * 2  # Entry and exit
        pnl -= fees
        
        return pnl
    
    def get_equity_curve(self) -> pd.Series:
        """Get equity curve.
        
        Returns:
            Series with equity values
        """
        return pd.Series(self.equity_curve, index=self.timestamps)
    
    def get_trades(self) -> pd.DataFrame:
        """Get trades as DataFrame.
        
        Returns:
            DataFrame with trade details
        """
        if not self.trades:
            return pd.DataFrame()
        
        return pd.DataFrame(self.trades)

