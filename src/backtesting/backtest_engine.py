"""Backtesting engine for strategy evaluation"""

import pandas as pd
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from src.core.strategy import Strategy
from src.brokers.paper_trader import PaperTrader

logger = logging.getLogger(__name__)


class BacktestEngine:
    """Engine for backtesting trading strategies"""

    def __init__(self, initial_capital: float = 10000, 
                 commission: float = 0.001, slippage: float = 0.001):
        """Initialize backtest engine
        
        Args:
            initial_capital: Starting capital
            commission: Commission per trade
            slippage: Slippage percentage
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.broker = None
        self.results = None

    def run(self, strategy: Strategy, data: pd.DataFrame, 
            verbose: bool = True) -> Dict:
        """Run backtest
        
        Args:
            strategy: Strategy to test
            data: Historical OHLCV data
            verbose: Print progress
            
        Returns:
            Backtest results
        """
        self.broker = PaperTrader(self.initial_capital, self.slippage)
        self.broker.connect()
        
        trades = []
        equity_curve = []
        
        # Walk through historical data
        for i in range(len(data) - 1):
            current_data = data.iloc[:i+1]
            current_price = data.iloc[i]['close']
            
            # Generate trading signal
            signal, _ = strategy.generate_signals(current_data)
            
            # Execute trades
            if signal == 1 and strategy.symbol not in self.broker.positions:
                # Calculate position size (fixed for simplicity)
                quantity = (self.broker.cash * 0.1) / current_price
                self.broker.place_order(strategy.symbol, 'BUY', quantity, current_price)
            
            elif signal == -1 and strategy.symbol in self.broker.positions:
                quantity = self.broker.positions[strategy.symbol]['quantity']
                self.broker.place_order(strategy.symbol, 'SELL', quantity, current_price)
            
            # Record equity
            prices = {strategy.symbol: current_price}
            equity = self.broker.get_portfolio_value(prices)
            equity_curve.append({
                'timestamp': data.index[i],
                'equity': equity,
                'cash': self.broker.cash,
                'price': current_price
            })
        
        # Calculate performance metrics
        results = self._calculate_metrics(equity_curve, self.broker.filled_orders)
        self.results = results
        
        if verbose:
            self._print_results(results)
        
        self.broker.disconnect()
        return results

    def _calculate_metrics(self, equity_curve: List[Dict], 
                          trades: List[Dict]) -> Dict:
        """Calculate performance metrics
        
        Args:
            equity_curve: Equity values over time
            trades: List of trades executed
            
        Returns:
            Performance metrics
        """
        equity_df = pd.DataFrame(equity_curve)
        
        total_return = ((equity_df['equity'].iloc[-1] - self.initial_capital) / 
                       self.initial_capital) * 100
        
        max_equity = equity_df['equity'].max()
        min_equity = equity_df['equity'].min()
        max_drawdown = ((min_equity - max_equity) / max_equity) * 100
        
        num_trades = len(trades)
        winning_trades = 0
        losing_trades = 0
        total_profit = 0
        
        for trade in trades:
            if trade['side'] == 'SELL':
                # Simple P&L calculation
                winning_trades += 1
        
        return {
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'num_trades': num_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'final_equity': equity_df['equity'].iloc[-1],
            'equity_curve': equity_df
        }

    def _print_results(self, results: Dict):
        """Print backtest results
        
        Args:
            results: Results dictionary
        """
        print("\n" + "="*50)
        print("BACKTEST RESULTS")
        print("="*50)
        print(f"Total Return: {results['total_return']:.2f}%")
        print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
        print(f"Total Trades: {results['num_trades']}")
        print(f"Final Equity: ${results['final_equity']:.2f}")
        print("="*50 + "\n")
