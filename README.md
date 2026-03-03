# Nifty Momentum Strategy

A systematic equity momentum strategy backtested on Nifty 50 stocks (2022–2026), 
built in Python. Combines classical momentum factor investing with a market regime 
filter to manage drawdowns.

---

## Strategy Performance

| Metric | Momentum Strategy | Equal Weight Benchmark |
|--------|------------------|----------------------|
| CAGR | 26.3% | 23.7% |
| Sharpe Ratio | 1.39 | 1.32 |
| Max Drawdown | -7.1% | -13.5% |
| Total Return | 101.5% | 89.4% |
| Monthly Win Rate | 55.6% | — |
| Annualized Alpha | 5.0% | — |
| Beta | 0.88 | — |
| Alpha P-Value | 0.000 | — |

**Alpha is statistically significant at 99% confidence (p-value: 0.000)**

---

## Strategy Logic

### Signal: 12-1 Momentum
Rank all stocks by their past 12-month return, skipping the most recent month.

**Why 12 months?**  
Jegadeesh and Titman (1993) documented that 12-month momentum produces the 
strongest and most persistent returns across markets. Institutional investors 
operate on annual cycles — annual reviews, annual rebalancing, annual reporting — 
creating 12-month price trends.

**Why skip 1 month?**  
The most recent month exhibits short-term reversal due to bid-ask bounce and 
short-term overreaction (Jegadeesh 1990). Skipping it removes this noise and 
captures the clean medium-term trend.

### Portfolio Construction
- Select top 10 stocks by momentum score each month
- Equal weight all selected stocks (10% each)
- Rebalance monthly at month-end close prices

### Risk Management: Market Regime Filter
If Nifty 50 index is **below its 200-day moving average**, move entire 
portfolio to cash.

**Why?**  
Momentum strategies crash hardest during market downturns because momentum 
stocks (recent winners) are widely held and sold simultaneously during panics. 
The 200 DMA filter detects bear market regimes before the crash destroys returns.

**Result:** Reduced max drawdown from -60.5% (no filter) to -7.1% (with filter)

---

## Key Findings

### Seasonality Analysis
![Monthly Returns Heatmap](monthly_returns_heatmap.png)

Strong months: **May (+5.5%), June (+6.7%), September (+3.3%)**  
Weak months: **January (-0.4%), August (-1.5%), October (-1.7%)**

October shows structural weakness — particularly brutal in 2024 (-6.7%).  
Consider reducing exposure or moving to cash in August and October.

### Equity Curve
![Equity Curve](equity_curve.png)

### Alpha Decomposition
- **Beta 0.88**: Strategy takes 12% less market risk than passive index
- **Alpha 5% annualized**: After controlling for market exposure, 
  genuine skill-based outperformance remains
- **R-squared 0.66**: 34% of strategy returns are independent of 
  market movements — this is where the momentum signal lives

---

## Why Linear Regression for Alpha/Beta?

CAPM assumes a linear relationship between asset returns and market returns.  
Economic logic: if market moves 1%, assets move proportionally based on 
systematic risk — proportionality is linear by definition.

**Known limitation:** The relationship may be non-linear during crashes. 
Momentum stocks exhibit convex drawdowns not captured by a single linear beta. 
A more rigorous analysis would use regime-conditional regressions 
(separate bull/bear regressions). This is a planned improvement.

---

## Repository Structure
```
├── config.py          # All strategy parameters (change here, updates everywhere)
├── data.py            # Data download and preparation layer
├── signals.py         # Momentum signal calculation
├── backtest.py        # Monthly rebalancing engine with market filter
├── analysis.py        # Performance metrics: Sharpe, alpha, beta, win rate
├── visualisation.py   # Equity curve and monthly heatmap charts
└── main.py            # Entry point — runs complete backtest pipeline
```

**Architecture:** Modular separation of concerns. Each file has one job.  
Adding a new strategy = new signals.py only. Risk management and analysis unchanged.

---

## How to Run
```bash
# Install dependencies
pip install pandas numpy yfinance matplotlib seaborn scipy

# Run complete backtest
python main.py
```

---

## Known Limitations & Future Improvements

1. **Transaction costs not modeled** — Real returns approximately 2-4% lower 
   annually after brokerage, STT, and market impact
2. **Short backtest period** — 4 years includes limited market regimes. 
   Testing on 2010-2026 would improve statistical robustness
3. **Linear alpha/beta** — Regime-conditional regression would better capture 
   non-linear crash behavior
4. **Universe limited to 32 stocks** — Expanding to Nifty 500 would improve 
   signal quality and reduce concentration risk
5. **No out-of-sample test** — Strategy built and tested on same data period. 
   Walk-forward validation is the next step

---

## Academic References

- Jegadeesh, N. & Titman, S. (1993). *Returns to Buying Winners and Selling 
  Losers: Implications for Stock Market Efficiency.* Journal of Finance.
- Jegadeesh, N. (1990). *Evidence of Predictable Behavior of Security Returns.* 
  Journal of Finance.
- Faber, M. (2007). *A Quantitative Approach to Tactical Asset Allocation.* 
  Journal of Wealth Management.

---

## About

Built by Satbir Singh Rai — Senior Research Analyst with 10+ years covering 
US-listed financial exchanges and market infrastructure (SPGI, MCO, ICE, CME, 
NDAQ). Combining fundamental research expertise with Python-based systematic 
strategy development.

[LinkedIn](https://www.linkedin.com/in/satbir-singh-rai-b303a62b/) | 
