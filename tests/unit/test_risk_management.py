"""Unit tests for risk management modules."""

import pytest

from src.risk_management import PositionSizer, RiskManager


class TestRiskManager:
    """Test RiskManager class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.risk_manager = RiskManager(
            max_leverage=5.0,
            max_position_size_usd=100000,
            max_drawdown_pct=10.0,
            liquidation_buffer_pct=5.0,
            funding_rate_threshold=0.001,
        )
    
    def test_liquidation_price_long(self):
        """Test liquidation price calculation for long position."""
        entry_price = 45000
        leverage = 3.0
        
        liq_price = self.risk_manager.calculate_liquidation_price(
            entry_price, leverage, position_type="long"
        )
        
        # For long: liq_price = entry_price * (1 - 1/leverage + maintenance_margin)
        # With 5% maintenance margin: liq_price = 45000 * (1 - 1/3 + 0.05) = 45000 * 0.7833 = 35250
        assert liq_price < entry_price
        assert liq_price > 0
    
    def test_liquidation_price_short(self):
        """Test liquidation price calculation for short position."""
        entry_price = 45000
        leverage = 3.0
        
        liq_price = self.risk_manager.calculate_liquidation_price(
            entry_price, leverage, position_type="short"
        )
        
        # For short: liq_price = entry_price * (1 + 1/leverage - maintenance_margin)
        assert liq_price > entry_price
        assert liq_price > 0
    
    def test_liquidation_distance(self):
        """Test liquidation distance calculation."""
        current_price = 46000
        liquidation_price = 35000
        
        distance = self.risk_manager.calculate_liquidation_distance(
            current_price, liquidation_price, position_type="long"
        )
        
        # Distance should be positive for long position above liquidation
        assert distance > 0
        assert distance < 100
    
    def test_funding_cost(self):
        """Test funding cost calculation."""
        position_size = 50000
        funding_rate = 0.0001
        
        cost_1h = self.risk_manager.calculate_funding_cost(
            position_size, funding_rate, hours=1
        )
        cost_24h = self.risk_manager.calculate_funding_cost(
            position_size, funding_rate, hours=24
        )
        
        # 24-hour cost should be approximately 24x 1-hour cost
        assert cost_24h > cost_1h
        assert cost_1h > 0
    
    def test_risk_metrics(self):
        """Test comprehensive risk metrics calculation."""
        metrics = self.risk_manager.calculate_risk_metrics(
            entry_price=45000,
            current_price=46000,
            position_size_usd=50000,
            leverage=3.0,
            funding_rate=0.0001,
            volatility=0.25,
            position_type="long",
        )
        
        assert metrics.liquidation_price > 0
        assert metrics.liquidation_distance_pct > 0
        assert 0 <= metrics.liquidation_probability <= 1
        assert metrics.funding_cost_hourly >= 0
        assert metrics.funding_cost_daily >= 0
        assert metrics.max_loss_usd >= 0
    
    def test_validate_position(self):
        """Test position validation."""
        checks = self.risk_manager.validate_position(
            position_size_usd=50000,
            leverage=3.0,
            liquidation_probability=0.05,
            funding_rate=0.0001,
        )
        
        assert isinstance(checks, dict)
        assert "leverage_ok" in checks
        assert "position_size_ok" in checks
        assert "liquidation_prob_ok" in checks
        assert "funding_rate_ok" in checks
        
        # All checks should pass for reasonable parameters
        assert all(checks.values())


class TestPositionSizer:
    """Test PositionSizer class."""
    
    def test_kelly_criterion(self):
        """Test Kelly Criterion position sizing."""
        position_size = PositionSizer.kelly_criterion(
            win_rate=0.55,
            avg_win=1000,
            avg_loss=900,
            account_size=100000,
        )
        
        assert position_size > 0
        assert position_size <= 100000
    
    def test_fixed_fraction(self):
        """Test fixed fraction position sizing."""
        position_size = PositionSizer.fixed_fraction(
            account_size=100000,
            risk_fraction=0.02,
        )
        
        assert position_size == 2000
    
    def test_volatility_adjusted(self):
        """Test volatility-adjusted position sizing."""
        position_size = PositionSizer.volatility_adjusted(
            account_size=100000,
            current_volatility=0.25,
            target_volatility=0.20,
            base_fraction=0.02,
        )
        
        assert position_size > 0
        assert position_size <= 100000
    
    def test_risk_based(self):
        """Test risk-based position sizing."""
        position_size = PositionSizer.risk_based(
            account_size=100000,
            entry_price=45000,
            stop_loss_price=42750,  # 5% below entry
            risk_amount_usd=2000,
        )
        
        assert position_size > 0
        assert position_size <= 100000
    
    def test_leverage_adjusted(self):
        """Test leverage-adjusted position sizing."""
        position_size = PositionSizer.leverage_adjusted(
            account_size=100000,
            leverage=3.0,
            base_fraction=0.02,
        )
        
        assert position_size > 0
        assert position_size <= 100000
    
    def test_calculate_leverage(self):
        """Test leverage calculation."""
        leverage = PositionSizer.calculate_leverage_for_position(
            account_size=100000,
            position_size_usd=300000,
        )
        
        assert leverage == 3.0

