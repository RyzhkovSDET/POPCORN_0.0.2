"""
Data processing module for cryptocurrency analysis.
Fetches and prepares market data for indicator calculations.
"""
import pandas as pd
from typing import Optional
from .api_requests import get_klines


def fetch_data_for_ticker(ticker: str, interval: str = "1m", limit: int = 100) -> pd.DataFrame:
    """
    Fetch and process klines data for a given ticker.
    
    Args:
        ticker: Trading pair (e.g., 'BTCUSDT')
        interval: Kline interval (e.g., '1m', '5m', '1h')
        limit: Number of klines to fetch
        
    Returns:
        DataFrame with OHLCV data or empty DataFrame if error
        
    Raises:
        ValueError: If data cannot be retrieved or processed
    """
    try:
        data = get_klines(ticker, interval=interval, limit=limit)
        
        if not data:
            raise ValueError("No data received from API")
        
        # Expected columns from Binance API
        columns = [
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "qav",
            "trades",
            "tbbav",
            "tbqav",
            "ignore"
        ]
        
        df = pd.DataFrame(data, columns=columns)
        
        # Convert numeric columns
        numeric_columns = ["open", "high", "low", "close", "volume"]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Check for NaN values after conversion
        if df[numeric_columns].isnull().any().any():
            raise ValueError("Invalid numeric data in response")
        
        # Convert timestamp to datetime
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        
        # Set time as index for better analysis
        df.set_index('time', inplace=True)
        
        return df
        
    except ValueError as e:
        raise ValueError(f"Data processing error for {ticker}: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error fetching data for {ticker}: {str(e)}")


def get_latest_price(ticker: str) -> Optional[float]:
    """
    Get the latest closing price for a ticker.
    
    Args:
        ticker: Trading pair
        
    Returns:
        Latest closing price or None if error
    """
    try:
        df = fetch_data_for_ticker(ticker, limit=1)
        if df.empty:
            return None
        return float(df['close'].iloc[-1])
    except:
        return None
