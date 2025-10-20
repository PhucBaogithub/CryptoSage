"""Position sizing strategies."""

from typing import Optional

from ..utils import get_logger

logger = get_logger(__name__)


class PositionSizer:
    """Calculates position sizes based on various strategies."""
    
    @staticmethod
    def kelly_criterion(
        win_rate: float,
        avg_win: float,
        avg_loss: float,
        account_size: float,
        max_fraction: float = 0.25,
    ) -> float:
        """Calculate position size using Kelly Criterion.
        
        Args:
            win_rate: Historical win rate (0-1)
            avg_win: Average win amount
            avg_loss: Average loss amount
            account_size: Total account size
            max_fraction: Maximum fraction of account to risk (safety limit)
            
        Returns:
            Position size in USD
        """
        if avg_loss == 0:
            return 0
        
        # Kelly formula: f = (bp - q) / b
        # where b = avg_win/avg_loss, p = win_rate, q = 1 - win_rate
        b = avg_win / avg_loss
        p = win_rate
        q = 1 - win_rate
        
        kelly_fraction = (b * p - q) / b
        
        # Apply safety limit
        kelly_fraction = min(kelly_fraction, max_fraction)
        kelly_fraction = max(kelly_fraction, 0)
        
        position_size = account_size * kelly_fraction
        
        logger.info(f"Kelly Criterion: fraction={kelly_fraction:.4f}, position_size={position_size:.2f}")
        return position_size
    
    @staticmethod
    def fixed_fraction(
        account_size: float,
        risk_fraction: float = 0.02,
    ) -> float:
        """Calculate position size using fixed fraction of account.
        
        Args:
            account_size: Total account size
            risk_fraction: Fraction of account to risk per trade (default 2%)
            
        Returns:
            Position size in USD
        """
        position_size = account_size * risk_fraction
        logger.info(f"Fixed Fraction: fraction={risk_fraction:.4f}, position_size={position_size:.2f}")
        return position_size
    
    @staticmethod
    def volatility_adjusted(
        account_size: float,
        current_volatility: float,
        target_volatility: float = 0.20,
        base_fraction: float = 0.02,
    ) -> float:
        """Calculate position size adjusted for volatility.
        
        Args:
            account_size: Total account size
            current_volatility: Current market volatility (annualized)
            target_volatility: Target volatility level
            base_fraction: Base fraction of account to risk
            
        Returns:
            Position size in USD
        """
        if current_volatility == 0:
            return 0
        
        # Adjust fraction inversely to volatility
        adjusted_fraction = base_fraction * (target_volatility / current_volatility)
        
        # Cap at reasonable limits
        adjusted_fraction = min(adjusted_fraction, 0.10)  # Max 10%
        adjusted_fraction = max(adjusted_fraction, 0.005)  # Min 0.5%
        
        position_size = account_size * adjusted_fraction
        
        logger.info(
            f"Volatility Adjusted: vol={current_volatility:.4f}, "
            f"fraction={adjusted_fraction:.4f}, position_size={position_size:.2f}"
        )
        return position_size
    
    @staticmethod
    def risk_based(
        account_size: float,
        entry_price: float,
        stop_loss_price: float,
        risk_amount_usd: float,
    ) -> float:
        """Calculate position size based on risk amount and stop loss.
        
        Args:
            account_size: Total account size
            entry_price: Entry price
            stop_loss_price: Stop loss price
            risk_amount_usd: Amount willing to risk in USD
            
        Returns:
            Position size in USD
        """
        if entry_price == stop_loss_price:
            return 0
        
        price_risk = abs(entry_price - stop_loss_price)
        position_size = risk_amount_usd / price_risk * entry_price
        
        # Cap at max fraction of account
        max_position = account_size * 0.10
        position_size = min(position_size, max_position)
        
        logger.info(
            f"Risk Based: risk_amount={risk_amount_usd:.2f}, "
            f"price_risk={price_risk:.2f}, position_size={position_size:.2f}"
        )
        return position_size
    
    @staticmethod
    def leverage_adjusted(
        account_size: float,
        leverage: float,
        base_fraction: float = 0.02,
        max_leverage: float = 5.0,
    ) -> float:
        """Calculate position size adjusted for leverage.
        
        Args:
            account_size: Total account size
            leverage: Leverage to use
            base_fraction: Base fraction of account
            max_leverage: Maximum allowed leverage
            
        Returns:
            Position size in USD
        """
        # Reduce position size as leverage increases
        leverage = min(leverage, max_leverage)
        adjusted_fraction = base_fraction / leverage
        
        position_size = account_size * adjusted_fraction
        
        logger.info(
            f"Leverage Adjusted: leverage={leverage:.2f}, "
            f"fraction={adjusted_fraction:.4f}, position_size={position_size:.2f}"
        )
        return position_size
    
    @staticmethod
    def calculate_leverage_for_position(
        account_size: float,
        position_size_usd: float,
    ) -> float:
        """Calculate leverage needed for a position size.
        
        Args:
            account_size: Total account size
            position_size_usd: Desired position size
            
        Returns:
            Required leverage
        """
        if account_size == 0:
            return 0
        
        leverage = position_size_usd / account_size
        return leverage

