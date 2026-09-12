"""Paper Trading Broker (for backtesting and simulation)"""

import logging
from typing import Optional, Dict
from datetime import datetime
from src.brokers.base_broker import BaseBroker

logger = logging.getLogger(__name__)


class PaperTrader(BaseBroker):
    """Paper trading broker for simulated trading"""

    def __init__(self, initial_balance: float = 10000, slippage: float = 0.001):
        """Initialize paper trader
        
        Args:
            initial_balance: Starting capital
            slippage: Slippage percentage for orders
        """
        super().__init__('PaperTrader')
        self.balance = initial_balance
        self.cash = initial_balance
        self.positions = {}
        self.slippage = slippage
        self.orders = []
        self.filled_orders = []
        self.trade_count = 0

    def connect(self) -> bool:
        """Connect (simulated)
        
        Returns:
            True
        """
        logger.info(f"Paper Trader Connected - Initial Balance: ${self.cash:.2f}")
        return True

    def disconnect(self) -> bool:
        """Disconnect (simulated)
        
        Returns:
            True
        """
        logger.info("Paper Trader Disconnected")
        return True

    def place_order(self, symbol: str, side: str, quantity: float,
                   price: Optional[float] = None) -> Dict:
        """Place simulated order
        
        Args:
            symbol: Trading pair
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Order price
            
        Returns:
            Order confirmation
        """
        if price is None:
            logger.error("Market orders not supported in paper trader")
            return {'status': 'error', 'message': 'Price required'}
        
        # Apply slippage
        if side.upper() == 'BUY':
            fill_price = price * (1 + self.slippage)
            cost = fill_price * quantity
            if cost > self.cash:
                logger.warning(f"Insufficient cash for {symbol} order")
                return {'status': 'error', 'message': 'Insufficient cash'}
            self.cash -= cost
            self._add_position(symbol, quantity, fill_price)
        else:  # SELL
            fill_price = price * (1 - self.slippage)
            if symbol not in self.positions:
                logger.warning(f"No position to sell for {symbol}")
                return {'status': 'error', 'message': 'No position'}
            if self.positions[symbol]['quantity'] < quantity:
                logger.warning(f"Insufficient quantity for {symbol}")
                quantity = self.positions[symbol]['quantity']
            self.cash += fill_price * quantity
            self._reduce_position(symbol, quantity)
        
        order = {
            'order_id': f"ORDER_{self.trade_count}",
            'symbol': symbol,
            'side': side.upper(),
            'quantity': quantity,
            'price': fill_price,
            'timestamp': datetime.now(),
            'status': 'FILLED'
        }
        self.trade_count += 1
        self.filled_orders.append(order)
        logger.info(f"{side.upper()} {quantity} {symbol} @ {fill_price:.8f}")
        return order

    def cancel_order(self, order_id: str) -> bool:
        """Cancel order (simulated)
        
        Args:
            order_id: Order ID
            
        Returns:
            True if successful
        """
        logger.info(f"Order {order_id} cancelled")
        return True

    def get_balance(self) -> Dict[str, float]:
        """Get account balance
        
        Returns:
            Balance dictionary
        """
        return {
            'cash': self.cash,
            'total': self.balance
        }

    def get_positions(self) -> Dict:
        """Get open positions
        
        Returns:
            Positions dictionary
        """
        return self.positions.copy()

    def _add_position(self, symbol: str, quantity: float, price: float):
        """Add or average position
        
        Args:
            symbol: Trading pair
            quantity: Quantity
            price: Price
        """
        if symbol in self.positions:
            old_qty = self.positions[symbol]['quantity']
            old_price = self.positions[symbol]['avg_price']
            new_qty = old_qty + quantity
            avg_price = (old_qty * old_price + quantity * price) / new_qty
            self.positions[symbol] = {'quantity': new_qty, 'avg_price': avg_price}
        else:
            self.positions[symbol] = {'quantity': quantity, 'avg_price': price}

    def _reduce_position(self, symbol: str, quantity: float):
        """Reduce position
        
        Args:
            symbol: Trading pair
            quantity: Quantity to reduce
        """
        if symbol in self.positions:
            new_qty = self.positions[symbol]['quantity'] - quantity
            if new_qty <= 0:
                del self.positions[symbol]
            else:
                self.positions[symbol]['quantity'] = new_qty

    def get_portfolio_value(self, prices: Dict[str, float]) -> float:
        """Calculate portfolio value
        
        Args:
            prices: Current prices {symbol: price}
            
        Returns:
            Total portfolio value
        """
        value = self.cash
        for symbol, position in self.positions.items():
            if symbol in prices:
                value += position['quantity'] * prices[symbol]
        return value
