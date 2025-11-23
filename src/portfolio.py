class Portfolio:
    def __init__(self, capital):
        self.initial = capital
        self.trades = []

    def update(self, trades_df):
        self.trades = trades_df

    def summary(self):
        if self.trades.empty:
            return f"Initial Capital: {self.initial}\nNo trades executed."
        total_profit = self.trades["profit"].sum()
        profitable = self.trades[self.trades["profit"] > 0].shape[0]
        total_trades = self.trades.shape[0]
        final_value = self.initial + total_profit
        return f"""
**Initial Capital:** {self.initial}  
**Final Portfolio Value:** {final_value:.2f}  
**Total P/L:** {total_profit:.2f}  
**Trades Executed:** {total_trades}  
**Profitable Trades:** {profitable} ({profitable/total_trades*100:.2f}%)  
        """
