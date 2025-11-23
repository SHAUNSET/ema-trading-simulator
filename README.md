EMA Trading Simulator 
Project: EMA Trading Simulator
GitHub: SHAUNSET/ema-trading-simulator
________________________________________
Overview
The EMA Trading Simulator is an interactive Python-based platform that allows users to simulate stock trading using Exponential Moving Averages (EMA).
It provides: - Live market data (when available) - Synthetic data fallback for experimentation - Visualization of trades and portfolio performance
Ideal for: - Learning EMA and trading strategies - Practicing trading analytics without financial risk - Backtesting custom strategies
________________________________________
Features
•	EMA Strategy Backtesting
o	Fast EMA vs Slow EMA crossovers
o	Configurable thresholds for triggering trades
o	Adjustable capital, trade limits, and EMA periods
•	Data Handling
o	Live stock data via Yahoo Finance
o	Synthetic data fallback if live data unavailable
o	Local caching for faster re-runs
•	Portfolio Analytics
o	Tracks executed trades and portfolio value
o	Displays total and profitable trades
o	Shows average profit per winning trade
•	Visualizations
o	EMA Crossover chart with buy/sell markers
o	Equity Curve chart showing portfolio growth
•	User-Friendly Interface
o	Interactive sliders and inputs
o	Strategy explanations and tooltips
o	Color-coded trade tables for quick analysis
________________________________________
How It Works
Fast EMA vs Slow EMA
•	Fast EMA: Captures short-term trends (reacts quickly to price changes)
•	Slow EMA: Captures long-term trends (reacts slowly)
Trading Signals
•	Buy Signal: Fast EMA > Slow EMA + Threshold
•	Sell Signal: Fast EMA < Slow EMA - Threshold
Profit
•	Buy low, sell high based on EMA crossovers
•	Portfolio value updates after each trade
Visualization
•	EMA Crossover Chart: Highlights buy/sell points
•	Equity Curve: Shows portfolio growth over time
________________________________________
Installation
1.	Clone the repository:
git clone https://github.com/SHAUNSET/ema-trading-simulator.git
cd ema-trading-simulator
2.	Create a virtual environment:
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
3.	Install dependencies:
pip install -r requirements.txt
________________________________________
Usage
1.	Run the app:
streamlit run run.py
2.	Select stocks (e.g., AAPL, MSFT, TSLA)
3.	Adjust parameters:
o	Fast EMA
o	Slow EMA
o	EMA Difference Threshold
o	Initial Capital
o	Max Trades
4.	Click Run Backtest
5.	Analyze:
o	Portfolio summary
o	Trades executed
o	EMA crossover chart
o	Equity curve
________________________________________
Tech Stack
•	Python – Core language
•	Streamlit – Frontend/UI
•	Pandas & Numpy – Data handling
•	Plotly – Interactive charting
•	yFinance – Live stock data fetch
•	SQLite / CSV – Data caching
________________________________________
Future Enhancements
•	Multi-indicator support (RSI, MACD)
•	Multi-stock portfolio simulation
•	Risk management features (stop-loss, position sizing)
•	Real-time notifications for live trading
________________________________________
License
MIT License © 2025 SHAUNSET
