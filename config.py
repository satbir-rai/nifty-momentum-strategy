# config.py
# ============================================================
# STRATEGY CONFIGURATION
# All parameters live here. Change once, updates everywhere.
# ============================================================

# --- Universe ---
TICKERS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS",
    "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS",
    "BEL.NS", "BHARTIARTL.NS", "ICICIBANK.NS", "INDIGO.NS",
    "INFY.NS", "ITC.NS", "JIOFIN.NS", "JSWSTEEL.NS",
    "KOTAKBANK.NS", "LT.NS", "M&M.NS", "MARUTI.NS",
    "MAXHEALTH.NS", "NESTLEIND.NS", "RELIANCE.NS", "SBIN.NS",
    "SHRIRAMFIN.NS", "SUNPHARMA.NS", "TATASTEEL.NS", "TCS.NS",
    "TECHM.NS", "TITAN.NS", "UPL.NS", "WIPRO.NS"
]

NIFTY_TICKER = "^NSEI"

# --- Date Range ---
START_DATE = "2022-01-01"
END_DATE = "2026-02-27"

# --- Strategy Parameters ---
MOMENTUM_LOOKBACK = 12      # Months of momentum signal (Jegadeesh & Titman 1993)
MOMENTUM_SKIP = 1           # Skip most recent month to avoid short-term reversal
TOP_N_STOCKS = 10           # Number of stocks to hold each month
MARKET_FILTER_MA = 200      # Moving average days for market regime filter

# --- Risk Parameters ---
RISK_FREE_RATE_MONTHLY = 0.005   # 6% annual / 12 = 0.5% monthly (India 10yr bond approx)