"""Example: Model Training."""

import sys

import numpy as np

sys.path.insert(0, "/Users/phucbao/Documents/Binance")

from src.data import DataManager
from src.models import LongTermModel, ShortTermModel
from src.utils import setup_logger

# Setup logging
setup_logger("model_training", log_level="INFO")

def prepare_data(df, input_length=168, output_length=30):
    """Prepare data for training.
    
    Args:
        df: DataFrame with features
        input_length: Input sequence length
        output_length: Output sequence length
        
    Returns:
        X, y arrays
    """
    X = []
    y = []
    
    for i in range(len(df) - input_length - output_length):
        X.append(df.iloc[i:i+input_length].values)
        
        # Target: next output_length returns
        future_returns = df["log_return"].iloc[i+input_length:i+input_length+output_length].values
        mean_return = np.mean(future_returns)
        std_return = np.std(future_returns)
        skew_return = (np.mean((future_returns - mean_return) ** 3)) / (std_return ** 3) if std_return > 0 else 0
        
        y.append([mean_return, std_return, skew_return])
    
    return np.array(X), np.array(y)

def main():
    """Train long-term and short-term models."""
    
    # Load data
    data_manager = DataManager()
    
    symbol = "BTCUSDT"
    timeframe = "1h"
    
    print(f"Loading {symbol} {timeframe} data...")
    df = data_manager.load_klines(symbol, timeframe, data_type="processed")
    
    if df is None or df.empty:
        print("No processed data found. Please run 02_feature_engineering.py first.")
        return
    
    print(f"Loaded {len(df)} candles")
    
    # Select features (exclude time columns)
    feature_cols = [col for col in df.columns if col not in ["open_time", "close_time"]]
    df_features = df[feature_cols].fillna(0)
    
    print(f"Using {len(feature_cols)} features")
    
    # Prepare data
    print("\nPreparing data for long-term model...")
    X_long, y_long = prepare_data(df_features, input_length=168, output_length=30)
    
    print(f"  X shape: {X_long.shape}")
    print(f"  y shape: {y_long.shape}")
    
    # Split into train/val
    split_idx = int(len(X_long) * 0.8)
    X_train = X_long[:split_idx]
    y_train = y_long[:split_idx]
    X_val = X_long[split_idx:]
    y_val = y_long[split_idx:]
    
    print(f"  Train: {X_train.shape[0]} samples")
    print(f"  Val: {X_val.shape[0]} samples")
    
    # Train long-term model
    print("\nTraining long-term model...")
    config_long = {
        "input_size": X_train.shape[2],
        "input_length": 168,
        "hidden_size": 64,
        "num_heads": 4,
        "num_layers": 2,
        "output_length": 30,
        "dropout": 0.1,
        "batch_size": 32,
        "epochs": 10,  # Reduced for demo
        "learning_rate": 0.001,
        "early_stopping_patience": 5,
    }
    
    model_long = LongTermModel(config_long)
    history_long = model_long.train(X_train, y_train, X_val, y_val)
    
    print(f"  Final train loss: {history_long['train_loss'][-1]:.6f}")
    if history_long['val_loss']:
        print(f"  Final val loss: {history_long['val_loss'][-1]:.6f}")
    
    # Save model
    model_long.save_model("models/long_term_model.pt")
    print("  Model saved to models/long_term_model.pt")
    
    # Train short-term model
    print("\nPreparing data for short-term model...")
    X_short, y_short = prepare_data(df_features, input_length=60, output_length=5)
    
    print(f"  X shape: {X_short.shape}")
    print(f"  y shape: {y_short.shape}")
    
    # Create classification targets (up/down/neutral)
    y_short_class = np.zeros((len(y_short), 3))
    for i, (mean, std, skew) in enumerate(y_short):
        if mean > 0.001:
            y_short_class[i, 0] = 1  # Up
        elif mean < -0.001:
            y_short_class[i, 1] = 1  # Down
        else:
            y_short_class[i, 2] = 1  # Neutral
    
    # Split
    split_idx = int(len(X_short) * 0.8)
    X_train_short = X_short[:split_idx]
    y_train_short = y_short_class[:split_idx]
    X_val_short = X_short[split_idx:]
    y_val_short = y_short_class[split_idx:]
    
    print(f"  Train: {X_train_short.shape[0]} samples")
    print(f"  Val: {X_val_short.shape[0]} samples")
    
    print("\nTraining short-term model...")
    config_short = {
        "input_size": X_train_short.shape[2],
        "input_length": 60,
        "hidden_size": 128,
        "num_heads": 8,
        "num_layers": 3,
        "dropout": 0.1,
        "batch_size": 64,
        "epochs": 10,  # Reduced for demo
        "learning_rate": 0.0005,
        "early_stopping_patience": 5,
    }
    
    model_short = ShortTermModel(config_short)
    history_short = model_short.train(X_train_short, y_train_short, X_val_short, y_val_short)
    
    print(f"  Final train loss: {history_short['train_loss'][-1]:.6f}")
    if history_short['val_loss']:
        print(f"  Final val loss: {history_short['val_loss'][-1]:.6f}")
    
    # Save model
    model_short.save_model("models/short_term_model.pt")
    print("  Model saved to models/short_term_model.pt")
    
    print("\nModel training completed!")

if __name__ == "__main__":
    main()

