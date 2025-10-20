"""Unit tests for utility modules."""

import pytest
from datetime import datetime, timezone

from src.utils import TimeUtils


class TestTimeUtils:
    """Test TimeUtils class."""
    
    def test_get_utc_now(self):
        """Test getting current UTC time."""
        now = TimeUtils.get_utc_now()
        assert isinstance(now, datetime)
        assert now.tzinfo == timezone.utc
    
    def test_timestamp_conversion(self):
        """Test timestamp conversion."""
        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        timestamp = TimeUtils.datetime_to_timestamp(dt)
        dt_back = TimeUtils.timestamp_to_datetime(timestamp)
        
        assert dt_back.year == dt.year
        assert dt_back.month == dt.month
        assert dt_back.day == dt.day
        assert dt_back.hour == dt.hour
    
    def test_timeframe_to_minutes(self):
        """Test timeframe to minutes conversion."""
        assert TimeUtils.timeframe_to_minutes("1m") == 1
        assert TimeUtils.timeframe_to_minutes("5m") == 5
        assert TimeUtils.timeframe_to_minutes("1h") == 60
        assert TimeUtils.timeframe_to_minutes("1d") == 1440
    
    def test_invalid_timeframe(self):
        """Test invalid timeframe raises error."""
        with pytest.raises(ValueError):
            TimeUtils.timeframe_to_minutes("invalid")
    
    def test_candle_start_time(self):
        """Test candle start time calculation."""
        dt = datetime(2024, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        
        # 1-hour candle
        start = TimeUtils.get_candle_start_time(dt, "1h")
        assert start.hour == 12
        assert start.minute == 0
        
        # 5-minute candle
        start = TimeUtils.get_candle_start_time(dt, "5m")
        assert start.minute == 30
    
    def test_date_parsing(self):
        """Test date parsing."""
        date_str = "2024-01-01"
        dt = TimeUtils.parse_date(date_str)
        
        assert dt.year == 2024
        assert dt.month == 1
        assert dt.day == 1
        assert dt.tzinfo == timezone.utc
    
    def test_datetime_formatting(self):
        """Test datetime formatting."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        formatted = TimeUtils.format_datetime(dt)
        
        assert "2024-01-01" in formatted
        assert "12:30:45" in formatted

