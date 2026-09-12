"""Base Broker class"""

from abc import ABC, abstractmethod
from typing import Optional, Dict


class BaseBroker(ABC):
    """Abstract base class for brokers"""

    def __init__(self, name: str):
        """Initialize broker
        
        Args:
            name: Broker name
        """
        self.name = name
        self.balance = 0
        self.positions = {}
        self.orders = []

    @abstractmethod
    def connect(self) -> bool:
        """Connect to broker"""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from broker"""
        pass

    @abstractmethod
    def place_order(self, symbol: str, side: str, quantity: float, 
                   price: Optional[float] = None) -> Dict:
        """Place order
        
        Args:
            symbol: Trading pair
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Order price (None for market order)
            
        Returns:
            Order confirmation
        """
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel order
        
        Args:
            order_id: Order ID
            
        Returns:
            True if successful
        """
        pass

    @abstractmethod
    def get_balance(self) -> Dict[str, float]:
        """Get account balance
        
        Returns:
            Balance dictionary
        """
        pass

    @abstractmethod
    def get_positions(self) -> Dict:
        """Get open positions
        
        Returns:
            Positions dictionary
        """
        pass
