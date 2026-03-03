# data.py
# ============================================================
# DATA LAYER
# Downloads and prepares all price data.
# Separated from strategy logic so you can swap data sources
# later (Bloomberg, NSE direct feed, etc.) without touching
# strategy code.
# ============================================================

import pandas as pd
import yfinance as yf
from config import TICKERS, NIFTY_TICKER, START_DATE, END_DATE


def download_prices():
    """
    Download monthly closing prices for all tickers.
    Returns DataFrame with dates as index, tickers as columns.
    """
    print(f"Downloading price data for {len(TICKERS)} stocks...")
    prices = yf.download(TICKERS, start=START_DATE, end=END_DATE)["Close"]
    
    # Resample to month-end prices
    monthly_prices = prices.resample("ME").last()
    
    # Calculate monthly returns: (this month price / last month price) - 1
    monthly_returns = monthly_prices.pct_change()
    
    print(f"Downloaded {len(monthly_prices)} months of data")
    print(f"Date range: {monthly_prices.index[0].date()} to {monthly_prices.index[-1].date()}")
    
    return monthly_prices, monthly_returns


def download_nifty():
    """
    Download Nifty 50 index data for market regime filter.
    Returns monthly prices and 200-day moving average.
    
    Why 200 DMA? It's the most widely watched trend indicator
    by institutional investors globally. Crossing below signals
    regime change from bull to bear market.
    """
    print("Downloading Nifty 50 index data...")
    nifty_daily = yf.download(NIFTY_TICKER, start=START_DATE, end=END_DATE)["Close"]
    
    # Monthly last price for regime comparison
    nifty_monthly = nifty_daily.resample("ME").last()
    
    # 200-day MA calculated on daily data, then resampled to monthly
    # Using daily data gives more accurate MA than calculating on monthly
    nifty_ma200 = nifty_daily.rolling(200).mean().resample("ME").last()
    
    return nifty_monthly, nifty_ma200
    