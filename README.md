# 📈 Nifty 50 Stock Performance Dashboard

## Project Overview
A comprehensive stock market analysis dashboard for Nifty 50 stocks using Python, MySQL, and Streamlit.

## Features
- 📊 Top 10 Green & Red Stocks Analysis
- 🔥 Volatility Analysis
- 📈 Cumulative Return Charts
- 🏭 Sector-wise Performance
- 🗺️ Stock Correlation Heatmap
- 📅 Monthly Gainers & Losers

## Tech Stack
- **Python** — Data processing & analysis
- **Pandas** — Data manipulation
- **MySQL** — Database storage
- **Streamlit** — Interactive dashboard
- **Plotly** — Charts & visualizations

## Project Structure


stock_project/
├── 01_extract_yaml_to_csv.py  # YAML to CSV extraction
├── 02_analysis.py             # Data analysis & charts
├── 03_database_setup.py       # MySQL database setup
├── 04_streamlit_app.py        # Streamlit dashboard
├── market_summary.csv         # Market summary data
└── Sector_data - Sheet1.csv   # Sector information


## How to Run

### Step 1: Install dependencies
```bash
pip install pandas numpy matplotlib seaborn streamlit sqlalchemy pymysql pyyaml plotly openpyxl
```

### Step 2: Extract YAML to CSV
```bash
python 01_extract_yaml_to_csv.py
```

### Step 3: Run Analysis
```bash
python 02_analysis.py
```

### Step 4: Setup Database
```bash
python 03_database_setup.py
```

### Step 5: Launch Dashboard
```bash
streamlit run 04_streamlit_app.py
```

## Dashboard Preview
- Total Stocks: 50
- Green Stocks: 38
- Red Stocks: 12
- Average Price: ₹2544

## Results
- 50 CSV files generated (one per stock)
- 11,150 rows stored in MySQL
- 5 interactive charts
- Real-time Streamlit dashboard


