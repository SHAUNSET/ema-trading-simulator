import pandas as pd

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def backtest_ema(df, fast=9, slow=21, capital=10000, threshold=0.0, max_trades=50):
    """
    Stronger EMA strategy with threshold + trade analytics
    Returns: trades_df, equity_curve_df, df_with_indicators
    """
    df = df.copy()
    df["ema_fast"] = ema(df["close"], fast)
    df["ema_slow"] = ema(df["close"], slow)
    df["ema_diff"] = df["ema_fast"] - df["ema_slow"]

    trades = []
    cash = capital
    position = 0
    entry_price = 0
    max_trades_count = 0
    equity_curve = []

    for i, row in df.iterrows():
        if max_trades_count >= max_trades:
            equity_curve.append(cash + position * row["close"])
            continue

        # BUY signal: fast EMA above slow EMA + threshold, no position
        if position == 0 and row["ema_diff"] >= threshold:
            position = cash // row["close"]
            if position == 0:
                equity_curve.append(cash)
                continue
            entry_price = row["close"]
            entry_ema_diff = row["ema_diff"]
            cash -= position * row["close"]
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

        # SELL signal: fast EMA below slow EMA + threshold, or last position
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

        equity_curve.append(cash + position * row["close"])

    trades_df = pd.DataFrame(trades)
    equity_curve_df = pd.DataFrame({"date": df["date"], "equity": equity_curve})
    return trades_df, equity_curve_df, df
