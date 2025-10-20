"""Binance API client for data collection."""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

import aiohttp
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException

from ..utils import TimeUtils, get_logger

logger = get_logger(__name__)


class BinanceDataClient:
    """Client for collecting data from Binance APIs."""
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        testnet: bool = False,
    ):
        """Initialize Binance data client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Whether to use testnet
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Initialize REST client
        if testnet:
            self.client = Client(
                api_key=api_key,
                api_secret=api_secret,
                testnet=True,
            )
        else:
            self.client = Client(
                api_key=api_key,
                api_secret=api_secret,
            )
        
        logger.info(f"BinanceDataClient initialized (testnet={testnet})")
    
    def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Get historical klines (candlestick) data.
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            interval: Kline interval (e.g., "1h", "1d")
            start_time: Start time for data collection
            end_time: End time for data collection
            limit: Maximum number of klines to return
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Convert times to milliseconds
            start_ms = TimeUtils.datetime_to_timestamp(start_time) if start_time else None
            end_ms = TimeUtils.datetime_to_timestamp(end_time) if end_time else None
            
            klines = self.client.futures_klines(
                symbol=symbol,
                interval=interval,
                startTime=start_ms,
                endTime=end_ms,
                limit=limit,
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(
                klines,
                columns=[
                    "open_time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "close_time",
                    "quote_asset_volume",
                    "number_of_trades",
                    "taker_buy_base_asset_volume",
                    "taker_buy_quote_asset_volume",
                    "ignore",
                ],
            )
            
            # Convert types
            numeric_cols = [
                "open",
                "high",
                "low",
                "close",
                "volume",
                "quote_asset_volume",
                "taker_buy_base_asset_volume",
                "taker_buy_quote_asset_volume",
            ]
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col])
            
            df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
            df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
            
            logger.info(f"Retrieved {len(df)} klines for {symbol} {interval}")
            return df
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
    
    def get_funding_rate_history(
        self,
        symbol: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Get historical funding rates.
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            start_time: Start time for data collection
            end_time: End time for data collection
            limit: Maximum number of records to return
            
        Returns:
            DataFrame with funding rate data
        """
        try:
            start_ms = TimeUtils.datetime_to_timestamp(start_time) if start_time else None
            end_ms = TimeUtils.datetime_to_timestamp(end_time) if end_time else None
            
            funding_rates = self.client.futures_funding_rate(
                symbol=symbol,
                startTime=start_ms,
                endTime=end_ms,
                limit=limit,
            )
            
            df = pd.DataFrame(funding_rates)
            df["fundingTime"] = pd.to_datetime(df["fundingTime"], unit="ms", utc=True)
            df["fundingRate"] = pd.to_numeric(df["fundingRate"])
            
            logger.info(f"Retrieved {len(df)} funding rates for {symbol}")
            return df
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
    
    def get_open_interest(
        self,
        symbol: str,
        period: str = "5m",
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Get open interest data.
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            period: Period for OI data (e.g., "5m", "1h")
            limit: Maximum number of records to return
            
        Returns:
            DataFrame with open interest data
        """
        try:
            oi_data = self.client.futures_open_interest_hist(
                symbol=symbol,
                period=period,
                limit=limit,
            )
            
            df = pd.DataFrame(oi_data)
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
            df["sumOpenInterest"] = pd.to_numeric(df["sumOpenInterest"])
            df["sumOpenInterestValue"] = pd.to_numeric(df["sumOpenInterestValue"])
            
            logger.info(f"Retrieved {len(df)} open interest records for {symbol}")
            return df
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
    
    def get_mark_price(self, symbol: str) -> Dict:
        """Get current mark price.
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            
        Returns:
            Dictionary with mark price data
        """
        try:
            mark_price = self.client.futures_mark_price(symbol=symbol)
            return mark_price
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
    
    def get_order_book(
        self,
        symbol: str,
        limit: int = 20,
    ) -> Dict:
        """Get current order book snapshot.
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            limit: Number of levels to return
            
        Returns:
            Dictionary with order book data
        """
        try:
            orderbook = self.client.futures_order_book(symbol=symbol, limit=limit)
            return orderbook
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
    
    def get_recent_trades(
        self,
        symbol: str,
        limit: int = 500,
    ) -> pd.DataFrame:
        """Get recent trades.
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            limit: Number of trades to return
            
        Returns:
            DataFrame with trade data
        """
        try:
            trades = self.client.futures_recent_trades(symbol=symbol, limit=limit)
            
            df = pd.DataFrame(trades)
            df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
            df["price"] = pd.to_numeric(df["price"])
            df["qty"] = pd.to_numeric(df["qty"])
            df["quoteQty"] = pd.to_numeric(df["quoteQty"])
            
            logger.info(f"Retrieved {len(df)} recent trades for {symbol}")
            return df
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise

