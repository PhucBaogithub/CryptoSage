"""Time utilities for the trading system."""

from datetime import datetime, timedelta, timezone
from typing import Dict

import pandas as pd
import pytz


class TimeUtils:
    """Utility class for time operations."""
    
    # Timeframe to minutes mapping
    TIMEFRAME_MINUTES: Dict[str, int] = {
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "4h": 240,
        "1d": 1440,
        "1w": 10080,
        "1M": 43200,
    }
    
    @staticmethod
    def get_utc_now() -> datetime:
        """Get current UTC time.
        
        Returns:
            Current UTC datetime
        """
        return datetime.now(timezone.utc)
    
    @staticmethod
    def timestamp_to_datetime(timestamp_ms: int) -> datetime:
        """Convert millisecond timestamp to datetime.
        
        Args:
            timestamp_ms: Timestamp in milliseconds
            
        Returns:
            Datetime object in UTC
        """
        return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
    
    @staticmethod
    def datetime_to_timestamp(dt: datetime) -> int:
        """Convert datetime to millisecond timestamp.
        
        Args:
            dt: Datetime object
            
        Returns:
            Timestamp in milliseconds
        """
        return int(dt.timestamp() * 1000)
    
    @staticmethod
    def timeframe_to_minutes(timeframe: str) -> int:
        """Convert timeframe string to minutes.
        
        Args:
            timeframe: Timeframe string (e.g., "1h", "5m")
            
        Returns:
            Number of minutes
            
        Raises:
            ValueError: If timeframe is not recognized
        """
        if timeframe not in TimeUtils.TIMEFRAME_MINUTES:
            raise ValueError(f"Unknown timeframe: {timeframe}")
        return TimeUtils.TIMEFRAME_MINUTES[timeframe]
    
    @staticmethod
    def minutes_to_timedelta(minutes: int) -> timedelta:
        """Convert minutes to timedelta.
        
        Args:
            minutes: Number of minutes
            
        Returns:
            Timedelta object
        """
        return timedelta(minutes=minutes)
    
    @staticmethod
    def get_candle_start_time(timestamp: datetime, timeframe: str) -> datetime:
        """Get the start time of a candle.
        
        Args:
            timestamp: Any time within the candle
            timeframe: Timeframe string
            
        Returns:
            Start time of the candle
        """
        minutes = TimeUtils.timeframe_to_minutes(timeframe)
        
        # Convert to minutes since epoch
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        minutes_since_epoch = int((timestamp - epoch).total_seconds() / 60)
        
        # Round down to nearest candle
        candle_start_minutes = (minutes_since_epoch // minutes) * minutes
        
        # Convert back to datetime
        return epoch + timedelta(minutes=candle_start_minutes)
    
    @staticmethod
    def get_candle_end_time(timestamp: datetime, timeframe: str) -> datetime:
        """Get the end time of a candle.
        
        Args:
            timestamp: Any time within the candle
            timeframe: Timeframe string
            
        Returns:
            End time of the candle
        """
        start_time = TimeUtils.get_candle_start_time(timestamp, timeframe)
        minutes = TimeUtils.timeframe_to_minutes(timeframe)
        return start_time + timedelta(minutes=minutes)
    
    @staticmethod
    def parse_date(date_str: str, format: str = "%Y-%m-%d") -> datetime:
        """Parse date string to datetime.
        
        Args:
            date_str: Date string
            format: Date format
            
        Returns:
            Datetime object in UTC
        """
        dt = datetime.strptime(date_str, format)
        return dt.replace(tzinfo=timezone.utc)
    
    @staticmethod
    def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime to string.
        
        Args:
            dt: Datetime object
            format: Output format
            
        Returns:
            Formatted datetime string
        """
        return dt.strftime(format)

