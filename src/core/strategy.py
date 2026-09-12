"""Base strategy class for trading strategies"""

from abc import ABC, abstractmethod
import pandas as pd
import logging
from typing import Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class Strategy(ABC):
    """Abstract base class for trading strategies"""

    def __init__(self, symbol: str, timeframe: str = '1h'):
        """Initialize strategy
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Trading timeframe
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.position = None
        self.entry_price = None
        self.trades = []
        self.signals = []

    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> pd.DataFrame:
        """Analyze market data and generate signals
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with analysis results and signals
        """
        pass

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> Tuple[int, Optional[float]]:
        """Generate buy/sell signals
        
        Args:
            data: Market data
            
        Returns:
            Tuple of (signal: -1/0/1, price: Optional[float])
            -1: Sell, 0: Hold, 1: Buy
        """
        pass

    def should_buy(self, data: pd.DataFrame) -> bool:
        """Check if buy signal is generated
        
        Args:
            data: Market data
            
        Returns:
            True if buy signal, False otherwise
        """
        signal, _ = self.generate_signals(data)
        return signal == 1

    def should_sell(self, data: pd.DataFrame) -> bool:
        """Check if sell signal is generated
        
        Args:
            data: Market data
            
        Returns:
            True if sell signal, False otherwise
        """
        signal, _ = self.generate_signals(data)
        return signal == -1

    def record_trade(self, trade_type: str, price: float, 
                    quantity: float, timestamp: datetime):
        """Record executed trade
        
        Args:
            trade_type: 'BUY' or 'SELL'
            price: Execution price
            quantity: Trade quantity
            timestamp: Trade timestamp
        """
        trade = {
            'type': trade_type,
            'price': price,
            'quantity': quantity,
            'timestamp': timestamp,
            'pnl': None
        }
        self.trades.append(trade)
        logger.info(f"{trade_type} {quantity} {self.symbol} @ {price}")

    def get_performance_metrics(self) -> dict:
        """Calculate performance metrics
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.trades:
            return {}
        
        buy_trades = [t for t in self.trades if t['type'] == 'BUY']
        sell_trades = [t for t in self.trades if t['type'] == 'SELL']
        
        total_profit = 0
        winning_trades = 0
        losing_trades = 0
        
        if len(buy_trades) == len(sell_trades):
            for buy, sell in zip(buy_trades, sell_trades):
                profit = (sell['price'] - buy['price']) * buy['quantity']
                total_profit += profit
                if profit > 0:
                    winning_trades += 1
                else:
                    losing_trades += 1
        
        win_rate = (winning_trades / len(buy_trades)) if buy_trades else 0
        
        return {
            'total_trades': len(buy_trades),
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_profit': total_profit
        }
