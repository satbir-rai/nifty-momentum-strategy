# backtest.py
# ============================================================
# BACKTEST ENGINE
# Simulates monthly rebalancing of momentum portfolio.
#
# REBALANCING LOGIC:
# - Last day of each month: run momentum ranking
# - Select top N stocks
# - Hold equally weighted for next month
# - If market filter triggers (Nifty below 200 DMA): go to cash
#
# MARKET FILTER:
# Momentum crashes hardest during market downturns because
# momentum stocks (recent winners) are held by many investors
# who all sell simultaneously during panic. The 200 DMA filter
# detects bear market regimes and moves to cash before the crash.
# Research: Faber (2007) showed this simple filter dramatically
# reduces drawdowns in trend-following strategies.
#
# IMPORTANT ASSUMPTION:
# We assume trading at month-end close prices with no
# transaction costs or market impact. Real returns would be
# 2-4% lower annually after costs. This is a known limitation.
# ============================================================

import pandas as pd
import numpy as np


def run_backtest(monthly_returns, portfolio_holdings, nifty_monthly, nifty_ma200):
    """
    Run monthly momentum backtest with market filter.
    
    Args:
        monthly_returns: DataFrame of monthly stock returns
        portfolio_holdings: Dict of {date: [list of stocks]}
        nifty_monthly: Series of monthly Nifty 50 prices
        nifty_ma200: Series of Nifty 200-day MA (resampled monthly)
    
    Returns:
        strategy_series: Monthly strategy returns
        benchmark_series: Monthly equal-weight benchmark returns
    """
    strategy_returns = []
    dates = []

    for i in range(1, len(monthly_returns)):
        date = monthly_returns.index[i]
        prev_date = monthly_returns.index[i-1]

        # ── MARKET REGIME FILTER ──
        # If Nifty is below its 200-day MA, we are in a bear market regime
        # Go to cash (return = 0) instead of holding momentum stocks
        # This is the single most impactful risk management rule
        try:
            nifty_price = nifty_monthly.loc[prev_date].item()
            nifty_ma = nifty_ma200.loc[prev_date].item()
            
            if nifty_price < nifty_ma:
                strategy_returns.append(0)  # Cash = 0% return
                dates.append(date)
                continue
        except (KeyError, ValueError):
            pass  # If data missing, continue without filter

        # ── PORTFOLIO RETURN ──
        # Equal weight all selected stocks
        # Each stock gets 1/N of portfolio
        holdings = portfolio_holdings.get(prev_date, [])

        if len(holdings) == 0:
            strategy_returns.append(np.nan)
        else:
            # Mean = equal weight average return across all holdings
            ret = monthly_returns.loc[date, holdings].mean()
            strategy_returns.append(ret)
        
        dates.append(date)

    strategy_series = pd.Series(strategy_returns, index=dates).dropna()
    
    # Benchmark: equal weight ALL stocks in universe each month
    # This is our comparison - can momentum beat simple equal weighting?
    benchmark_series = monthly_returns.mean(axis=1).loc[strategy_series.index]

    return strategy_series, benchmark_series