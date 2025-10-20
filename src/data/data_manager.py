"""Data management and storage."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from ..utils import TimeUtils, get_logger

logger = get_logger(__name__)


class DataManager:
    """Manages data storage and retrieval."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize data manager.
        
        Args:
            data_dir: Base directory for data storage
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.cache_dir = self.data_dir / "cache"
        
        # Create directories
        for dir_path in [self.raw_dir, self.processed_dir, self.cache_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"DataManager initialized with data_dir={data_dir}")
    
    def save_klines(
        self,
        symbol: str,
        interval: str,
        df: pd.DataFrame,
        data_type: str = "raw",
    ) -> Path:
        """Save klines data to disk.
        
        Args:
            symbol: Trading pair
            interval: Kline interval
            df: DataFrame with klines data
            data_type: Type of data ("raw" or "processed")
            
        Returns:
            Path to saved file
        """
        if data_type == "raw":
            dir_path = self.raw_dir
        else:
            dir_path = self.processed_dir
        
        # Create symbol directory
        symbol_dir = dir_path / symbol
        symbol_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = symbol_dir / f"klines_{interval}.parquet"
        df.to_parquet(file_path)
        
        logger.info(f"Saved {len(df)} klines to {file_path}")
        return file_path
    
    def load_klines(
        self,
        symbol: str,
        interval: str,
        data_type: str = "raw",
    ) -> Optional[pd.DataFrame]:
        """Load klines data from disk.
        
        Args:
            symbol: Trading pair
            interval: Kline interval
            data_type: Type of data ("raw" or "processed")
            
        Returns:
            DataFrame with klines data or None if not found
        """
        if data_type == "raw":
            dir_path = self.raw_dir
        else:
            dir_path = self.processed_dir
        
        file_path = dir_path / symbol / f"klines_{interval}.parquet"
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return None
        
        df = pd.read_parquet(file_path)
        logger.info(f"Loaded {len(df)} klines from {file_path}")
        return df
    
    def save_funding_rates(
        self,
        symbol: str,
        df: pd.DataFrame,
    ) -> Path:
        """Save funding rates data to disk.
        
        Args:
            symbol: Trading pair
            df: DataFrame with funding rates
            
        Returns:
            Path to saved file
        """
        symbol_dir = self.raw_dir / symbol
        symbol_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = symbol_dir / "funding_rates.parquet"
        df.to_parquet(file_path)
        
        logger.info(f"Saved {len(df)} funding rates to {file_path}")
        return file_path
    
    def load_funding_rates(self, symbol: str) -> Optional[pd.DataFrame]:
        """Load funding rates data from disk.
        
        Args:
            symbol: Trading pair
            
        Returns:
            DataFrame with funding rates or None if not found
        """
        file_path = self.raw_dir / symbol / "funding_rates.parquet"
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return None
        
        df = pd.read_parquet(file_path)
        logger.info(f"Loaded {len(df)} funding rates from {file_path}")
        return df
    
    def save_open_interest(
        self,
        symbol: str,
        df: pd.DataFrame,
    ) -> Path:
        """Save open interest data to disk.
        
        Args:
            symbol: Trading pair
            df: DataFrame with open interest
            
        Returns:
            Path to saved file
        """
        symbol_dir = self.raw_dir / symbol
        symbol_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = symbol_dir / "open_interest.parquet"
        df.to_parquet(file_path)
        
        logger.info(f"Saved {len(df)} open interest records to {file_path}")
        return file_path
    
    def load_open_interest(self, symbol: str) -> Optional[pd.DataFrame]:
        """Load open interest data from disk.
        
        Args:
            symbol: Trading pair
            
        Returns:
            DataFrame with open interest or None if not found
        """
        file_path = self.raw_dir / symbol / "open_interest.parquet"
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return None
        
        df = pd.read_parquet(file_path)
        logger.info(f"Loaded {len(df)} open interest records from {file_path}")
        return df
    
    def get_latest_timestamp(
        self,
        symbol: str,
        interval: str,
        data_type: str = "raw",
    ) -> Optional[datetime]:
        """Get the latest timestamp in stored klines data.
        
        Args:
            symbol: Trading pair
            interval: Kline interval
            data_type: Type of data ("raw" or "processed")
            
        Returns:
            Latest timestamp or None if no data found
        """
        df = self.load_klines(symbol, interval, data_type)
        if df is None or df.empty:
            return None
        
        return df["close_time"].max()

