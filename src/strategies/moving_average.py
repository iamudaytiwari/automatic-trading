"""Moving Average Crossover Strategy"""

import pandas as pd
from typing import Tuple, Optional
from src.core.strategy import Strategy
from src.indicators.technical import TechnicalIndicators


class MAStrategy(Strategy):
    """Moving Average Crossover Strategy
    
    Buys when fast MA crosses above slow MA
    Sells when fast MA crosses below slow MA
    """

    def __init__(self, symbol: str, fast_period: int = 10, 
                 slow_period: int = 20, timeframe: str = '1h'):
        """Initialize MA strategy
        
        Args:
            symbol: Trading pair
            fast_period: Fast MA period
            slow_period: Slow MA period
            timeframe: Timeframe
        """
        super().__init__(symbol, timeframe)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.last_signal = 0

    def analyze(self, data: pd.DataFrame) -> pd.DataFrame:
        """Analyze data and calculate MAs
        
        Args:
            data: OHLCV data
            
        Returns:
            Data with MA columns added
        """
        indicators = TechnicalIndicators(data)
        data['fast_ma'] = indicators.calculate_sma(self.fast_period)
        data['slow_ma'] = indicators.calculate_sma(self.slow_period)
        return data

    def generate_signals(self, data: pd.DataFrame) -> Tuple[int, Optional[float]]:
        """Generate buy/sell signals
        
        Args:
            data: Market data with indicators
            
        Returns:
            Tuple of (signal, price)
        """
        if len(data) < self.slow_period:
            return 0, None
        
        analyzed_data = self.analyze(data)
        current_fast = analyzed_data['fast_ma'].iloc[-1]
        current_slow = analyzed_data['slow_ma'].iloc[-1]
        prev_fast = analyzed_data['fast_ma'].iloc[-2]
        prev_slow = analyzed_data['slow_ma'].iloc[-2]
        current_price = data['close'].iloc[-1]
        
        # Buy signal: fast MA crosses above slow MA
        if prev_fast <= prev_slow and current_fast > current_slow:
            self.last_signal = 1
            return 1, current_price
        
        # Sell signal: fast MA crosses below slow MA
        elif prev_fast >= prev_slow and current_fast < current_slow:
            self.last_signal = -1
            return -1, current_price
        
        return 0, None
