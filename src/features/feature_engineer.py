"""Feature engineering for price prediction and trading signals."""

from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import talib
from ta import add_all_ta_features

from ..utils import get_logger

logger = get_logger(__name__)


class FeatureEngineer:
    """Generates features for machine learning models."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize feature engineer.
        
        Args:
            config: Configuration dictionary for features
        """
        self.config = config or {}
        logger.info("FeatureEngineer initialized")
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer all features from OHLCV data.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with engineered features
        """
        df = df.copy()
        
        # Price features
        df = self._add_price_features(df)
        
        # Technical indicators
        df = self._add_technical_indicators(df)
        
        # Liquidity features
        df = self._add_liquidity_features(df)
        
        # Volatility features
        df = self._add_volatility_features(df)
        
        # Trend features
        df = self._add_trend_features(df)
        
        logger.info(f"Engineered {len(df.columns)} features")
        return df
    
    def _add_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add price-based features.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with price features
        """
        # Log returns
        df["log_return"] = np.log(df["close"] / df["close"].shift(1))
        
        # Multi-period returns
        for period in [5, 20, 60]:
            df[f"return_{period}"] = df["close"].pct_change(period)
            df[f"log_return_{period}"] = np.log(df["close"] / df["close"].shift(period))
        
        # Price momentum
        df["momentum_5"] = df["close"] - df["close"].shift(5)
        df["momentum_20"] = df["close"] - df["close"].shift(20)
        
        # Price rate of change
        df["roc_5"] = (df["close"] - df["close"].shift(5)) / df["close"].shift(5)
        df["roc_20"] = (df["close"] - df["close"].shift(20)) / df["close"].shift(20)
        
        return df
    
    def _add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add technical indicators.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with technical indicators
        """
        # RSI
        df["rsi_14"] = talib.RSI(df["close"], timeperiod=14)
        df["rsi_7"] = talib.RSI(df["close"], timeperiod=7)
        
        # MACD
        macd, signal, hist = talib.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)
        df["macd"] = macd
        df["macd_signal"] = signal
        df["macd_hist"] = hist
        
        # Bollinger Bands
        upper, middle, lower = talib.BBANDS(df["close"], timeperiod=20)
        df["bb_upper"] = upper
        df["bb_middle"] = middle
        df["bb_lower"] = lower
        df["bb_width"] = (upper - lower) / middle
        df["bb_position"] = (df["close"] - lower) / (upper - lower)
        
        # ATR (Average True Range)
        df["atr_14"] = talib.ATR(df["high"], df["low"], df["close"], timeperiod=14)
        
        # ADX
        df["adx_14"] = talib.ADX(df["high"], df["low"], df["close"], timeperiod=14)
        
        # EMA
        for period in [8, 21, 55]:
            df[f"ema_{period}"] = talib.EMA(df["close"], timeperiod=period)
        
        # SMA
        for period in [20, 50, 200]:
            df[f"sma_{period}"] = talib.SMA(df["close"], timeperiod=period)
        
        return df
    
    def _add_liquidity_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add liquidity-based features.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with liquidity features
        """
        # Volume features
        df["volume_sma_20"] = df["volume"].rolling(20).mean()
        df["volume_ratio"] = df["volume"] / df["volume_sma_20"]
        
        # On-Balance Volume
        df["obv"] = (np.sign(df["close"].diff()) * df["volume"]).fillna(0).cumsum()
        
        # Volume Rate of Change
        df["vroc_5"] = (df["volume"] - df["volume"].shift(5)) / df["volume"].shift(5)
        
        return df
    
    def _add_volatility_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volatility features.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with volatility features
        """
        # Historical volatility
        for period in [5, 20, 60]:
            df[f"volatility_{period}"] = df["log_return"].rolling(period).std()
        
        # Parkinson volatility
        df["parkinson_vol"] = np.sqrt(
            np.log(df["high"] / df["low"]) ** 2 / (4 * np.log(2))
        ).rolling(20).mean()
        
        # Garman-Klass volatility
        hl = np.log(df["high"] / df["low"])
        co = np.log(df["close"] / df["open"])
        df["gk_vol"] = (0.5 * hl ** 2 - (2 * np.log(2) - 1) * co ** 2).rolling(20).mean()
        
        return df
    
    def _add_trend_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add trend-based features.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with trend features
        """
        # Trend direction
        df["trend_5"] = np.where(df["close"] > df["close"].shift(5), 1, -1)
        df["trend_20"] = np.where(df["close"] > df["close"].shift(20), 1, -1)
        
        # Higher High / Lower Low
        df["hh_5"] = df["high"].rolling(5).max() == df["high"]
        df["ll_5"] = df["low"].rolling(5).min() == df["low"]
        
        # Close position in range
        df["close_position_5"] = (df["close"] - df["low"].rolling(5).min()) / (
            df["high"].rolling(5).max() - df["low"].rolling(5).min()
        )
        
        return df
    
    def add_funding_rate_features(
        self,
        klines_df: pd.DataFrame,
        funding_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Add funding rate features.
        
        Args:
            klines_df: DataFrame with klines data
            funding_df: DataFrame with funding rates
            
        Returns:
            DataFrame with funding rate features
        """
        klines_df = klines_df.copy()
        
        # Merge funding rates
        klines_df = klines_df.merge_asof(
            funding_df[["fundingTime", "fundingRate"]],
            left_on="close_time",
            right_on="fundingTime",
            direction="backward",
        )
        
        # Funding rate features
        klines_df["funding_rate"] = klines_df["fundingRate"]
        klines_df["funding_rate_sma_8"] = klines_df["funding_rate"].rolling(8).mean()
        klines_df["funding_rate_std_8"] = klines_df["funding_rate"].rolling(8).std()
        
        return klines_df
    
    def add_open_interest_features(
        self,
        klines_df: pd.DataFrame,
        oi_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Add open interest features.
        
        Args:
            klines_df: DataFrame with klines data
            oi_df: DataFrame with open interest
            
        Returns:
            DataFrame with open interest features
        """
        klines_df = klines_df.copy()
        
        # Merge open interest
        klines_df = klines_df.merge_asof(
            oi_df[["timestamp", "sumOpenInterest", "sumOpenInterestValue"]],
            left_on="close_time",
            right_on="timestamp",
            direction="backward",
        )
        
        # Open interest features
        klines_df["open_interest"] = klines_df["sumOpenInterest"]
        klines_df["oi_change_pct"] = klines_df["open_interest"].pct_change()
        klines_df["oi_sma_24"] = klines_df["open_interest"].rolling(24).mean()
        
        return klines_df

