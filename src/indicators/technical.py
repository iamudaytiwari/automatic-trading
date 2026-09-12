"""Technical analysis indicators"""

import pandas as pd
import numpy as np
from typing import Optional


class TechnicalIndicators:
    """Calculate technical analysis indicators"""

    def __init__(self, data: pd.DataFrame):
        """Initialize with OHLCV data
        
        Args:
            data: DataFrame with OHLCV columns
        """
        self.data = data.copy()

    def calculate_sma(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Simple Moving Average
        
        Args:
            period: Period for SMA
            column: Column to calculate on
            
        Returns:
            SMA values
        """
        return self.data[column].rolling(window=period).mean()

    def calculate_ema(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Exponential Moving Average
        
        Args:
            period: Period for EMA
            column: Column to calculate on
            
        Returns:
            EMA values
        """
        return self.data[column].ewm(span=period, adjust=False).mean()

    def calculate_rsi(self, period: int = 14, column: str = 'close') -> pd.Series:
        """Relative Strength Index
        
        Args:
            period: RSI period
            column: Column to calculate on
            
        Returns:
            RSI values (0-100)
        """
        delta = self.data[column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_macd(self, fast: int = 12, slow: int = 26, 
                       signal: int = 9, column: str = 'close'):
        """MACD (Moving Average Convergence Divergence)
        
        Args:
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            column: Column to calculate on
            
        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        ema_fast = self.data[column].ewm(span=fast, adjust=False).mean()
        ema_slow = self.data[column].ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    def calculate_bollinger_bands(self, period: int = 20, 
                                 std_dev: int = 2, column: str = 'close'):
        """Bollinger Bands
        
        Args:
            period: Period for moving average
            std_dev: Number of standard deviations
            column: Column to calculate on
            
        Returns:
            Tuple of (Upper band, Middle band, Lower band)
        """
        sma = self.data[column].rolling(window=period).mean()
        std = self.data[column].rolling(window=period).std()
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        return upper_band, sma, lower_band

    def calculate_atr(self, period: int = 14) -> pd.Series:
        """Average True Range
        
        Args:
            period: ATR period
            
        Returns:
            ATR values
        """
        high_low = self.data['high'] - self.data['low']
        high_close = np.abs(self.data['high'] - self.data['close'].shift())
        low_close = np.abs(self.data['low'] - self.data['close'].shift())
        
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr

    def calculate_stochastic(self, period: int = 14, smooth_k: int = 3,
                            smooth_d: int = 3):
        """Stochastic Oscillator
        
        Args:
            period: Lookback period
            smooth_k: K smoothing period
            smooth_d: D smoothing period
            
        Returns:
            Tuple of (K line, D line)
        """
        low_min = self.data['low'].rolling(window=period).min()
        high_max = self.data['high'].rolling(window=period).max()
        k_percent = 100 * ((self.data['close'] - low_min) / (high_max - low_min))
        k_line = k_percent.rolling(window=smooth_k).mean()
        d_line = k_line.rolling(window=smooth_d).mean()
        return k_line, d_line
