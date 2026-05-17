import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import glob

# page config
st.set_page_config(
    page_title="Nifty 50 Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# paths
BASE_DIR = r"C:\Users\sandh\Desktop\stock_project"
CSV_DIR = os.path.join(BASE_DIR, "csv_output")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

# load market summary
@st.cache_data
def load_summary():
    return pd.read_csv(os.path.join(BASE_DIR, "market_summary.csv"))

@st.cache_data
def load_stock(ticker):
    path = os.path.join(CSV_DIR, f"{ticker}.csv")
    df = pd.read_csv(path, parse_dates=['Date'])
    return df.sort_values('Date')

summary_df = load_summary()

# title
st.title("📈 Nifty 50 Stock Performance Dashboard")
st.markdown("**Full Year Analysis — 2023 to 2024**")
st.divider()

# top metrics
col1, col2, col3, col4 = st.columns(4)
green = len(summary_df[summary_df['Yearly_Return'] > 0])
red   = len(summary_df[summary_df['Yearly_Return'] <= 0])
col1.metric("Total Stocks", "50")
col2.metric("Green Stocks 🟢", green)
col3.metric("Red Stocks 🔴", red)
col4.metric("Avg Price", f"₹{summary_df['Avg_Price'].mean():.0f}")

st.divider()

# sidebar
st.sidebar.title("🔍 Filters")
selected_ticker = st.sidebar.selectbox(
    "Select a Stock",
    sorted(summary_df['Ticker'].tolist())
)

# tab layout
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 Top Stocks",
    "📊 Stock Detail",
    "🔥 Volatility",
    "📈 Cumulative Return",
    "🗺️ Correlation"
])

# tab 1 - top stocks
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 Top 10 Green Stocks")
        top10g = summary_df.nlargest(10, 'Yearly_Return')[['Ticker', 'Yearly_Return']]
        fig = px.bar(top10g, x='Ticker', y='Yearly_Return',
                     color='Yearly_Return', color_continuous_scale='Greens',
                     title="Top 10 Best Performing Stocks")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🔴 Top 10 Red Stocks")
        top10r = summary_df.nsmallest(10, 'Yearly_Return')[['Ticker', 'Yearly_Return']]
        fig = px.bar(top10r, x='Ticker', y='Yearly_Return',
                     color='Yearly_Return', color_continuous_scale='Reds_r',
                     title="Top 10 Worst Performing Stocks")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 All Stocks Summary Table")
    display_df = summary_df.copy()
    display_df['Status'] = display_df['Yearly_Return'].apply(
        lambda x: '🟢 Green' if x > 0 else '🔴 Red'
    )
    st.dataframe(display_df.sort_values('Yearly_Return', ascending=False),
                 use_container_width=True)

# tab 2 - stock detail
with tab2:
    st.subheader(f"📊 {selected_ticker} — Stock Price History")
    stock_df = load_stock(selected_ticker)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=stock_df['Date'],
        open=stock_df['Open'],
        high=stock_df['High'],
        low=stock_df['Low'],
        close=stock_df['Close'],
        name=selected_ticker
    ))
    fig.update_layout(title=f"{selected_ticker} Candlestick Chart",
                      xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    stock_info = summary_df[summary_df['Ticker'] == selected_ticker].iloc[0]
    col1.metric("Start Price", f"₹{stock_info['Start_Price']}")
    col1.metric("End Price",   f"₹{stock_info['End_Price']}")
    col2.metric("Yearly Return", f"{stock_info['Yearly_Return']}%")
    col2.metric("Volatility",    f"{stock_info['Volatility']:.4f}")

# tab 3 - volatility
with tab3:
    st.subheader("🔥 Top 10 Most Volatile Stocks")
    top_vol = summary_df.nlargest(10, 'Volatility')
    fig = px.bar(top_vol, x='Ticker', y='Volatility',
                 color='Volatility', color_continuous_scale='Oranges',
                 title="Top 10 Volatile Stocks")
    st.plotly_chart(fig, use_container_width=True)

# tab 4 - cumulative return
with tab4:
    st.subheader("📈 Cumulative Return — Top 5 Stocks")
    top5 = summary_df.nlargest(5, 'Yearly_Return')['Ticker'].tolist()
    fig = go.Figure()
    for ticker in top5:
        df = load_stock(ticker)
        df['Daily_Return']      = df['Close'].pct_change()
        df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Cumulative_Return'] * 100,
            name=ticker, mode='lines'
        ))
    fig.update_layout(title="Cumulative Return (%)",
                      xaxis_title="Date", yaxis_title="Return (%)")
    st.plotly_chart(fig, use_container_width=True)

# tab 5 - correlation
with tab5:
    st.subheader("🗺️ Stock Price Correlation Heatmap")
    st.image(os.path.join(CHARTS_DIR, "chart4_correlation.png"),
             use_container_width=True)

st.divider()
st.caption("Built with Streamlit | Nifty 50 Stock Analysis Project")