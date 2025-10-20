"""Example: Risk Management."""

import sys

sys.path.insert(0, "/Users/phucbao/Documents/Binance")

from src.risk_management import PositionSizer, RiskManager
from src.utils import setup_logger

# Setup logging
setup_logger("risk_management", log_level="INFO")

def main():
    """Demonstrate risk management features."""
    
    print("="*60)
    print("RISK MANAGEMENT EXAMPLE")
    print("="*60)
    
    # Initialize risk manager
    risk_manager = RiskManager(
        max_leverage=5.0,
        max_position_size_usd=100000,
        max_drawdown_pct=10.0,
        liquidation_buffer_pct=5.0,
        funding_rate_threshold=0.001,
    )
    
    # Example position parameters
    entry_price = 45000
    current_price = 46000
    position_size_usd = 50000
    leverage = 3.0
    funding_rate = 0.0001
    volatility = 0.25  # 25% annualized
    
    print(f"\nPosition Parameters:")
    print(f"  Entry Price: ${entry_price:,.2f}")
    print(f"  Current Price: ${current_price:,.2f}")
    print(f"  Position Size: ${position_size_usd:,.2f}")
    print(f"  Leverage: {leverage}x")
    print(f"  Funding Rate: {funding_rate:.6f}")
    print(f"  Volatility: {volatility:.2%}")
    
    # Calculate liquidation price
    print(f"\n1. Liquidation Analysis:")
    liq_price = risk_manager.calculate_liquidation_price(
        entry_price, leverage, position_type="long"
    )
    print(f"  Liquidation Price: ${liq_price:,.2f}")
    
    liq_distance = risk_manager.calculate_liquidation_distance(
        current_price, liq_price, position_type="long"
    )
    print(f"  Distance to Liquidation: {liq_distance:.2f}%")
    
    liq_prob = risk_manager.estimate_liquidation_probability(
        current_price, liq_price, volatility, time_horizon_hours=24, position_type="long"
    )
    print(f"  Liquidation Probability (24h): {liq_prob:.2%}")
    
    # Calculate funding costs
    print(f"\n2. Funding Cost Analysis:")
    funding_hourly = risk_manager.calculate_funding_cost(
        position_size_usd, funding_rate, hours=1
    )
    funding_daily = risk_manager.calculate_funding_cost(
        position_size_usd, funding_rate, hours=24
    )
    funding_monthly = risk_manager.calculate_funding_cost(
        position_size_usd, funding_rate, hours=24*30
    )
    
    print(f"  Hourly Funding Cost: ${funding_hourly:,.2f}")
    print(f"  Daily Funding Cost: ${funding_daily:,.2f}")
    print(f"  Monthly Funding Cost: ${funding_monthly:,.2f}")
    
    # Calculate comprehensive risk metrics
    print(f"\n3. Comprehensive Risk Metrics:")
    metrics = risk_manager.calculate_risk_metrics(
        entry_price=entry_price,
        current_price=current_price,
        position_size_usd=position_size_usd,
        leverage=leverage,
        funding_rate=funding_rate,
        volatility=volatility,
        position_type="long",
    )
    
    print(f"  Liquidation Price: ${metrics.liquidation_price:,.2f}")
    print(f"  Distance to Liquidation: {metrics.liquidation_distance_pct:.2f}%")
    print(f"  Liquidation Probability: {metrics.liquidation_probability:.2%}")
    print(f"  Hourly Funding Cost: ${metrics.funding_cost_hourly:,.2f}")
    print(f"  Daily Funding Cost: ${metrics.funding_cost_daily:,.2f}")
    print(f"  Max Loss (USD): ${metrics.max_loss_usd:,.2f}")
    print(f"  Max Loss (%): {metrics.max_loss_pct:.2f}%")
    
    # Validate position
    print(f"\n4. Position Validation:")
    checks = risk_manager.validate_position(
        position_size_usd=position_size_usd,
        leverage=leverage,
        liquidation_probability=liq_prob,
        funding_rate=funding_rate,
    )
    
    for check, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {check}: {status}")
    
    # Position sizing examples
    print(f"\n5. Position Sizing Strategies:")
    account_size = 100000
    
    # Kelly Criterion
    kelly_size = PositionSizer.kelly_criterion(
        win_rate=0.55,
        avg_win=1000,
        avg_loss=900,
        account_size=account_size,
    )
    print(f"  Kelly Criterion: ${kelly_size:,.2f}")
    
    # Fixed Fraction
    fixed_size = PositionSizer.fixed_fraction(
        account_size=account_size,
        risk_fraction=0.02,
    )
    print(f"  Fixed Fraction (2%): ${fixed_size:,.2f}")
    
    # Volatility Adjusted
    vol_adjusted_size = PositionSizer.volatility_adjusted(
        account_size=account_size,
        current_volatility=volatility,
        target_volatility=0.20,
        base_fraction=0.02,
    )
    print(f"  Volatility Adjusted: ${vol_adjusted_size:,.2f}")
    
    # Risk Based
    risk_based_size = PositionSizer.risk_based(
        account_size=account_size,
        entry_price=entry_price,
        stop_loss_price=entry_price * 0.95,
        risk_amount_usd=2000,
    )
    print(f"  Risk Based (2% risk): ${risk_based_size:,.2f}")
    
    # Leverage Adjusted
    leverage_adj_size = PositionSizer.leverage_adjusted(
        account_size=account_size,
        leverage=leverage,
        base_fraction=0.02,
    )
    print(f"  Leverage Adjusted ({leverage}x): ${leverage_adj_size:,.2f}")
    
    # Calculate required leverage
    print(f"\n6. Leverage Calculation:")
    required_leverage = PositionSizer.calculate_leverage_for_position(
        account_size=account_size,
        position_size_usd=position_size_usd,
    )
    print(f"  Position Size: ${position_size_usd:,.2f}")
    print(f"  Account Size: ${account_size:,.2f}")
    print(f"  Required Leverage: {required_leverage:.2f}x")
    
    print("\n" + "="*60)
    print("Risk management example completed!")
    print("="*60)

if __name__ == "__main__":
    main()

