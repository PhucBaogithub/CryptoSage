"""Order execution for Binance Futures."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from ..utils import get_logger

logger = get_logger(__name__)


class OrderType(Enum):
    """Order types."""
    LIMIT = "LIMIT"
    MARKET = "MARKET"


class OrderSide(Enum):
    """Order sides."""
    BUY = "BUY"
    SELL = "SELL"


class PositionSide(Enum):
    """Position sides."""
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass
class Order:
    """Order object."""
    
    symbol: str
    side: OrderSide
    position_side: PositionSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    take_profit_price: Optional[float] = None
    leverage: int = 1
    timestamp: Optional[datetime] = None
    order_id: Optional[str] = None
    status: str = "PENDING"
    
    def __post_init__(self):
        """Initialize order."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class OrderExecutor:
    """Executes orders on Binance Futures."""
    
    def __init__(
        self,
        client,
        mode: str = "paper",
        max_retries: int = 3,
        retry_delay_seconds: float = 1.0,
    ):
        """Initialize order executor.
        
        Args:
            client: Binance client
            mode: Execution mode ("paper", "testnet", or "live")
            max_retries: Maximum number of retries
            retry_delay_seconds: Delay between retries
        """
        self.client = client
        self.mode = mode
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds
        self.orders: Dict[str, Order] = {}
        
        logger.info(f"OrderExecutor initialized: mode={mode}")
    
    def place_order(self, order: Order) -> Optional[Dict]:
        """Place an order.
        
        Args:
            order: Order object
            
        Returns:
            Order response or None if failed
        """
        if self.mode == "paper":
            return self._place_paper_order(order)
        elif self.mode == "testnet":
            return self._place_testnet_order(order)
        elif self.mode == "live":
            return self._place_live_order(order)
        else:
            logger.error(f"Unknown execution mode: {self.mode}")
            return None
    
    def _place_paper_order(self, order: Order) -> Dict:
        """Place a paper order (simulated).
        
        Args:
            order: Order object
            
        Returns:
            Simulated order response
        """
        order.order_id = f"PAPER_{len(self.orders)}"
        order.status = "FILLED"
        self.orders[order.order_id] = order
        
        logger.info(
            f"Paper order placed: {order.symbol} {order.side.value} "
            f"{order.quantity} @ {order.price}"
        )
        
        return {
            "orderId": order.order_id,
            "symbol": order.symbol,
            "status": "FILLED",
            "side": order.side.value,
            "positionSide": order.position_side.value,
            "quantity": order.quantity,
            "price": order.price,
        }
    
    def _place_testnet_order(self, order: Order) -> Optional[Dict]:
        """Place an order on testnet.
        
        Args:
            order: Order object
            
        Returns:
            Order response or None if failed
        """
        try:
            if order.order_type == OrderType.LIMIT:
                response = self.client.futures_create_order(
                    symbol=order.symbol,
                    side=order.side.value,
                    positionSide=order.position_side.value,
                    type="LIMIT",
                    timeInForce="GTC",
                    quantity=order.quantity,
                    price=order.price,
                )
            else:  # MARKET
                response = self.client.futures_create_order(
                    symbol=order.symbol,
                    side=order.side.value,
                    positionSide=order.position_side.value,
                    type="MARKET",
                    quantity=order.quantity,
                )
            
            order.order_id = response["orderId"]
            order.status = response["status"]
            self.orders[order.order_id] = order
            
            logger.info(f"Testnet order placed: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to place testnet order: {e}")
            return None
    
    def _place_live_order(self, order: Order) -> Optional[Dict]:
        """Place a live order.
        
        Args:
            order: Order object
            
        Returns:
            Order response or None if failed
        """
        logger.warning("LIVE TRADING MODE - Placing real order!")
        
        try:
            if order.order_type == OrderType.LIMIT:
                response = self.client.futures_create_order(
                    symbol=order.symbol,
                    side=order.side.value,
                    positionSide=order.position_side.value,
                    type="LIMIT",
                    timeInForce="GTC",
                    quantity=order.quantity,
                    price=order.price,
                )
            else:  # MARKET
                response = self.client.futures_create_order(
                    symbol=order.symbol,
                    side=order.side.value,
                    positionSide=order.position_side.value,
                    type="MARKET",
                    quantity=order.quantity,
                )
            
            order.order_id = response["orderId"]
            order.status = response["status"]
            self.orders[order.order_id] = order
            
            logger.info(f"Live order placed: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to place live order: {e}")
            return None
    
    def cancel_order(self, symbol: str, order_id: str) -> Optional[Dict]:
        """Cancel an order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID
            
        Returns:
            Cancel response or None if failed
        """
        if self.mode == "paper":
            if order_id in self.orders:
                self.orders[order_id].status = "CANCELED"
                logger.info(f"Paper order canceled: {order_id}")
                return {"orderId": order_id, "status": "CANCELED"}
            return None
        
        try:
            response = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            logger.info(f"Order canceled: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to cancel order: {e}")
            return None
    
    def get_order_status(self, symbol: str, order_id: str) -> Optional[Dict]:
        """Get order status.
        
        Args:
            symbol: Trading pair
            order_id: Order ID
            
        Returns:
            Order status or None if failed
        """
        if self.mode == "paper":
            if order_id in self.orders:
                return {"orderId": order_id, "status": self.orders[order_id].status}
            return None
        
        try:
            response = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            return response
        except Exception as e:
            logger.error(f"Failed to get order status: {e}")
            return None

