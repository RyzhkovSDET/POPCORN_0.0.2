"""
API requests module for Binance Vision API.
Handles klines data fetching with caching and error handling.
"""
import requests
from typing import Dict, List, Any
from storage.cache import get_cache_manager


BINANCE_API_URL = "https://data-api.binance.vision/api/v3/klines"
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
CACHE_TTL = 60  # seconds


def get_klines(
    ticker: str,
    interval: str = "1m",
    limit: int = 100,
    use_cache: bool = True
) -> List[List[Any]]:
    """
    Fetch klines (candlestick) data from Binance Vision API.
    
    Args:
        ticker: Trading pair (e.g., 'BTCUSDT')
        interval: Kline interval (e.g., '1m', '5m', '1h')
        limit: Number of klines to fetch (max 1000)
        use_cache: Use cache if available
        
    Returns:
        List of kline data or empty list if error
        
    Raises:
        ValueError: If parameters are invalid
    """
    if not ticker:
        raise ValueError("Ticker cannot be empty")
    
    if limit > 1000:
        raise ValueError("Limit cannot exceed 1000")
    
    # Check cache first
    cache_key = f"{ticker}_{interval}_{limit}"
    if use_cache:
        cache_manager = get_cache_manager()
        cached_data = cache_manager.get(cache_key)
        if cached_data is not None:
            return cached_data
    
    params = {
        "symbol": ticker.upper(),
        "interval": interval,
        "limit": limit
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (POPCORN/0.0.2)"
    }
    
    # Retry logic
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                BINANCE_API_URL,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Cache successful response
            if use_cache:
                cache_manager = get_cache_manager()
                cache_manager.set(cache_key, data, ttl=CACHE_TTL)
            
            return data
            
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES - 1:
                continue
            raise Exception(f"Request timeout after {MAX_RETRIES} attempts")
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise ValueError(f"Invalid ticker or interval: {ticker} {interval}")
            if attempt < MAX_RETRIES - 1:
                continue
            raise Exception(f"HTTP Error {e.response.status_code}")
        
        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                continue
            raise Exception(f"Request failed: {str(e)}")
    
    return []
