"""Example: Data Collection from Binance."""

import sys
from datetime import datetime, timedelta

sys.path.insert(0, "/Users/phucbao/Documents/Binance")

from src.data import BinanceDataClient, DataManager
from src.utils import Config, setup_logger, TimeUtils

# Setup logging
setup_logger("data_collection", log_level="INFO")

def main():
    """Collect historical data from Binance."""
    
    # Load configuration
    config = Config()
    
    # Initialize clients
    client = BinanceDataClient(
        api_key=config.get("binance.api_key", ""),
        api_secret=config.get("binance.api_secret", ""),
        testnet=config.get("binance.testnet", True),
    )
    
    data_manager = DataManager()
    
    # Configuration
    symbols = config.get("data_collection.symbols", ["BTCUSDT"])
    timeframes = config.get("data_collection.timeframes", ["1h", "1d"])
    
    print(f"Collecting data for symbols: {symbols}")
    print(f"Timeframes: {timeframes}")
    
    # Collect klines data
    for symbol in symbols:
        for timeframe in timeframes:
            print(f"\nCollecting {symbol} {timeframe}...")
            
            try:
                # Get historical data
                df = client.get_klines(
                    symbol=symbol,
                    interval=timeframe,
                    limit=1000,
                )
                
                print(f"  Retrieved {len(df)} candles")
                print(f"  Date range: {df['open_time'].min()} to {df['open_time'].max()}")
                print(f"  Price range: ${df['low'].min():.2f} - ${df['high'].max():.2f}")
                
                # Save data
                data_manager.save_klines(symbol, timeframe, df, data_type="raw")
                print(f"  Saved to disk")
                
            except Exception as e:
                print(f"  Error: {e}")
    
    # Collect funding rates
    print("\n\nCollecting funding rates...")
    for symbol in symbols:
        try:
            df_funding = client.get_funding_rate_history(
                symbol=symbol,
                limit=1000,
            )
            
            print(f"  {symbol}: Retrieved {len(df_funding)} funding rate records")
            print(f"  Funding rate range: {df_funding['fundingRate'].min():.6f} to {df_funding['fundingRate'].max():.6f}")
            
            data_manager.save_funding_rates(symbol, df_funding)
            print(f"  Saved to disk")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Collect open interest
    print("\n\nCollecting open interest...")
    for symbol in symbols:
        try:
            df_oi = client.get_open_interest(
                symbol=symbol,
                period="1h",
                limit=1000,
            )
            
            print(f"  {symbol}: Retrieved {len(df_oi)} open interest records")
            
            data_manager.save_open_interest(symbol, df_oi)
            print(f"  Saved to disk")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n\nData collection completed!")

if __name__ == "__main__":
    main()

