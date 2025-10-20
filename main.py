"""Main entry point for Bitcoin Futures Trading System."""

import argparse
import sys
from pathlib import Path

from src.utils import Config, setup_logger

# Setup logging
setup_logger("main", log_level="INFO")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Bitcoin Futures Trading System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py collect-data
  python main.py engineer-features
  python main.py train-models
  python main.py backtest
  python main.py trade --mode paper
        """,
    )
    
    parser.add_argument(
        "command",
        choices=[
            "collect-data",
            "engineer-features",
            "train-models",
            "backtest",
            "trade",
            "monitor",
        ],
        help="Command to execute",
    )
    
    parser.add_argument(
        "--mode",
        choices=["paper", "testnet", "live"],
        default="paper",
        help="Execution mode (default: paper)",
    )
    
    parser.add_argument(
        "--symbol",
        default="BTCUSDT",
        help="Trading symbol (default: BTCUSDT)",
    )
    
    parser.add_argument(
        "--config",
        default="config/config.yaml",
        help="Configuration file path",
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config(args.config)
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║   Bitcoin Futures Trading System                           ║
║   Command: {args.command:<45} ║
║   Mode: {args.mode:<52} ║
║   Symbol: {args.symbol:<50} ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    try:
        if args.command == "collect-data":
            from examples.example_01_data_collection import main as collect_data
            collect_data()
        
        elif args.command == "engineer-features":
            from examples.example_02_feature_engineering import main as engineer_features
            engineer_features()
        
        elif args.command == "train-models":
            from examples.example_03_model_training import main as train_models
            train_models()
        
        elif args.command == "backtest":
            from examples.example_04_backtesting import main as backtest
            backtest()
        
        elif args.command == "trade":
            print(f"Starting trading in {args.mode} mode...")
            print("Trading functionality coming soon!")
        
        elif args.command == "monitor":
            print("Starting monitoring...")
            print("Monitoring functionality coming soon!")
        
        print("\n✓ Command completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

