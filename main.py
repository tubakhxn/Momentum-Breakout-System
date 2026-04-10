"""
main.py
Orchestrates the trading system: loads data, runs strategy, backtests, visualizes, and outputs results.
"""
from data import fetch_data
from strategy import generate_signals
from backtest import run_backtest, calculate_metrics
from visualization import plot_all

if __name__ == "__main__":
    import argparse
    import sys
    import pandas as pd
    from datetime import datetime, timedelta
    from data import fetch_data
    from strategy import generate_signals
    from backtest import run_backtest, calculate_metrics
    # from visualization import plot_price_signals, plot_equity_curve, plot_volume

    parser = argparse.ArgumentParser(description="Momentum Breakout Trading System")
    parser.add_argument('--symbol', type=str, default='AAPL', help='Ticker symbol (default: AAPL)')
    parser.add_argument('--start', type=str, default=(datetime.now()-timedelta(days=365)).strftime('%Y-%m-%d'), help='Start date')
    parser.add_argument('--end', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date')
    parser.add_argument('--simulate', action='store_true', help='Use simulated data')
    args = parser.parse_args()

    print(f"Fetching data for {args.symbol}...")
    df = fetch_data(args.symbol, args.start, args.end, simulate=args.simulate)
    print("Generating signals...")
    signals = generate_signals(df)
    print("Running backtest...")
    equity_df, trades = run_backtest(df, signals)
    equity_curve = equity_df['equity_curve']
    print("Calculating metrics...")
    metrics = calculate_metrics(equity_curve)

    print("\nPerformance Summary:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\nTrade Log:")
    print(trades)

    print("\nPlotting results...")
    plot_all(df, signals, trades, equity_curve)
