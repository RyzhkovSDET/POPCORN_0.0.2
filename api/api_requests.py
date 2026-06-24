import requests

def get_klines(ticker, interval="1m", limit=100):
    url = "https://data-api.binance.vision/api/v3/klines"

    params = {
        "symbol": ticker,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    return response.json()