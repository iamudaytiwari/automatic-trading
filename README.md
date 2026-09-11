# Automatic Trading System (ATA)

A comprehensive algorithmic trading platform built with Python, featuring real-time market analysis, automated trade execution, and portfolio management.

## 🚀 Features

- **Real-time Market Data**: Fetch live price data from multiple exchanges
- **Technical Analysis**: Pre-built indicators (RSI, MACD, Bollinger Bands, Moving Averages)
- **Automated Trading Strategies**: Implement and backtest custom trading strategies
- **Risk Management**: Position sizing, stop-loss, take-profit management
- **Portfolio Tracking**: Monitor positions, P&L, and performance metrics
- **Backtesting Engine**: Test strategies against historical data
- **API Integration**: Connect with major exchanges (Binance, Kraken, Coinbase, etc.)
- **Alerts & Notifications**: Real-time trading alerts and webhooks
- **Dashboard**: Web-based monitoring and control panel

## 📋 Project Structure

```
automatic-trading/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── market_data.py          # Market data fetching
│   │   ├── strategy.py              # Base strategy class
│   │   └── portfolio.py             # Portfolio management
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── moving_average.py        # MA crossover strategy
│   │   ├── rsi_strategy.py          # RSI-based strategy
│   │   ├── macd_strategy.py         # MACD strategy
│   │   └── bollinger_bands.py       # Bollinger Bands strategy
│   ├── indicators/
│   │   ├── __init__.py
│   │   ├── technical.py             # Technical indicators
│   │   └── statistics.py            # Statistical functions
│   ├── backtesting/
│   │   ├── __init__.py
│   │   ├── backtest_engine.py       # Backtesting engine
│   │   └── performance_metrics.py   # Performance analysis
│   ├── brokers/
│   │   ├── __init__.py
│   │   ├── base_broker.py           # Base broker class
│   │   ├── binance_broker.py        # Binance integration
│   │   ├── kraken_broker.py         # Kraken integration
│   │   └── paper_trader.py          # Paper trading
│   ├── risk_management/
│   │   ├── __init__.py
│   │   ├── position_sizer.py        # Position sizing
│   │   └── risk_analyzer.py         # Risk analysis
│   └── utils/
│       ├── __init__.py
│       ├── config.py                # Configuration management
│       ├── logger.py                # Logging utilities
│       └── helpers.py               # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_indicators.py
│   ├── test_strategies.py
│   ├── test_backtesting.py
│   └── test_brokers.py
├── dashboard/
│   ├── app.py                       # Flask/Dash application
│   ├── templates/
│   └── static/
├── examples/
│   ├── simple_strategy.py
│   ├── backtest_example.py
│   └── live_trading.py
├── data/
│   ├── .gitkeep
│   └── historical/
├── config/
│   ├── trading_config.yaml
│   ├── strategies_config.yaml
│   └── .env.example
├── requirements.txt
├── setup.py
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip or conda
- Virtual environment (recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/iamudaytiwari/automatic-trading.git
cd automatic-trading

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp config/.env.example config/.env
# Edit config/.env with your API keys
```

## 📦 Dependencies

Key packages:
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `ccxt` - Cryptocurrency exchange APIs
- `ta-lib` - Technical analysis
- `scikit-learn` - ML capabilities
- `plotly` - Data visualization
- `flask` / `dash` - Web dashboard
- `pytest` - Testing framework
- `pyyaml` - Configuration management

## 🎯 Quick Start

### 1. Simple Moving Average Strategy

```python
from src.strategies.moving_average import MAStrategy
from src.brokers.paper_trader import PaperTrader

# Initialize broker (paper trading)
broker = PaperTrader(initial_balance=10000)

# Create strategy
strategy = MAStrategy(
    fast_period=10,
    slow_period=20,
    symbol='BTC/USD'
)

# Run trading
strategy.run(broker)
```

### 2. Backtest a Strategy

