"""Example: Feature Engineering."""

import sys

sys.path.insert(0, "/Users/phucbao/Documents/Binance")

from src.data import DataManager
from src.features import FeatureEngineer
from src.utils import setup_logger

# Setup logging
setup_logger("feature_engineering", log_level="INFO")

def main():
    """Engineer features from raw OHLCV data."""
    
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
    print(f"Columns: {df.columns.tolist()}")
    
    # Engineer features
    print("\nEngineering features...")
    engineer = FeatureEngineer()
    df_features = engineer.engineer_features(df)
    
    print(f"Engineered {len(df_features.columns)} features")
    print(f"\nFeature columns:")
    for col in df_features.columns:
        print(f"  - {col}")
    
    # Display statistics
    print(f"\nFeature statistics:")
    print(df_features.describe())
    
    # Check for missing values
    print(f"\nMissing values:")
    missing = df_features.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("  No missing values")
    
    # Save processed data
    print(f"\nSaving processed data...")
    data_manager.save_klines(symbol, timeframe, df_features, data_type="processed")
    print("Saved!")
    
    # Display sample
    print(f"\nSample data (last 5 rows):")
    print(df_features.tail())

if __name__ == "__main__":
    main()

