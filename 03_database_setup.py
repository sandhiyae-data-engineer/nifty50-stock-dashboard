import pymysql
import pandas as pd
import os
import glob

# database connection details
HOST = "localhost"
USER = "root"
PASSWORD = "root123"
DATABASE = "stock_db"

# step 1 - create database
conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS stock_db")
cursor.execute("USE stock_db")
print("Database created successfully!")

# step 2 - create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(20),
    date DATE,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    volume BIGINT,
    month VARCHAR(10)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS market_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(20),
    start_price FLOAT,
    end_price FLOAT,
    yearly_return FLOAT,
    volatility FLOAT,
    avg_price FLOAT,
    avg_volume FLOAT
)
""")

conn.commit()
print("Tables created successfully!")

# step 3 - upload stock prices data
BASE_DIR = r"C:\Users\sandh\Desktop\stock_project"
CSV_DIR = os.path.join(BASE_DIR, "csv_output")
all_files = glob.glob(os.path.join(CSV_DIR, "*.csv"))

print(f"\nUploading {len(all_files)} stock files to MySQL...")

for file in all_files:
    ticker = os.path.basename(file).replace(".csv", "")
    df = pd.read_csv(file, parse_dates=['Date'])

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO stock_prices 
            (ticker, date, open_price, high_price, low_price, close_price, volume, month)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            ticker,
            str(row['Date'].date()),
            float(row['Open']),
            float(row['High']),
            float(row['Low']),
            float(row['Close']),
            int(row['Volume']),
            str(row['Month'])
        ))

    conn.commit()
    print(f"Uploaded: {ticker}")

# step 4 - upload market summary data
summary_file = os.path.join(BASE_DIR, "market_summary.csv")
summary_df = pd.read_csv(summary_file)

for _, row in summary_df.iterrows():
    cursor.execute("""
        INSERT INTO market_summary
        (ticker, start_price, end_price, yearly_return, volatility, avg_price, avg_volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        str(row['Ticker']),
        float(row['Start_Price']),
        float(row['End_Price']),
        float(row['Yearly_Return']),
        float(row['Volatility']),
        float(row['Avg_Price']),
        float(row['Avg_Volume'])
    ))

conn.commit()
print("\nMarket summary uploaded!")

# step 5 - verify data
cursor.execute("SELECT COUNT(*) FROM stock_prices")
count1 = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM market_summary")
count2 = cursor.fetchone()[0]

print(f"\nstock_prices table  : {count1} rows")
print(f"market_summary table: {count2} rows")
print("\nDatabase setup complete!")

cursor.close()
conn.close()