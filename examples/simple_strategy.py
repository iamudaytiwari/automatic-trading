"""Example: Simple Moving Average Strategy"""

from src.strategies.moving_average import MAStrategy
from src.brokers.paper_trader import PaperTrader
from src.core.market_data import MarketData
import logging

logging.basicConfig(level=logging.INFO)


def main():
    """Run simple MA strategy example"""
    print("\n" + "="*50)
    print("MOVING AVERAGE STRATEGY EXAMPLE")
    print("="*50 + "\n")
    
    # Initialize components
    broker = PaperTrader(initial_balance=10000)
    broker.connect()
    
    strategy = MAStrategy(
        symbol='BTC/USDT',
        fast_period=10,
        slow_period=20
    )
    
    # Fetch market data
    print("Fetching market data...")
    market_data = MarketData('binance')
    data = market_data.get_ohlcv('BTC/USDT', timeframe='1h', limit=100)
    
    print(f"Loaded {len(data)} candles\n")
    
    # Run strategy
    for i in range(20, len(data)):
        current_data = data.iloc[:i+1]
        current_price = data.iloc[i]['close']
        
        signal, price = strategy.generate_signals(current_data)
        
        if signal == 1 and strategy.symbol not in broker.positions:
            quantity = (broker.cash * 0.2) / current_price
            broker.place_order(strategy.symbol, 'BUY', quantity, current_price)
        
        elif signal == -1 and strategy.symbol in broker.positions:
            quantity = broker.positions[strategy.symbol]['quantity']
            broker.place_order(strategy.symbol, 'SELL', quantity, current_price)
    
    # Print results
    print(f"\nFinal Cash: ${broker.cash:.2f}")
    print(f"Positions: {broker.positions}")
    print(f"Total Trades: {len(broker.filled_orders)}")
    
    broker.disconnect()


if __name__ == '__main__':
    main()
