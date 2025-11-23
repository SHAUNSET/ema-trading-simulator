import streamlit as st
import os
from src.data_fetcher import fetch_hybrid as fetch_historical
from src.strategy import backtest_ema
from src.portfolio import Portfolio
from src.utils import plot_ema_chart, plot_equity_curve
from datetime import datetime

def main():
    st.set_page_config(page_title="EMA Simulator", layout="wide")
    st.title("📈 EMA Trading Simulator")

    # ------------------ Strategy Explanation ------------------
    with st.expander("📖 Strategy Explanation"):
        st.markdown("""
### Understanding EMA (Exponential Moving Average)

An **EMA (Exponential Moving Average)** is a type of moving average that gives **more weight to recent prices**.  
This makes it react faster to recent price changes compared to a simple moving average.

- **Fast EMA**: Reacts quickly to recent price changes. Captures short-term trends.
- **Slow EMA**: Reacts slower. Captures long-term trends.
- **EMA Difference Threshold**: A value that defines how far apart the fast and slow EMA must be to trigger a buy or sell.

### How the Strategy Works

1. **Buy Signal**  
   - When the **Fast EMA** crosses **above the Slow EMA** by more than the threshold.  
   - Indicates the stock is gaining momentum upward.  

2. **Sell Signal**  
   - When the **Fast EMA** crosses **below the Slow EMA** by more than the threshold.  
   - Indicates the stock is losing momentum or may reverse downward.

### Trade Example

- Fast EMA = 10-day EMA  
- Slow EMA = 21-day EMA  
- Threshold = 0.5  

If the 10-day EMA is **higher than 21-day EMA + 0.5**, the strategy triggers a **buy**.  
If the 10-day EMA falls **below 21-day EMA - 0.5**, the strategy triggers a **sell**.

### Making Profit

- Profit is made when you **buy low and sell high** based on EMA signals.  
- The **portfolio value** updates after every trade, reflecting gains/losses.  
- By adjusting **Fast EMA, Slow EMA, and Threshold**, you can fine-tune the strategy to respond faster or slower to market trends.

### Visual Guides

- **EMA Crossover Chart**: Shows Fast EMA vs Slow EMA. Buy signals marked in green, Sell signals in red.  
- **Equity Curve**: Shows portfolio growth over time. Helps visualize overall performance.

### Tips for Users

- Start with default settings and observe how trades are executed.  
- Experiment with different EMA periods and thresholds to understand their effect.  
- Focus on the **profit/loss column** to see which trades were successful.  
- Remember: No strategy guarantees profit — this simulator is **educational** and helps understand market dynamics.

""")

    # ------------------ Backtest Settings ------------------
    st.sidebar.header("Backtest Settings")
    stocks = st.sidebar.multiselect(
        "Select Stocks",
        ["AAPL", "MSFT", "TSLA"],
        default=["AAPL"]
    )
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

            if df.empty:
                st.error(f"❌ Could not fetch data for {stock}. Using cached or synthetic data.")
                continue

            # Show last update timestamp
            cache_path = f"data/{stock}.csv"
            if os.path.exists(cache_path):
                ts = datetime.fromtimestamp(os.path.getmtime(cache_path)).strftime("%Y-%m-%d %H:%M:%S")
                st.caption(f"🗂️ Data last updated: **{ts}**")
            else:
                st.caption("🗂️ No cache timestamp available.")

            # Run strategy
            trades, equity_curve, df_ind = backtest_ema(df, fast, slow, capital, threshold, max_trades)
            portfolio = Portfolio(capital)
            portfolio.update(trades)

            # Portfolio summary
            st.markdown("### 💼 Portfolio Summary")
            st.markdown(portfolio.summary())

            # Trades table
            if not trades.empty:
                st.markdown("### 🧾 Trades Executed")
                st.dataframe(
                    trades.style.apply(
                        lambda row: [
                            'background-color: #d4f4dd' if col == 'Profit' and v > 0
                            else ('background-color: #f4d4d4' if col == 'Profit' and v <= 0 else '')
                            for col, v in zip(row.index, row)
                        ],
                        axis=1
                    )
                )

                # EMA Chart
                st.markdown("### 📉 EMA Crossovers")
                st.plotly_chart(plot_ema_chart(df_ind, trades), use_container_width=True)

                # Equity Curve
                st.markdown("### 📈 Equity Curve")
                st.plotly_chart(plot_equity_curve(equity_curve), use_container_width=True)
            else:
                st.info("🔍 No trades executed for this stock.")

if __name__ == "__main__":
    main()
