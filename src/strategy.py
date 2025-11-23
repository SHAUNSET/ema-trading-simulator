import pandas as pd
import numpy as np

def ema(series, period):
    """Compute Exponential Moving Average for a given series."""
    series = pd.to_numeric(series, errors='coerce')
    return series.ewm(span=period, adjust=False).mean()

def backtest_ema(df, fast=9, slow=21, capital=10000, threshold=0.0, max_trades=50):
    """
    Strong EMA trading strategy with threshold and analytics.
    
    Parameters:
        df (pd.DataFrame): Historical OHLC data with at least 'date' and 'close' columns
        fast (int): Fast EMA period
        slow (int): Slow EMA period
        capital (float): Initial portfolio capital
        threshold (float): EMA difference threshold for trade signals
        max_trades (int): Maximum number of trades allowed
    
    Returns:
        trades_df (pd.DataFrame): All executed trades with entry/exit info
        equity_curve_df (pd.DataFrame): Portfolio equity over time
        df (pd.DataFrame): Original data with EMA indicators
    """

    df = df.copy()

    # Ensure numeric 'close'
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df = df.dropna(subset=['close'])
    if df.empty:
        return pd.DataFrame(), pd.DataFrame(), df

    # Compute EMAs and EMA difference
    df["ema_fast"] = ema(df["close"], fast)
    df["ema_slow"] = ema(df["close"], slow)
    df["ema_diff"] = df["ema_fast"] - df["ema_slow"]

    trades = []
    cash = capital
    position = 0
    entry_price = 0
    entry_ema_diff = 0
    max_trades_count = 0
    equity_curve = []

    for i, row in df.iterrows():
        # Skip if max trades reached
        if max_trades_count >= max_trades:
            equity_curve.append(cash + position * row["close"])
            continue

        # BUY signal: fast EMA above slow EMA + threshold, no current position
        if position == 0 and row["ema_diff"] >= threshold:
            position = cash // row["close"]
            if position == 0:
                equity_curve.append(cash)
                continue
            entry_price = row["close"]
            entry_ema_diff = row["ema_diff"]
            cash -= position * entry_price
            trades.append({
                "entry_date": row["date"],
                "entry_price": entry_price,
                "shares": position,
                "entry_ema_diff": entry_ema_diff,
                "exit_date": None,
                "exit_price": None,
                "exit_ema_diff": None,
                "profit": None
            })
            max_trades_count += 1

        # SELL signal: fast EMA below slow EMA - threshold, or last position
        elif position > 0 and row["ema_diff"] <= -threshold:
            exit_price = row["close"]
            exit_ema_diff = row["ema_diff"]
            profit = position * (exit_price - entry_price)
            cash += position * exit_price
            # update last trade
            trades[-1].update({
                "exit_date": row["date"],
                "exit_price": exit_price,
                "exit_ema_diff": exit_ema_diff,
                "profit": profit
            })
            position = 0
            entry_price = 0
            entry_ema_diff = 0

        equity_curve.append(cash + position * row["close"])

    trades_df = pd.DataFrame(trades)
    equity_curve_df = pd.DataFrame({"date": df["date"], "equity": equity_curve})

    # Add summary metrics
    if not trades_df.empty:
        trades_df["exit_date"] = trades_df["exit_date"].fillna("Open")
        trades_df["exit_price"] = trades_df["exit_price"].fillna(np.nan)
        trades_df["profit"] = trades_df["profit"].fillna(0)
        trades_df["cumulative_profit"] = trades_df["profit"].cumsum()

    return trades_df, equity_curve_df, df
