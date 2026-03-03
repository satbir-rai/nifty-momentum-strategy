# analysis.py
# ============================================================
# PERFORMANCE ANALYSIS
# Calculates all key metrics for strategy evaluation.
#
# KEY METRICS EXPLAINED:
#
# CAGR (Compound Annual Growth Rate):
#   The steady annual return that would produce your actual
#   total return. Accounts for compounding.
#   Formula: (Final Value / Initial Value)^(1/years) - 1
#
# SHARPE RATIO:
#   Return per unit of risk taken.
#   Formula: (Strategy Return - Risk Free Rate) / Volatility
#   Above 1.0 = decent, Above 1.5 = good, Above 2.0 = excellent
#
# MAX DRAWDOWN:
#   Worst peak-to-trough loss in the entire period.
#   Tells you the worst case scenario you'd have experienced.
#   Critical for assessing whether you could psychologically
#   hold through the strategy's bad periods.
#
# ALPHA:
#   Return generated ABOVE what market exposure alone explains.
#   Pure skill component. Calculated via regression against benchmark.
#   5% alpha = after accounting for market risk, you earn 5% extra/year.
#
# BETA:
#   Sensitivity to market movements.
#   Beta 0.88 = if market falls 10%, strategy falls 8.8%.
#   Below 1.0 = less risky than market. Above 1.0 = more risky.
#
# P-VALUE:
#   Probability that your alpha is due to pure luck.
#   Below 0.05 = less than 5% chance it's luck = statistically significant.
#   Your result of 0.000 = essentially zero chance of luck.
# ============================================================

import pandas as pd
import numpy as np
from scipy import stats
from config import RISK_FREE_RATE_MONTHLY


def calculate_metrics(returns, name="Strategy"):
    """Calculate and print all performance metrics."""
    
    cumulative = (1 + returns).cumprod()
    n_years = len(returns) / 12
    
    # CAGR
    cagr = (cumulative.iloc[-1] ** (1/n_years)) - 1
    
    # Sharpe Ratio
    excess_returns = returns - RISK_FREE_RATE_MONTHLY
    sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(12)
    
    # Maximum Drawdown
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    
    # Win Rate
    wins = (returns > 0).sum()
    win_rate = wins / len(returns)
    
    print(f"\n{'='*45}")
    print(f"{name} Performance")
    print(f"{'='*45}")
    print(f"CAGR:           {cagr:.1%}")
    print(f"Sharpe Ratio:   {sharpe:.2f}")
    print(f"Max Drawdown:   {max_drawdown:.1%}")
    print(f"Total Return:   {(cumulative.iloc[-1]-1):.1%}")
    print(f"Monthly Win Rate: {win_rate:.1%}")
    
    return cumulative


def calculate_alpha_beta(strategy_returns, benchmark_returns):
    """
    Decompose strategy returns into alpha (skill) and beta (market exposure).
    
    Uses OLS regression: Strategy Return = Alpha + Beta * Benchmark Return
    
    WHY LINEAR REGRESSION?
    CAPM theory assumes linear relationship between asset and market returns.
    Economic logic: if market moves 1%, assets move proportionally based on
    their systematic risk. This proportionality is linear by definition.
    
    LIMITATION: Real relationship may be non-linear, especially during crashes
    when momentum stocks exhibit convex drawdowns. A more rigorous analysis
    would use regime-conditional regressions (separate bull/bear regressions).
    """
    aligned = pd.DataFrame({
        'strategy': strategy_returns,
        'benchmark': benchmark_returns
    }).dropna()

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        aligned['benchmark'],
        aligned['strategy']
    )

    beta = slope
    monthly_alpha = intercept
    annual_alpha = (1 + monthly_alpha) ** 12 - 1
    r_squared = r_value ** 2

    print(f"\n{'='*45}")
    print("ALPHA & BETA ANALYSIS")
    print(f"{'='*45}")
    print(f"Beta:              {beta:.2f}")
    print(f"Monthly Alpha:     {monthly_alpha:.3%}")
    print(f"Annualized Alpha:  {annual_alpha:.2%}")
    print(f"R-squared:         {r_squared:.2f}")
    print(f"P-value:           {p_value:.3f}")
    print()
    
    if p_value < 0.05:
        print("✅ Alpha is statistically significant at 95% confidence")
        print("   Interpretation: Less than 5% probability this is due to luck")
    else:
        print("❌ Alpha is NOT statistically significant")
        print("   Interpretation: Results may be due to chance")

    print()
    print(f"For every 1% the market moves, strategy moves {beta:.2f}%")
    print(f"After market risk adjustment: {annual_alpha:.1%} genuine alpha per year")
    
    return beta, annual_alpha, r_squared, p_value


def calculate_win_rate(strategy_returns, benchmark_returns):
    """
    Calculate how often strategy beats benchmark month by month.
    
    Win rate above 50% = strategy consistently adds value.
    Symmetric win/loss amounts = edge comes from consistency not outliers.
    Asymmetric (bigger wins than losses) = even better, positive skew.
    """
    outperformance = strategy_returns - benchmark_returns
    
    wins = (outperformance > 0).sum()
    total = len(outperformance)
    win_rate = wins / total
    
    avg_win = outperformance[outperformance > 0].mean()
    avg_loss = outperformance[outperformance < 0].mean()
    
    print(f"\n{'='*45}")
    print("BENCHMARK COMPARISON")
    print(f"{'='*45}")
    print(f"Monthly Win Rate:     {win_rate:.1%}")
    print(f"Months beating benchmark: {wins} of {total}")
    print(f"Avg outperformance (wins):  {avg_win:.2%}")
    print(f"Avg underperformance (losses): {avg_loss:.2%}")
    
    # Skill ratio: avg win / abs(avg loss). Above 1 = positive skew
    if avg_loss != 0:
        skill_ratio = abs(avg_win / avg_loss)
        print(f"Skill Ratio (win/loss size): {skill_ratio:.2f}x")
    
    return win_rate, avg_win, avg_loss