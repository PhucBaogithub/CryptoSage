"""Risk management for futures trading."""

from dataclasses import dataclass
from typing import Dict, Optional

from ..utils import get_logger

logger = get_logger(__name__)


@dataclass
class RiskMetrics:
    """Risk metrics for a position."""
    
    liquidation_price: float
    liquidation_distance_pct: float
    liquidation_probability: float
    funding_cost_hourly: float
    funding_cost_daily: float
    max_loss_usd: float
    max_loss_pct: float


class RiskManager:
    """Manages risk for futures trading."""
    
    def __init__(
        self,
        max_leverage: float = 5.0,
        max_position_size_usd: float = 100000,
        max_drawdown_pct: float = 10.0,
        liquidation_buffer_pct: float = 5.0,
        funding_rate_threshold: float = 0.001,
    ):
        """Initialize risk manager.
        
        Args:
            max_leverage: Maximum allowed leverage
            max_position_size_usd: Maximum position size in USD
            max_drawdown_pct: Maximum allowed drawdown percentage
            liquidation_buffer_pct: Buffer to maintain from liquidation price
            funding_rate_threshold: Funding rate threshold for warnings
        """
        self.max_leverage = max_leverage
        self.max_position_size_usd = max_position_size_usd
        self.max_drawdown_pct = max_drawdown_pct
        self.liquidation_buffer_pct = liquidation_buffer_pct
        self.funding_rate_threshold = funding_rate_threshold
        
        logger.info(
            f"RiskManager initialized: max_leverage={max_leverage}, "
            f"max_position_size={max_position_size_usd}"
        )
    
    def calculate_liquidation_price(
        self,
        entry_price: float,
        leverage: float,
        position_type: str = "long",
        maintenance_margin_rate: float = 0.05,
    ) -> float:
        """Calculate liquidation price.
        
        Args:
            entry_price: Entry price
            leverage: Leverage used
            position_type: "long" or "short"
            maintenance_margin_rate: Maintenance margin rate (typically 5%)
            
        Returns:
            Liquidation price
        """
        if position_type == "long":
            # For long: liquidation_price = entry_price * (1 - 1/leverage + maintenance_margin_rate)
            liquidation_price = entry_price * (1 - 1 / leverage + maintenance_margin_rate)
        else:  # short
            # For short: liquidation_price = entry_price * (1 + 1/leverage - maintenance_margin_rate)
            liquidation_price = entry_price * (1 + 1 / leverage - maintenance_margin_rate)
        
        return liquidation_price
    
    def calculate_liquidation_distance(
        self,
        current_price: float,
        liquidation_price: float,
        position_type: str = "long",
    ) -> float:
        """Calculate distance to liquidation as percentage.
        
        Args:
            current_price: Current price
            liquidation_price: Liquidation price
            position_type: "long" or "short"
            
        Returns:
            Distance to liquidation as percentage
        """
        if position_type == "long":
            distance_pct = (current_price - liquidation_price) / current_price * 100
        else:  # short
            distance_pct = (liquidation_price - current_price) / current_price * 100
        
        return distance_pct
    
    def estimate_liquidation_probability(
        self,
        current_price: float,
        liquidation_price: float,
        volatility: float,
        time_horizon_hours: float = 24,
        position_type: str = "long",
    ) -> float:
        """Estimate probability of liquidation using normal distribution.
        
        Args:
            current_price: Current price
            liquidation_price: Liquidation price
            volatility: Annualized volatility
            time_horizon_hours: Time horizon in hours
            position_type: "long" or "short"
            
        Returns:
            Liquidation probability (0-1)
        """
        import numpy as np
        from scipy.stats import norm
        
        # Convert annualized volatility to hourly
        hourly_vol = volatility / np.sqrt(365 * 24)
        
        # Calculate z-score
        if position_type == "long":
            z_score = (liquidation_price - current_price) / (current_price * hourly_vol * np.sqrt(time_horizon_hours))
        else:  # short
            z_score = (current_price - liquidation_price) / (current_price * hourly_vol * np.sqrt(time_horizon_hours))
        
        # Probability is CDF of z-score
        prob = norm.cdf(z_score)
        return max(0, min(1, prob))
    
    def calculate_funding_cost(
        self,
        position_size_usd: float,
        funding_rate: float,
        hours: float = 1,
    ) -> float:
        """Calculate funding cost.
        
        Args:
            position_size_usd: Position size in USD
            funding_rate: Funding rate (per 8 hours typically)
            hours: Number of hours to calculate for
            
        Returns:
            Funding cost in USD
        """
        # Funding rate is typically per 8 hours
        periods = hours / 8
        cost = position_size_usd * funding_rate * periods
        return cost
    
    def calculate_risk_metrics(
        self,
        entry_price: float,
        current_price: float,
        position_size_usd: float,
        leverage: float,
        funding_rate: float,
        volatility: float,
        position_type: str = "long",
    ) -> RiskMetrics:
        """Calculate comprehensive risk metrics.
        
        Args:
            entry_price: Entry price
            current_price: Current price
            position_size_usd: Position size in USD
            leverage: Leverage used
            funding_rate: Current funding rate
            volatility: Current volatility
            position_type: "long" or "short"
            
        Returns:
            RiskMetrics object
        """
        # Liquidation price
        liq_price = self.calculate_liquidation_price(entry_price, leverage, position_type)
        
        # Distance to liquidation
        liq_distance_pct = self.calculate_liquidation_distance(current_price, liq_price, position_type)
        
        # Liquidation probability
        liq_prob = self.estimate_liquidation_probability(
            current_price, liq_price, volatility, 24, position_type
        )
        
        # Funding costs
        funding_hourly = self.calculate_funding_cost(position_size_usd, funding_rate, 1)
        funding_daily = self.calculate_funding_cost(position_size_usd, funding_rate, 24)
        
        # Max loss
        if position_type == "long":
            max_loss_usd = position_size_usd * (1 - liquidation_price / entry_price)
        else:
            max_loss_usd = position_size_usd * (liquidation_price / entry_price - 1)
        
        max_loss_pct = (max_loss_usd / position_size_usd) * 100
        
        return RiskMetrics(
            liquidation_price=liq_price,
            liquidation_distance_pct=liq_distance_pct,
            liquidation_probability=liq_prob,
            funding_cost_hourly=funding_hourly,
            funding_cost_daily=funding_daily,
            max_loss_usd=max_loss_usd,
            max_loss_pct=max_loss_pct,
        )
    
    def validate_position(
        self,
        position_size_usd: float,
        leverage: float,
        liquidation_probability: float,
        funding_rate: float,
    ) -> Dict[str, bool]:
        """Validate if a position meets risk criteria.
        
        Args:
            position_size_usd: Position size in USD
            leverage: Leverage
            liquidation_probability: Liquidation probability
            funding_rate: Funding rate
            
        Returns:
            Dictionary with validation results
        """
        checks = {
            "leverage_ok": leverage <= self.max_leverage,
            "position_size_ok": position_size_usd <= self.max_position_size_usd,
            "liquidation_prob_ok": liquidation_probability < 0.1,  # Less than 10%
            "funding_rate_ok": abs(funding_rate) <= self.funding_rate_threshold,
        }
        
        return checks

