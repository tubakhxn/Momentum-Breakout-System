"""
backtest.py
Runs the trading strategy, manages positions, and calculates performance metrics.
"""
import pandas as pd
import numpy as np

def run_backtest(df: pd.DataFrame, signals: pd.DataFrame, trailing_stop: float = 0.05, ma_window: int = 20) -> pd.DataFrame:
    """
    Simulate trades, apply exits, and calculate equity curve.
    Args:
        df (pd.DataFrame): Price and volume data.
        signals (pd.DataFrame): Buy/sell signals.
        trailing_stop (float): Trailing stop percentage.
        ma_window (int): Moving average window for exit.
    Returns:
        pd.DataFrame: DataFrame with trades, equity curve, and metrics.
    """
    position = 0
    entry_price = 0
    stop_price = 0
    equity = [1.0]
    trade_log = []
    max_equity = 1.0
    ma = df['Close'].rolling(ma_window).mean()
    for i in range(1, len(df)):
        date = df.index[i]
        price = df['Close'].iloc[i]
        if position == 0 and signals['buy_signal'].iloc[i]:
            position = 1
            entry_price = price
            stop_price = price * (1 - trailing_stop)
            trade_log.append({'Date': date, 'Type': 'Buy', 'Price': price})
        elif position == 1:
            stop_price = max(stop_price, price * (1 - trailing_stop))
            if price < stop_price or price < ma.iloc[i]:
                position = 0
                trade_log.append({'Date': date, 'Type': 'Sell', 'Price': price})
        # Update equity
        if position == 1:
            ret = price / entry_price
        else:
            ret = 1.0
        equity.append(equity[-1] * ret if position == 1 else equity[-1])
        max_equity = max(max_equity, equity[-1])
    equity_curve = pd.Series(equity[1:], index=df.index[1:])
    trades = pd.DataFrame(trade_log)
    return pd.DataFrame({'equity_curve': equity_curve}), trades

def calculate_metrics(equity_curve: pd.Series) -> dict:
    """
    Calculate total return, Sharpe ratio, and max drawdown.
    Args:
        equity_curve (pd.Series): Cumulative returns.
    Returns:
        dict: Performance metrics.
    """
    returns = equity_curve.pct_change().dropna()
    total_return = equity_curve.iloc[-1] - 1
    sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
    roll_max = equity_curve.cummax()
    drawdown = (equity_curve - roll_max) / roll_max
    max_drawdown = drawdown.min()
    return {
        'Total Return': f"{total_return*100:.2f}%",
        'Sharpe Ratio': f"{sharpe:.2f}",
        'Max Drawdown': f"{max_drawdown*100:.2f}%"
    }
