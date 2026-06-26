# 🍿 POPCORN - Cryptocurrency Trading Analysis Tool

A real-time cryptocurrency market analysis dashboard powered by Streamlit, featuring technical indicators, watchlist management, and automated trading signals.

## Features

- 📊 **Real-time Market Data**: Fetch live candlestick data from Binance Vision API
- 📈 **Technical Indicators**: RSI (Relative Strength Index) and EMA (Exponential Moving Average)
- 🎯 **Trading Signals**: AI-powered buy/sell/hold recommendations
- 📋 **Watchlist Management**: Manage your cryptocurrency watchlist
- 💾 **Data Caching**: Efficient caching system to reduce API calls
- 🔄 **Auto Refresh**: Automatic data updates every 10 seconds

## Project Structure

```
POPCORN_0.0.2/
├── api/
│   ├── api_requests.py      # Binance API integration with retry logic
│   ├── get_data.py          # Data fetching and processing
│   └── init.py
├── storage/
│   ├── cache.py             # TTL-based caching module
│   └── coins_storage.py     # Watchlist persistence
├── main.py                  # Streamlit dashboard
├── coins.csv                # Watched cryptocurrencies list
└── README.md
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/RyzhkovSDET/POPCORN_0.0.2.git
cd POPCORN_0.0.2
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate      # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Required Dependencies

- `streamlit` - Web dashboard framework
- `pandas` - Data manipulation
- `requests` - HTTP requests
- `plotly` - Interactive charts
- `ta` - Technical Analysis library

## Usage

```bash
streamlit run main.py
```

The dashboard will open at `http://localhost:8501`

## How It Works

### Trading Signals

The system calculates a **Score (0-100)** based on:
- **RSI < 30**: +20 points (Oversold, buy signal)
- **RSI > 70**: -20 points (Overbought, sell signal)
- **Price > EMA(20)**: +15 points (Uptrend)
- **Price < EMA(20)**: -15 points (Downtrend)

**Signal Interpretation**:
- 🟢 **Score > 80**: Strong Buy
- 🟡 **Score 60-80**: Buy
- ⚪ **Score 40-60**: Hold
- 🟠 **Score 20-40**: Sell
- 🔴 **Score < 20**: Strong Sell

### RSI Zones

- 🟦 **OVS (< 30)**: Oversold
- 🟩 **WKN (30-40)**: Weak
- 🟨 **NEU (40-60)**: Neutral
- 🟧 **STR (60-70)**: Strong
- 🔴 **OVB (> 70)**: Overbought

## API Reference

### Storage Module

```python
from storage.coins_storage import load_coins, save_coins, add_coin, remove_coin

# Load watched coins
coins = load_coins()

# Add new coin
add_coin("ETHUSDT")

# Remove coin
remove_coin("ETHUSDT")

# Save coins
save_coins(coins)
```

### Cache Module

```python
from storage.cache import get_cache_manager

cache = get_cache_manager()

# Store value with 300s TTL
cache.set("key", value, ttl=300)

# Retrieve value (returns None if expired)
value = cache.get("key")

# Get cache info
info = cache.get_cache_info()
```

### API Requests

```python
from api.api_requests import get_klines

# Fetch klines with caching
data = get_klines("BTCUSDT", interval="1m", limit=100, use_cache=True)

# Fetch without cache
data = get_klines("BTCUSDT", use_cache=False)
```

### Data Processing

```python
from api.get_data import fetch_data_for_ticker, get_latest_price

# Get DataFrame with OHLCV data
df = fetch_data_for_ticker("BTCUSDT")

# Get latest price
price = get_latest_price("BTCUSDT")
```

## Configuration

Edit settings in `main.py`:

```python
REFRESH_SEC = 10  # Auto-refresh interval in seconds
```

## Performance Optimization

- **Caching**: API responses cached for 60 seconds by default
- **Retry Logic**: 3 retry attempts for failed requests
- **Request Timeout**: 10-second timeout per request
- **Lazy Loading**: Data fetched only for visible coins

## Troubleshooting

### API Request Timeout
- Check internet connection
- Verify Binance API is accessible
- Check `REQUEST_TIMEOUT` setting (api/api_requests.py)

### Invalid Ticker
- Ensure ticker format is correct (e.g., `BTCUSDT`)
- Verify coin is listed on Binance

### Data Display Issues
- Clear cache: `cache.clear()`
- Restart Streamlit: `Ctrl+C` then `streamlit run main.py`

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see LICENSE.md for details.

## Version

**Current Version**: 0.0.2

---

Made with ❤️ for cryptocurrency traders
