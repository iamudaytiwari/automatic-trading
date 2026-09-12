"""RSI (Relative Strength Index) Strategy"""

import pandas as pd
from typing import Tuple, Optional
from src.core.strategy import Strategy
from src.indicators.technical import TechnicalIndicators


class RSIStrategy(Strategy):
    """RSI-Based Trading Strategy
    
    Buys when RSI < oversold level
    Sells when RSI > overbought level
    """

    def __init__(self, symbol: str, period: int = 14, 
                 oversold: int = 30, overbought: int = 70, timeframe: str = '1h'):
        """Initialize RSI strategy
        
        Args:
            symbol: Trading pair
            period: RSI period
            oversold: Oversold threshold
            overbought: Overbought threshold
            timeframe: Timeframe
        """
        super().__init__(symbol, timeframe)
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def analyze(self, data: pd.DataFrame) -> pd.DataFrame:
        """Analyze data and calculate RSI
        
        Args:
            data: OHLCV data
            
        Returns:
            Data with RSI column added
        """
        indicators = TechnicalIndicators(data)
        data['rsi'] = indicators.calculate_rsi(self.period)
        return data

    def generate_signals(self, data: pd.DataFrame) -> Tuple[int, Optional[float]]:
        """Generate buy/sell signals
        
        Args:
            data: Market data
            
        Returns:
            Tuple of (signal, price)
        """
        if len(data) < self.period:
            return 0, None
        
        analyzed_data = self.analyze(data)
        current_rsi = analyzed_data['rsi'].iloc[-1]
        current_price = data['close'].iloc[-1]
        
        # Buy signal: RSI crosses above oversold
        if current_rsi < self.oversold:
            return 1, current_price
        
        # Sell signal: RSI crosses above overbought
        elif current_rsi > self.overbought:
            return -1, current_price
        
        return 0, None
