# 📈 EMA Trading Simulator

A comprehensive **Exponential Moving Average (EMA) trading simulator** built with Python and Streamlit.  
Learn how EMA-based trading strategies work, visualize trades, and analyze portfolio performance — all in an interactive, educational simulator.

---

## 🔹 Features

- **Hybrid Data Fetching**:  
  - Tries to fetch **live stock data** using Yahoo Finance (`yfinance`).  
  - Falls back to **cached CSV** or **synthetic data** if live data is unavailable.  

- **Customizable EMA Strategy**:  
  - Set **Fast EMA**, **Slow EMA**, and **EMA Difference Threshold**.  
  - Controls **initial capital** and **maximum trades**.  

- **Trade Analytics**:  
  - Displays **executed trades**, **profit/loss per trade**, and **portfolio summary**.  
  - Highlights profitable trades for easy visualization.  

- **Visualizations**:  
  - **EMA Crossover Chart** – shows fast vs slow EMA, with buy/sell signals.  
  - **Equity Curve** – tracks portfolio growth over time.  

- **Educational Explanation**:  
  - Step-by-step guide on how EMA works and how trading signals are generated.  
  - Helps users understand market dynamics and strategy mechanics.

---

## 🔹 How the Strategy Works

1. **Buy Signal**: Fast EMA > Slow EMA + Threshold → Buy.  
2. **Sell Signal**: Fast EMA < Slow EMA - Threshold → Sell.  
3. **Profit Mechanism**: Buy low, sell high based on EMA crossovers.  
4. **EMA Threshold**: Ensures trades are triggered only when the trend is significant.

---

## 🔹 Getting Started

### Prerequisites
- Python 3.10+
- pip
- Git

### Install Dependencies
```bash
pip install -r requirements.txt


Run the App

streamlit run run.py


🔹 Folder Structure

ema-trading-simulator/
│
├── src/
│   ├── app.py             # Main Streamlit app
│   ├── data_fetcher.py    # Fetches live/cached/synthetic stock data
│   ├── strategy.py        # EMA strategy logic
│   ├── portfolio.py       # Portfolio management and summary
│   └── utils.py           # Plotting functions
│
├── data/                  # Cached CSV files
├── run.py                 # Entry point
├── requirements.txt       # Python dependencies
└── README.md



🔹 How to Contribute

Fork the repo.

Create a new branch: git checkout -b feature/my-feature

Commit your changes: git commit -m "Add my feature"

Push to branch: git push origin feature/my-feature

Open a Pull Request.