```python
from src.backtesting.backtest_engine import BacktestEngine
from src.strategies.rsi_strategy import RSIStrategy

engine = BacktestEngine(
    start_date='2022-01-01',
    end_date='2023-12-31',
    initial_capital=10000
)

strategy = RSIStrategy(symbol='ETH/USD')
results = engine.run(strategy)
print(results.performance_report())
```

### 3. Live Trading

```python
from src.brokers.binance_broker import BinanceBroker
from src.strategies.macd_strategy import MACDStrategy

broker = BinanceBroker(
    api_key='your_api_key',
    api_secret='your_api_secret'
)

strategy = MACDStrategy(symbol='BTC/USDT')
strategy.run(broker, live=True)
```

## ⚙️ Configuration

Edit `config/trading_config.yaml`:

```yaml
trading:
  initial_capital: 10000
  max_positions: 5
  risk_per_trade: 0.02  # 2% risk per trade

strategies:
  moving_average:
    enabled: true
    fast_period: 10
    slow_period: 20
  
  rsi:
    enabled: true
    period: 14
    oversold: 30
    overbought: 70

brokers:
  paper_trader:
    slippage: 0.001
  binance:
    sandbox: true
```

## 📊 Dashboard

Start the web dashboard:

```bash
python dashboard/app.py
# Visit http://localhost:5000
```

Features:
- Real-time position monitoring
- Strategy performance charts
- Trade history and P&L analysis
- Risk metrics dashboard
- Alert management

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/test_strategies.py

# Run with coverage
pytest --cov=src tests/
```

## 📈 Available Strategies

1. **Moving Average Crossover** - Buys on fast MA > slow MA, sells on opposite
2. **RSI Strategy** - Buys on oversold (RSI < 30), sells on overbought (RSI > 70)
3. **MACD Strategy** - Trades on MACD signal line crossovers
4. **Bollinger Bands** - Buys at lower band, sells at upper band
5. **Custom Strategies** - Extend `Strategy` base class

## 🔐 Risk Management

- **Position Sizing**: Kelly Criterion, Fixed Fractional
- **Stop Loss**: Fixed, Trailing, ATR-based
- **Take Profit**: Fixed, Breakeven, Scaling
- **Max Drawdown**: Portfolio-level limits
- **Correlation Risk**: Multi-asset risk analysis

## 🌐 Exchange Integrations

- Binance (Spot & Futures)
- Kraken
- Coinbase
- Bybit
- OKX
- Paper Trader (Backtesting & Simulation)

## 📝 API Reference

### Market Data
```python
from src.core.market_data import MarketData

data = MarketData('binance')
df = data.get_ohlcv('BTC/USDT', timeframe='1h', limit=100)
```

### Technical Indicators
```python
from src.indicators.technical import TechnicalIndicators

ind = TechnicalIndicators(df)
rsi = ind.calculate_rsi(period=14)
macd = ind.calculate_macd()
bollinger = ind.calculate_bollinger_bands()
```

### Strategy Base Class
```python
from src.core.strategy import Strategy

class MyStrategy(Strategy):
    def __init__(self, symbol):
        super().__init__(symbol)
    
    def analyze(self, data):
        # Your analysis logic
        pass
    
    def should_buy(self, data):
        # Buy signal logic
        pass
    
    def should_sell(self, data):
        # Sell signal logic
        pass
```

## 🚨 Important Notes

⚠️ **Disclaimer**: This is an educational project. Always:
- Start with paper trading
- Test thoroughly in backtesting
- Use proper risk management
- Never risk capital you can't afford to lose
- Keep API keys secure
- Monitor live trading actively

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📧 Support & Contact

- Issues: [GitHub Issues](https://github.com/iamudaytiwari/automatic-trading/issues)
- Discussions: [GitHub Discussions](https://github.com/iamudaytiwari/automatic-trading/discussions)

## 🔄 Roadmap

- [ ] Machine Learning strategy integration
- [ ] Advanced portfolio optimization
- [ ] Options trading support
- [ ] Multi-asset correlation analysis
- [ ] Real-time sentiment analysis
- [ ] Advanced order types (OCO, Iceberg)
- [ ] Performance analytics suite
- [ ] Cloud deployment guides

---

**Happy Trading! 📈**
