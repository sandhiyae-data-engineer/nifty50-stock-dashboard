import yaml
import pandas as pd
import os
import glob

BASE_DIR = r"C:\Users\sandh\Desktop\stock_project"
OUTPUT_DIR = os.path.join(BASE_DIR, "csv_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

yaml_files = glob.glob(os.path.join(BASE_DIR, "2024-*", "*.yaml"))
print(f"Total YAML files found: {len(yaml_files)}")

all_stocks = {}

for yaml_file in yaml_files:
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        if data is None:
            continue
        for record in data:
            ticker = record.get('Ticker', '')
            if not ticker:
                continue
            if ticker not in all_stocks:
                all_stocks[ticker] = []
            all_stocks[ticker].append({
                'Date': record.get('date', ''),
                'Open': record.get('open', 0),
                'High': record.get('high', 0),
                'Low': record.get('low', 0),
                'Close': record.get('close', 0),
                'Volume': record.get('volume', 0),
                'Month': record.get('month', '')
            })
    except Exception as e:
        print(f"Error: {yaml_file}: {e}")

print(f"Total stocks found: {len(all_stocks)}")

for ticker, records in all_stocks.items():
    df = pd.DataFrame(records)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    csv_path = os.path.join(OUTPUT_DIR, f"{ticker}.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved: {ticker}.csv — {len(df)} rows")

print("Done! Check csv_output folder.")