import streamlit as st
import os
from src.data_fetcher import fetch_hybrid as fetch_historical
from src.strategy import backtest_ema
from src.portfolio import Portfolio
from src.utils import plot_ema_chart, plot_equity_curve
from datetime import datetime
import pandas as pd
import numpy as np
from datetime import timedelta

# ------------------ Synthetic Data Generator ------------------
def generate_synthetic(symbol: str, days: int = 252) -> pd.DataFrame:
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
    return df

# ------------------ Streamlit App ------------------
def main():
    st.set_page_config(page_title="EMA Simulator", layout="wide")
    st.title("📈 EMA Trading Simulator")

    # ------------------ Strategy Explanation ------------------
    with st.expander("📖 Strategy Explanation"):
        st.markdown("""
### Understanding EMA (Exponential Moving Average)
EMA gives **more weight to recent prices**, so it reacts faster than a simple moving average.

- **Fast EMA**: Captures short-term trends.
- **Slow EMA**: Captures long-term trends.
- **EMA Difference Threshold**: Minimum difference between fast and slow EMA to trigger trades.

### How the Strategy Works
1. **Buy Signal**: Fast EMA > Slow EMA + Threshold → momentum upward → buy.
2. **Sell Signal**: Fast EMA < Slow EMA - Threshold → momentum downward → sell.

### Making Profit
- Buy low, sell high based on EMA crossovers.
- Portfolio updates after every trade.
- Adjust EMA periods and thresholds to optimize.

### Visual Guides
- **EMA Crossover Chart**: Fast vs Slow EMA, buy/sell points highlighted.
- **Equity Curve**: Portfolio value over time.
        """)

    # ------------------ Backtest Settings ------------------
    st.sidebar.header("Backtest Settings")
    stocks = st.sidebar.multiselect("Select Stocks", ["AAPL", "MSFT", "TSLA"], default=["AAPL"])
    fast = st.sidebar.slider("Fast EMA", 1, 50, 9)
    slow = st.sidebar.slider("Slow EMA", 5, 200, 21)
    threshold = st.sidebar.number_input("EMA Difference Threshold", 0.0, 500.0, 0.5)
    capital = st.sidebar.number_input("Initial Capital", 1000, 2000000, 10000)
    max_trades = st.sidebar.number_input("Max Trades", 1, 500, 50)
    run_btn = st.sidebar.button("Run Backtest")

    # ------------------ Run Backtest ------------------
    if run_btn:
        for stock in stocks:
            st.subheader(f"📌 {stock}")
            df = fetch_historical(stock)

            # ------------------ Sanitize DataFrame ------------------
            if df.empty:
                st.warning(f"⚠️ Could not fetch data for {stock}, generating synthetic data.")
                df = generate_synthetic(stock)

            if 'close' not in df.columns or df['close'].dropna().empty:
                st.warning(f"⚠️ 'close' column missing or empty for {stock}, generating synthetic data.")
                df = generate_synthetic(stock)

            df['close'] = pd.to_numeric(df['close'], errors='coerce')
            df = df.dropna(subset=['close'])

            # Show last update timestamp
            cache_path = f"data/{stock}.csv"
            if os.path.exists(cache_path):
                ts = datetime.fromtimestamp(os.path.getmtime(cache_path)).strftime("%Y-%m-%d %H:%M:%S")
                st.caption(f"🗂️ Data last updated: **{ts}**")
            else:
                st.caption("🗂️ No cache timestamp available.")

            # ------------------ Run EMA Strategy ------------------
            trades, equity_curve, df_ind = backtest_ema(df, fast, slow, capital, threshold, max_trades)
            portfolio = Portfolio(capital)
            portfolio.update(trades)

            # ------------------ Portfolio Summary ------------------
            st.markdown("### 💼 Portfolio Summary")
            st.markdown(portfolio.summary())

            # Additional metrics
            if not trades.empty:
                profitable_trades = trades[trades['profit'] > 0]
                avg_profit = profitable_trades['profit'].mean() if not profitable_trades.empty else 0
                st.markdown(f"**Total Trades:** {len(trades)} | **Profitable Trades:** {len(profitable_trades)} | **Avg Profit per Winning Trade:** {avg_profit:.2f}")

            # ------------------ Trades Table ------------------
            if not trades.empty:
                st.markdown("### 🧾 Trades Executed")
                trades_display = trades.copy()
                trades_display["profit"] = pd.to_numeric(trades_display["profit"], errors="coerce").fillna(0)

                def highlight_profit(val):
                    color = '#d4f4dd' if val > 0 else ('#f4d4d4' if val < 0 else '')
                    return f'background-color: {color}'

                st.dataframe(trades_display.style.applymap(highlight_profit, subset=["profit"]))

                # ------------------ EMA Chart ------------------
                st.markdown("### 📉 EMA Crossovers")
                st.plotly_chart(plot_ema_chart(df_ind, trades), use_container_width=True)

                # ------------------ Equity Curve ------------------
                st.markdown("### 📈 Equity Curve")
                st.plotly_chart(plot_equity_curve(equity_curve), use_container_width=True)
            else:
                st.info("🔍 No trades executed for this stock.")

if __name__ == "__main__":
    main()
