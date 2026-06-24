import pandas as pd
from .api_requests import get_klines

def fetch_data_for_ticker(ticker):
    data = get_klines(ticker, interval="1m", limit=100)

    if not data:
        raise Exception("Не удалось получить данные")

    df = pd.DataFrame(
        data,
        columns=[
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
    )

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col])

    return df