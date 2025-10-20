"""Example: Backtesting."""

import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/Users/phucbao/Documents/Binance")

from src.backtesting import BacktestEngine
from src.data import DataManager
from src.utils import setup_logger

# Setup logging
setup_logger("backtesting", log_level="INFO")

def simple_signal_generator(df):
    """Generate simple trading signals based on moving averages.
    
    Args:
        df: DataFrame with OHLCV data
        
    Returns:
        Signal: 1 (long), -1 (short), 0 (neutral)
    """
    if len(df) < 50:
        return 0
    
    # Simple MA crossover
    sma_20 = df["close"].rolling(20).mean().iloc[-1]
    sma_50 = df["close"].rolling(50).mean().iloc[-1]
    
    if sma_20 > sma_50:
        return 1  # Long
    elif sma_20 < sma_50:
        return -1  # Short
    else:
        return 0  # Neutral

def simple_position_sizer(equity, signal):
    """Simple position sizing.
    
    Args:
        equity: Current equity
        signal: Trading signal
        
    Returns:
        Position size
    """
    if signal == 0:
        return 0
    return equity * 0.02  # Risk 2% per trade

def main():
    """Run backtest."""
    
    # Load data
    data_manager = DataManager()
    
    symbol = "BTCUSDT"
    timeframe = "1h"
    
    print(f"Loading {symbol} {timeframe} data...")
    df = data_manager.load_klines(symbol, timeframe, data_type="raw")
    
    if df is None or df.empty:
        print("No data found. Please run 01_data_collection.py first.")
        return
    
    print(f"Loaded {len(df)} candles")
    print(f"Date range: {df['open_time'].min()} to {df['open_time'].max()}")
    
    # Set index to timestamp
    df = df.set_index("open_time")
    
    # Run backtest
    print("\nRunning backtest...")
    engine = BacktestEngine(
        initial_capital=100000,
        maker_fee=0.0002,
        taker_fee=0.0004,
        slippage_pct=0.01,
        leverage=3.0,
    )
    
    metrics = engine.run(df, simple_signal_generator, simple_position_sizer)
    
    # Display results
    print("\n" + "="*60)
    print("BACKTEST RESULTS")
    print("="*60)
    print(metrics)
    
    # Get equity curve
    equity_curve = engine.get_equity_curve()
    print(f"\nEquity Curve Statistics:")
    print(f"  Initial: ${equity_curve.iloc[0]:,.2f}")
    print(f"  Final: ${equity_curve.iloc[-1]:,.2f}")
    print(f"  Min: ${equity_curve.min():,.2f}")
    print(f"  Max: ${equity_curve.max():,.2f}")
    
    # Get trades
    trades_df = engine.get_trades()
    if not trades_df.empty:
        print(f"\nTrades Summary:")
        print(f"  Total trades: {len(trades_df)}")
        print(f"  Winning trades: {(trades_df['pnl'] > 0).sum()}")
        print(f"  Losing trades: {(trades_df['pnl'] < 0).sum()}")
        print(f"  Total P&L: ${trades_df['pnl'].sum():,.2f}")
        print(f"  Avg P&L: ${trades_df['pnl'].mean():,.2f}")
        print(f"  Max win: ${trades_df['pnl'].max():,.2f}")
        print(f"  Max loss: ${trades_df['pnl'].min():,.2f}")
        
        print(f"\nFirst 5 trades:")
        print(trades_df.head())
    
    print("\nBacktest completed!")

if __name__ == "__main__":
    main()

