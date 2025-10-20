"""Backtesting metrics and performance analysis."""

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd


@dataclass
class BacktestMetrics:
    """Backtesting performance metrics."""
    
    total_return_pct: float
    annual_return_pct: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown_pct: float
    calmar_ratio: float
    win_rate_pct: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win_usd: float
    avg_loss_usd: float
    largest_win_usd: float
    largest_loss_usd: float
    consecutive_wins: int
    consecutive_losses: int
    
    def __str__(self) -> str:
        """String representation."""
        return f"""
Backtesting Metrics:
  Total Return: {self.total_return_pct:.2f}%
  Annual Return: {self.annual_return_pct:.2f}%
  Sharpe Ratio: {self.sharpe_ratio:.2f}
  Sortino Ratio: {self.sortino_ratio:.2f}
  Max Drawdown: {self.max_drawdown_pct:.2f}%
  Calmar Ratio: {self.calmar_ratio:.2f}
  Win Rate: {self.win_rate_pct:.2f}%
  Profit Factor: {self.profit_factor:.2f}
  Total Trades: {self.total_trades}
  Winning Trades: {self.winning_trades}
  Losing Trades: {self.losing_trades}
  Avg Win: ${self.avg_win_usd:.2f}
  Avg Loss: ${self.avg_loss_usd:.2f}
  Largest Win: ${self.largest_win_usd:.2f}
  Largest Loss: ${self.largest_loss_usd:.2f}
  Consecutive Wins: {self.consecutive_wins}
  Consecutive Losses: {self.consecutive_losses}
"""


class MetricsCalculator:
    """Calculates backtesting metrics."""
    
    @staticmethod
    def calculate_metrics(
        equity_curve: pd.Series,
        trades: List[Dict],
        risk_free_rate: float = 0.02,
    ) -> BacktestMetrics:
        """Calculate comprehensive backtesting metrics.
        
        Args:
            equity_curve: Series with equity values over time
            trades: List of trade dictionaries with entry/exit prices and P&L
            risk_free_rate: Annual risk-free rate for Sharpe ratio
            
        Returns:
            BacktestMetrics object
        """
        # Returns
        returns = equity_curve.pct_change().dropna()
        total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0] - 1) * 100
        
        # Annualized return
        days = (equity_curve.index[-1] - equity_curve.index[0]).days
        years = days / 365.25
        annual_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (1 / years) - 1
        annual_return_pct = annual_return * 100
        
        # Sharpe ratio
        excess_returns = returns - risk_free_rate / 252
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
        
        # Sortino ratio (only downside volatility)
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std()
        sortino_ratio = np.sqrt(252) * excess_returns.mean() / downside_std if downside_std > 0 else 0
        
        # Max drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown_pct = drawdown.min() * 100
        
        # Calmar ratio
        calmar_ratio = annual_return / abs(max_drawdown_pct / 100) if max_drawdown_pct != 0 else 0
        
        # Trade statistics
        if trades:
            pnls = [t.get("pnl", 0) for t in trades]
            winning_trades = sum(1 for p in pnls if p > 0)
            losing_trades = sum(1 for p in pnls if p < 0)
            total_trades = len(trades)
            win_rate_pct = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            gross_profit = sum(p for p in pnls if p > 0)
            gross_loss = abs(sum(p for p in pnls if p < 0))
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
            
            avg_win = gross_profit / winning_trades if winning_trades > 0 else 0
            avg_loss = gross_loss / losing_trades if losing_trades > 0 else 0
            
            largest_win = max(pnls) if pnls else 0
            largest_loss = min(pnls) if pnls else 0
            
            # Consecutive wins/losses
            consecutive_wins = MetricsCalculator._max_consecutive(pnls, lambda x: x > 0)
            consecutive_losses = MetricsCalculator._max_consecutive(pnls, lambda x: x < 0)
        else:
            winning_trades = 0
            losing_trades = 0
            total_trades = 0
            win_rate_pct = 0
            profit_factor = 0
            avg_win = 0
            avg_loss = 0
            largest_win = 0
            largest_loss = 0
            consecutive_wins = 0
            consecutive_losses = 0
        
        return BacktestMetrics(
            total_return_pct=total_return,
            annual_return_pct=annual_return_pct,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            max_drawdown_pct=max_drawdown_pct,
            calmar_ratio=calmar_ratio,
            win_rate_pct=win_rate_pct,
            profit_factor=profit_factor,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            avg_win_usd=avg_win,
            avg_loss_usd=avg_loss,
            largest_win_usd=largest_win,
            largest_loss_usd=largest_loss,
            consecutive_wins=consecutive_wins,
            consecutive_losses=consecutive_losses,
        )
    
    @staticmethod
    def _max_consecutive(values: List, condition) -> int:
        """Calculate maximum consecutive values meeting condition.
        
        Args:
            values: List of values
            condition: Function to test condition
            
        Returns:
            Maximum consecutive count
        """
        max_count = 0
        current_count = 0
        
        for value in values:
            if condition(value):
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        
        return max_count

