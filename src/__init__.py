"""Automatic Trading System (ATA) - Main Package"""

__version__ = '0.1.0'
__author__ = 'Uday Tiwari'
__email__ = 'contact@iamudaytiwari.dev'

from src.core.market_data import MarketData
from src.core.strategy import Strategy
from src.core.portfolio import Portfolio

__all__ = [
    'MarketData',
    'Strategy',
    'Portfolio',
]
