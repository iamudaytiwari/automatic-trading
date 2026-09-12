"""Portfolio management module"""

import pandas as pd
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class Portfolio:
    """Manage trading portfolio and positions"""

    def __init__(self, initial_balance: float):
        """Initialize portfolio
        
        Args:
            initial_balance: Starting capital
        """
        self.initial_balance = initial_balance
        self.cash = initial_balance
        self.positions = {}  # {symbol: {'quantity': float, 'avg_price': float}}
        self.trade_history = []
        self.performance_history = []

    def add_position(self, symbol: str, quantity: float, price: float):
        """Add or update position
        
        Args:
            symbol: Trading pair
            quantity: Quantity to add
            price: Entry price
        """
        if symbol in self.positions:
            old_qty = self.positions[symbol]['quantity']
            old_price = self.positions[symbol]['avg_price']
            new_qty = old_qty + quantity
            if new_qty != 0:
                avg_price = (old_qty * old_price + quantity * price) / new_qty
                self.positions[symbol] = {'quantity': new_qty, 'avg_price': avg_price}
            else:
                del self.positions[symbol]
        else:
            self.positions[symbol] = {'quantity': quantity, 'avg_price': price}

    def close_position(self, symbol: str, quantity: float, price: float) -> float:
        """Close position and return P&L
        
        Args:
            symbol: Trading pair
            quantity: Quantity to close
            price: Exit price
            
        Returns:
            Realized P&L
        """
        if symbol not in self.positions:
            logger.warning(f"No position for {symbol}")
            return 0
        
        position = self.positions[symbol]
        if position['quantity'] < quantity:
            logger.warning(f"Insufficient quantity for {symbol}")
            quantity = position['quantity']
        
        avg_price = position['avg_price']
        pnl = (price - avg_price) * quantity
        
        self.add_position(symbol, -quantity, price)
        self.cash += pnl
        
        return pnl

    def get_total_value(self, market_prices: Dict[str, float]) -> float:
        """Calculate total portfolio value
        
        Args:
            market_prices: Current market prices {symbol: price}
            
        Returns:
            Total portfolio value
        """
        total = self.cash
        for symbol, position in self.positions.items():
            if symbol in market_prices:
                total += position['quantity'] * market_prices[symbol]
        return total

    def get_returns(self, market_prices: Dict[str, float]) -> float:
        """Calculate portfolio returns
        
        Args:
            market_prices: Current market prices
            
        Returns:
            Total return percentage
        """
        total_value = self.get_total_value(market_prices)
        return ((total_value - self.initial_balance) / self.initial_balance) * 100

    def get_positions(self) -> Dict:
        """Get current positions
        
        Returns:
            Dictionary of positions
        """
        return self.positions.copy()

    def get_cash(self) -> float:
        """Get available cash
        
        Returns:
            Available cash amount
        """
        return self.cash
