"""MACD (Moving Average Convergence Divergence) Strategy"""

import pandas as pd
from typing import Tuple, Optional
from src.core.strategy import Strategy
from src.indicators.technical import TechnicalIndicators


class MACDStrategy(Strategy):
    """MACD-Based Trading Strategy
    
    Buys when MACD line crosses above signal line
    Sells when MACD line crosses below signal line
    """

    def __init__(self, symbol: str, fast: int = 12, slow: int = 26,
                 signal: int = 9, timeframe: str = '1h'):
        """Initialize MACD strategy
        
        Args:
            symbol: Trading pair
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            timeframe: Timeframe
        """
        super().__init__(symbol, timeframe)
        self.fast = fast
        self.slow = slow
        self.signal_period = signal

    def analyze(self, data: pd.DataFrame) -> pd.DataFrame:
        """Analyze data and calculate MACD
        
        Args:
            data: OHLCV data
            
        Returns:
            Data with MACD columns added
        """
        indicators = TechnicalIndicators(data)
        macd, signal, histogram = indicators.calculate_macd(
            self.fast, self.slow, self.signal_period
        )
        data['macd'] = macd
        data['signal_line'] = signal
        data['histogram'] = histogram
        return data

    def generate_signals(self, data: pd.DataFrame) -> Tuple[int, Optional[float]]:
        """Generate buy/sell signals
        
        Args:
            data: Market data
            
        Returns:
            Tuple of (signal, price)
        """
        if len(data) < self.slow:
            return 0, None
        
        analyzed_data = self.analyze(data)
        current_macd = analyzed_data['macd'].iloc[-1]
        current_signal = analyzed_data['signal_line'].iloc[-1]
        prev_macd = analyzed_data['macd'].iloc[-2]
        prev_signal = analyzed_data['signal_line'].iloc[-2]
        current_price = data['close'].iloc[-1]
        
        # Buy signal: MACD crosses above signal line
        if prev_macd <= prev_signal and current_macd > current_signal:
            return 1, current_price
        
        # Sell signal: MACD crosses below signal line
        elif prev_macd >= prev_signal and current_macd < current_signal:
            return -1, current_price
        
        return 0, None
