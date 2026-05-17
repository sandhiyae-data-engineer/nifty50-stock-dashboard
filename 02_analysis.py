import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# paths setup
BASE_DIR = r"C:\Users\sandh\Desktop\stock_project"
CSV_DIR = os.path.join(BASE_DIR, "csv_output")
SECTOR_FILE = os.path.join(BASE_DIR, "Sector_data - Sheet1.csv")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# load all csv files
all_files = glob.glob(os.path.join(CSV_DIR, "*.csv"))
print(f"Total stocks loaded: {len(all_files)}")

summary_list = []

for file in all_files:
    ticker = os.path.basename(file).replace(".csv", "")
    df = pd.read_csv(file, parse_dates=['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

    if len(df) < 2:
        continue

    start_price = df['Close'].iloc[0]
    end_price = df['Close'].iloc[-1]
    yearly_return = ((end_price - start_price) / start_price) * 100
    daily_return = df['Close'].pct_change().dropna()
    volatility = daily_return.std() * 100
    avg_price = df['Close'].mean()
    avg_volume = df['Volume'].mean()

    summary_list.append({
        'Ticker': ticker,
        'Start_Price': round(start_price, 2),
        'End_Price': round(end_price, 2),
        'Yearly_Return': round(yearly_return, 2),
        'Volatility': round(volatility, 4),
        'Avg_Price': round(avg_price, 2),
        'Avg_Volume': round(avg_volume, 0)
    })

summary_df = pd.DataFrame(summary_list)
summary_df.to_csv(os.path.join(BASE_DIR, "market_summary.csv"), index=False)

# top 10 green and red stocks
top10_green = summary_df.nlargest(10, 'Yearly_Return')
top10_red = summary_df.nsmallest(10, 'Yearly_Return')

print("\n--- TOP 10 GREEN STOCKS ---")
print(top10_green[['Ticker', 'Yearly_Return']].to_string(index=False))
print("\n--- TOP 10 RED STOCKS ---")
print(top10_red[['Ticker', 'Yearly_Return']].to_string(index=False))

# market summary
green_count = len(summary_df[summary_df['Yearly_Return'] > 0])
red_count = len(summary_df[summary_df['Yearly_Return'] <= 0])
print(f"\n--- MARKET SUMMARY ---")
print(f"Green Stocks : {green_count}")
print(f"Red Stocks   : {red_count}")
print(f"Avg Price    : {summary_df['Avg_Price'].mean():.2f}")
print(f"Avg Volume   : {summary_df['Avg_Volume'].mean():.0f}")

# chart 1 - top 10 volatile stocks
top10_vol = summary_df.nlargest(10, 'Volatility')
plt.figure(figsize=(12, 6))
plt.bar(top10_vol['Ticker'], top10_vol['Volatility'], color='orange')
plt.title('Top 10 Most Volatile Stocks')
plt.xlabel('Stock')
plt.ylabel('Volatility (Std Dev %)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'chart1_volatility.png'))
plt.close()
print("Chart 1 saved.")

# chart 2 - cumulative return top 5 stocks
top5 = summary_df.nlargest(5, 'Yearly_Return')['Ticker'].tolist()
plt.figure(figsize=(14, 7))
for ticker in top5:
    df = pd.read_csv(os.path.join(CSV_DIR, f"{ticker}.csv"), parse_dates=['Date'])
    df = df.sort_values('Date')
    df['Daily_Return'] = df['Close'].pct_change()
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1
    plt.plot(df['Date'], df['Cumulative_Return'] * 100, label=ticker)
plt.title('Cumulative Return - Top 5 Stocks')
plt.xlabel('Date')
plt.ylabel('Cumulative Return (%)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'chart2_cumulative_return.png'))
plt.close()
print("Chart 2 saved.")

# chart 3 - sector wise performance
try:
    sector_df = pd.read_csv(SECTOR_FILE)
    print(f"Sector columns: {sector_df.columns.tolist()}")
    ticker_col = [c for c in sector_df.columns if 'ticker' in c.lower() or 'symbol' in c.lower()][0]
    sector_col = [c for c in sector_df.columns if 'sector' in c.lower()][0]
    sector_df = sector_df.rename(columns={ticker_col: 'Ticker', sector_col: 'Sector'})
    merged = summary_df.merge(sector_df[['Ticker', 'Sector']], on='Ticker', how='left')
    sector_avg = merged.groupby('Sector')['Yearly_Return'].mean().sort_values()
    plt.figure(figsize=(12, 6))
    colors = ['green' if x > 0 else 'red' for x in sector_avg.values]
    plt.bar(sector_avg.index, sector_avg.values, color=colors)
    plt.title('Average Yearly Return by Sector')
    plt.xlabel('Sector')
    plt.ylabel('Avg Yearly Return (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'chart3_sector.png'))
    plt.close()
    print("Chart 3 saved.")
except Exception as e:
    print(f"Sector chart error: {e}")

# chart 4 - correlation heatmap
close_dict = {}
for file in all_files:
    ticker = os.path.basename(file).replace(".csv", "")
    df = pd.read_csv(file, parse_dates=['Date'])
    df = df.sort_values('Date')
    close_dict[ticker] = df.set_index('Date')['Close']
close_df = pd.DataFrame(close_dict).dropna(axis=1, thresh=100)
corr_matrix = close_df.pct_change().corr()
plt.figure(figsize=(20, 16))
sns.heatmap(corr_matrix, annot=False, cmap='RdYlGn', center=0, linewidths=0.3)
plt.title('Stock Price Correlation Heatmap')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'chart4_correlation.png'))
plt.close()
print("Chart 4 saved.")

# chart 5 - monthly top 5 gainers and losers
all_monthly = []
for file in all_files:
    ticker = os.path.basename(file).replace(".csv", "")
    df = pd.read_csv(file, parse_dates=['Date'])
    df['YearMonth'] = df['Date'].dt.to_period('M')
    for month, grp in df.groupby('YearMonth'):
        if len(grp) < 2:
            continue
        ret = ((grp['Close'].iloc[-1] - grp['Close'].iloc[0]) / grp['Close'].iloc[0]) * 100
        all_monthly.append({'Ticker': ticker, 'Month': str(month), 'Monthly_Return': round(ret, 2)})

monthly_df = pd.DataFrame(all_monthly)
months = sorted(monthly_df['Month'].unique())
fig, axes = plt.subplots(len(months), 1, figsize=(14, 6 * len(months)))
for i, month in enumerate(months):
    mdf = monthly_df[monthly_df['Month'] == month]
    top5g = mdf.nlargest(5, 'Monthly_Return')
    top5l = mdf.nsmallest(5, 'Monthly_Return')
    combined = pd.concat([top5g, top5l]).sort_values('Monthly_Return')
    colors = ['green' if x > 0 else 'red' for x in combined['Monthly_Return']]
    axes[i].barh(combined['Ticker'], combined['Monthly_Return'], color=colors)
    axes[i].set_title(f'{month} - Top 5 Gainers and Losers')
    axes[i].set_xlabel('Monthly Return (%)')
    axes[i].axvline(0, color='black', linewidth=0.8)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'chart5_monthly_gainers_losers.png'))
plt.close()
print("Chart 5 saved.")

print("\nAll analysis complete! Check charts folder.")