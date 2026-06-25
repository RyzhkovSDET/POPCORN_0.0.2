import requests

BASE_URL = "https://data-api.binance.vision/api/v3/klines"
DEFAULT_TIMEOUT = 10  # seconds

def get_klines(ticker, interval="1m", limit=100, timeout=DEFAULT_TIMEOUT):
    """
    Запрашивает свечи (klines) с Binance public mirror.
    Возвращает список свечей или выбрасывает RuntimeError с описанием ошибки.
    """
    params = {"symbol": ticker, "interval": interval, "limit": limit}
    headers = {"User-Agent": "POPCORN/1.0"}

    try:
        resp = requests.get(BASE_URL, params=params, headers=headers, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise ValueError("Unexpected response format from klines API")
        return data
    except requests.RequestException as e:
        # Оборачиваем в понятное исключение
        raise RuntimeError(f"Ошибка при запросе klines для {ticker}: {e}") from e
    except ValueError as e:
        raise RuntimeError(f"Неправильный формат ответа для {ticker}: {e}") from e
