import plotly.graph_objs as go
import pandas as pd

def plot_ema_chart(df, trades_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["close"], mode="lines", name="Close"))
    fig.add_trace(go.Scatter(x=df["date"], y=df["ema_fast"], mode="lines", name="EMA Fast"))
    fig.add_trace(go.Scatter(x=df["date"], y=df["ema_slow"], mode="lines", name="EMA Slow"))

    for _, t in trades_df.iterrows():
        if pd.notnull(t["entry_date"]):
            fig.add_trace(go.Scatter(
                x=[t["entry_date"]], y=[t["entry_price"]],
                mode="markers", marker=dict(color="green", size=10),
                name="BUY"
            ))
        if pd.notnull(t["exit_date"]):
            fig.add_trace(go.Scatter(
                x=[t["exit_date"]], y=[t["exit_price"]],
                mode="markers", marker=dict(color="red", size=10),
                name="SELL"
            ))
    fig.update_layout(title="EMA Crossovers", xaxis_title="Date", yaxis_title="Price")
    return fig

def plot_equity_curve(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["equity"], mode="lines", name="Equity"))
    fig.update_layout(title="Equity Curve", xaxis_title="Date", yaxis_title="Portfolio Value")
    return fig
