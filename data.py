"""
data.py
Fetches or simulates historical price and volume data for the trading system.
"""
import pandas as pd
import numpy as np

def fetch_data(symbol: str, start: str, end: str, simulate: bool = False) -> pd.DataFrame:
    """
    Fetch historical price and volume data using yfinance or simulate data.
    Args:
        symbol (str): Ticker symbol.
        start (str): Start date (YYYY-MM-DD).
        end (str): End date (YYYY-MM-DD).
        simulate (bool): If True, generate simulated data.
    Returns:
        pd.DataFrame: DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume']
    """
    if simulate:
        np.random.seed(42)
        dates = pd.date_range(start, end)
        price = np.cumprod(1 + np.random.normal(0, 0.01, len(dates))) * 100
        volume = np.random.randint(1e5, 2e5, len(dates))
        df = pd.DataFrame({
            'Open': price * (1 + np.random.normal(0, 0.002, len(dates))),
            'High': price * (1 + np.random.normal(0.01, 0.005, len(dates))),
            'Low': price * (1 - np.random.normal(0.01, 0.005, len(dates))),
            'Close': price,
            'Volume': volume
        }, index=dates)
        return df
    else:
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("yfinance not installed. Please install it or use simulate=True.")
        df = yf.download(symbol, start=start, end=end)
        if df.empty:
            raise ValueError("No data fetched. Check symbol and date range.")
        return df[['Open', 'High', 'Low', 'Close', 'Volume']]
