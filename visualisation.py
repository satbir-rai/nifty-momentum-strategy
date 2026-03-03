# visualisation.py
# ============================================================
# ALL CHARTS AND VISUALISATIONS
# Separated so you can regenerate charts without rerunning
# the entire backtest.
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_equity_curve(strategy_series, benchmark_series):
    """
    Plot cumulative returns of strategy vs benchmark.
    Shows how ₹100 grows over time under each approach.
    """
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    (1 + strategy_series).cumprod().mul(100).plot(
        ax=ax, label="Momentum Strategy", color="#00ff88", linewidth=2
    )
    (1 + benchmark_series).cumprod().mul(100).plot(
        ax=ax, label="Equal Weight Benchmark", color="#ff9500",
        linewidth=2, linestyle="--"
    )

    ax.set_title("Nifty Momentum Strategy vs Benchmark",
                 color='white', fontsize=14, fontweight='bold')
    ax.set_ylabel("Portfolio Value (Starting ₹100)", color='white')
    ax.set_xlabel("Date", color='white')
    ax.tick_params(colors='white')
    ax.legend(facecolor='#2d2d2d', labelcolor='white')
    ax.grid(True, alpha=0.2, color='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig("equity_curve.png", dpi=150, bbox_inches='tight',
                facecolor='#1a1a2e')
    plt.show()
    print("Saved: equity_curve.png")


def plot_monthly_heatmap(strategy_series):
    """
    Monthly returns heatmap with seasonality analysis.
    
    Rows = years, Columns = months.
    Red = negative month, Green = positive month.
    Bottom bar chart shows average return by month across all years.
    
    USE: Identify months where strategy consistently struggles.
    Consider reducing position size or going to cash in weak months.
    """
    monthly_df = strategy_series.copy()
    monthly_df.index = pd.to_datetime(monthly_df.index)

    heatmap_data = pd.DataFrame({
        'Year': monthly_df.index.year,
        'Month': monthly_df.index.month,
        'Return': monthly_df.values
    })

    pivot = heatmap_data.pivot_table(
        values='Return', index='Year', columns='Month'
    )

    month_names = ['Jan','Feb','Mar','Apr','May','Jun',
                   'Jul','Aug','Sep','Oct','Nov','Dec']
    pivot.columns = [month_names[m-1] for m in pivot.columns]

    avg_row = pivot.mean()
    pivot['Annual'] = (1 + pivot.fillna(0)).prod(axis=1) - 1

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(14, 8),
        gridspec_kw={'height_ratios': [4, 1]},
        facecolor='#1a1a2e'
    )

    sns.heatmap(
        pivot.iloc[:, :-1],
        annot=pivot.iloc[:, :-1].map(
            lambda x: f"{x:.1%}" if pd.notna(x) else ""
        ),
        fmt='', cmap='RdYlGn', center=0,
        linewidths=0.5, linecolor='#2d2d2d', ax=ax1,
        cbar_kws={'label': 'Monthly Return', 'shrink': 0.8},
        annot_kws={'size': 9}
    )

    for i, (year, row) in enumerate(pivot.iterrows()):
        annual = row['Annual']
        color = '#00ff88' if annual > 0 else '#ff4444'
        ax1.text(len(month_names) + 0.6, i + 0.5,
                 f"{annual:.1%}", va='center', ha='left',
                 color=color, fontsize=9, fontweight='bold')

    ax1.text(len(month_names) + 0.6, -0.3, 'Annual',
             va='center', ha='left', color='white',
             fontsize=9, fontweight='bold')
    ax1.set_title('Momentum Strategy - Monthly Returns Heatmap',
                  fontsize=14, color='white', pad=15, fontweight='bold')
    ax1.set_xlabel('')
    ax1.set_ylabel('Year', color='white')
    ax1.tick_params(colors='white')

    colors = ['#00cc44' if v > 0 else '#cc0000' for v in avg_row.values]
    bars = ax2.bar(range(len(avg_row)), avg_row.values,
                   color=colors, alpha=0.8)

    for bar, val in zip(bars, avg_row.values):
        ax2.text(bar.get_x() + bar.get_width()/2,
                 val + (0.001 if val > 0 else -0.003),
                 f"{val:.1%}", ha='center',
                 va='bottom' if val > 0 else 'top',
                 color='white', fontsize=8)

    ax2.set_xticks(range(len(avg_row)))
    ax2.set_xticklabels(month_names, color='white', fontsize=9)
    ax2.set_title('Average Monthly Return by Month',
                  color='white', fontsize=11)
    ax2.set_facecolor('#1a1a2e')
    ax2.tick_params(colors='white')
    ax2.axhline(y=0, color='white', linewidth=0.5, alpha=0.5)
    ax2.spines['bottom'].set_color('white')
    ax2.spines['left'].set_color('white')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig('monthly_returns_heatmap.png', dpi=150,
                bbox_inches='tight', facecolor='#1a1a2e')
    plt.show()

    print("\nSeasonal Analysis:")
    print("=" * 45)
    for month, ret in avg_row.items():
        signal = "⚠️ AVOID" if ret < -0.01 else (
            "✅ STRONG" if ret > 0.02 else "➡️ NEUTRAL"
        )
        print(f"{month:>4}: {ret:>7.2%}  {signal}")
    
    print("Saved: monthly_returns_heatmap.png")