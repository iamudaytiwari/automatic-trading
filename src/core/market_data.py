"""Market data fetching and management module"""

import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class MarketData:
    """Fetch and manage market data from various exchanges"""

    def __init__(self, exchange_name: str = 'binance'):
        """Initialize market data connector
        
        Args:
            exchange_name: Name of the exchange (binance, kraken, coinbase, etc.)
        """
        self.exchange_name = exchange_name.lower()
        self.exchange = self._init_exchange()
        self.cache = {}

    def _init_exchange(self):
        """Initialize exchange API connection"""
        try:
            exchange_class = getattr(ccxt, self.exchange_name)
            return exchange_class()
        except AttributeError:
            raise ValueError(f"Exchange {self.exchange_name} not supported")

    def get_ohlcv(self, symbol: str, timeframe: str = '1h', 
                   limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV (candlestick) data
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Timeframe (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            limit: Number of candles to fetch
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            data = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(
                data,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            logger.error(f"Error fetching OHLCV data: {e}")
            raise

    def get_ticker(self, symbol: str) -> Dict:
        """Fetch current ticker data
        
        Args:
            symbol: Trading pair
            
        Returns:
            Ticker data dictionary
        """
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            logger.error(f"Error fetching ticker: {e}")
            raise

    def get_order_book(self, symbol: str, limit: int = 20) -> Dict:
        """Fetch order book data
        
        Args:
            symbol: Trading pair
            limit: Depth of order book
            
        Returns:
            Order book data
        """
        try:
            return self.exchange.fetch_order_book(symbol, limit=limit)
        except Exception as e:
            logger.error(f"Error fetching order book: {e}")
            raise

    def get_supported_symbols(self) -> List[str]:
        """Get list of supported trading pairs
        
        Returns:
            List of supported symbols
        """
        try:
            return self.exchange.symbols
        except Exception as e:
            logger.error(f"Error fetching symbols: {e}")
            raise
