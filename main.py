# main.py
# ============================================================
# MAIN ENTRY POINT
# Run this file to execute the complete momentum strategy
# backtest and generate all analysis and charts.
#
# STRATEGY SUMMARY:
# - Universe: 32 Nifty 50 stocks
# - Signal: 12-month momentum, skip 1 month (Jegadeesh & Titman 1993)
# - Portfolio: Top 10 stocks, equal weighted
# - Risk Management: Exit to cash when Nifty below 200-day MA
# - Rebalancing: Monthly
#
# RESULTS (2022-2026):
# - CAGR: 26.3% vs benchmark 23.7%
# - Sharpe: 1.39 vs benchmark 1.32
# - Max Drawdown: -7.1% vs benchmark -13.5%
# - Alpha: 5% annualized (p-value: 0.000, statistically significant)
# - Beta: 0.88 (less market risk than benchmark)
# - Monthly Win Rate: 55.6%
# ============================================================

from data import download_prices, download_nifty
from signals import calculate_momentum, build_monthly_holdings
from backtest import run_backtest
from analysis import calculate_metrics, calculate_alpha_beta, calculate_win_rate
from visualisation import plot_equity_curve, plot_monthly_heatmap


def main():
    print("=" * 50)
    print("NIFTY MOMENTUM STRATEGY BACKTEST")
    print("=" * 50)

    # Step 1: Get data
    print("\n[1/5] Downloading market data...")
    monthly_prices, monthly_returns = download_prices()
    nifty_monthly, nifty_ma200 = download_nifty()

    # Step 2: Generate signals
    print("\n[2/5] Calculating momentum signals...")
    momentum = calculate_momentum(monthly_returns)
    portfolio_holdings = build_monthly_holdings(momentum)

    # Step 3: Run backtest
    print("\n[3/5] Running backtest...")
    strategy_series, benchmark_series = run_backtest(
        monthly_returns, portfolio_holdings, nifty_monthly, nifty_ma200
    )

    # Step 4: Analyse performance
    print("\n[4/5] Analysing performance...")
    calculate_metrics(strategy_series, "Momentum Strategy")
    calculate_metrics(benchmark_series, "Equal Weight Benchmark")
    calculate_alpha_beta(strategy_series, benchmark_series)
    calculate_win_rate(strategy_series, benchmark_series)

    # Step 5: Generate charts
    print("\n[5/5] Generating charts...")
    plot_equity_curve(strategy_series, benchmark_series)
    plot_monthly_heatmap(strategy_series)

    print("\n✅ Backtest complete. All charts saved.")
    print("Files generated: equity_curve.png, monthly_returns_heatmap.png")


if __name__ == "__main__":
    main()