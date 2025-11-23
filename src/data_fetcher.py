import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import yfinance as yf

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_hybrid(symbol: str, days: int = 252) -> pd.DataFrame:
    """
    Hybrid fetch: try live data first, fallback to synthetic if live fails.
    """
    symbol = symbol.upper()
    cache_path = f"{DATA_DIR}/{symbol}.csv"

    # --- Try cached CSV ---
    if os.path.exists(cache_path):
        try:
            df = pd.read_csv(cache_path)
            if not df.empty:
                return df
        except:
            pass

    # --- Try live fetch ---
    try:
        df = yf.download(symbol, period=f"{days}d", interval="1d")
        if not df.empty:
            df.reset_index(inplace=True)
            df.rename(columns={
                "Date":"date",
                "Open":"open",
                "High":"high",
                "Low":"low",
                "Close":"close",
                "Adj Close":"adj_close",
                "Volume":"volume"
            }, inplace=True)
            df.to_csv(cache_path, index=False)
            return df
    except:
        pass

    # --- Fallback to synthetic ---
    print(f"⚠️ Could not fetch live data for {symbol}. Using synthetic data.")

    np.random.seed(hash(symbol) % 2**32)
    start_price = np.random.uniform(200, 300)
    dates = [datetime.today() - timedelta(days=x) for x in range(days)]
    dates.sort()

    prices = [start_price]
    for _ in range(1, days):
        prices.append(prices[-1] * (1 + np.random.normal(0, 0.01)))

    df = pd.DataFrame({
        "date": dates,
        "open": prices,
        "high": [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
        "low": [p * (1 - np.random.uniform(0, 0.02)) for p in prices],
        "close": prices,
        "adj_close": prices,
        "volume": np.random.randint(100000, 1000000, size=days)
    })

    df.to_csv(cache_path, index=False)
    return df
