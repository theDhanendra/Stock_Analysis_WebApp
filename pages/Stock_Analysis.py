import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
from pages.utils.patched_lib.squeeze_pro import squeeze_pro
from pages.utils.plotly_figure import plotly_table, close_chart, candlestick, RSI, Moving_average, MACD

# Setting page config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="page_with_curl",
    layout="wide",
)

def display_header():
    st.title("Stock Analysis")

def get_user_inputs():
    col1, col2, col3 = st.columns(3)
    today = datetime.date.today()
    with col1:
        ticker = st.text_input("Stock Ticker", "TSLA")
    with col2:
        start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
    with col3:
        end_date = st.date_input("Choose End Date", datetime.date(today.year, today.month, today.day))
    return ticker, start_date, end_date

def display_stock_info(ticker):
    stock = yf.Ticker(ticker)
    st.subheader(ticker)
    st.write(f"##### {stock.info['longBusinessSummary']}")
    st.write("**Sector:**", stock.info['sector'])
    st.write("#### **Full Time Employees:**", stock.info['fullTimeEmployees'])
    st.write("#### **Website:**", stock.info['website'])

def display_metrics(stock):
    col1, col2 = st.columns(2)
    with col1:
        df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
        df[''] = [stock.info['marketCap'], stock.info['beta'], stock.info['trailingEps'], stock.info['trailingPE']]
        fig_df = plotly_table(df)
        st.plotly_chart(fig_df, use_container_width=True)

    with col2:
        df = pd.DataFrame(index=('Quick Ratio', 'Revenue per share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'))
        df[''] = [stock.info["quickRatio"], stock.info["revenuePerShare"], stock.info["profitMargins"], stock.info["debtToEquity"], stock.info["returnOnEquity"]]
        fig_df = plotly_table(df)
        st.plotly_chart(fig_df, use_container_width=True)

def fetch_stock_data(ticker, start_date, end_date):
    with st.spinner("Fetching stock data..."):
        data = yf.download(ticker, start=start_date, end=end_date)
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]  # Flatten or rename columns
        data.index = data.index.date
    return data

def display_daily_change(data):
    col1, col2, col3 = st.columns(3)
    daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    col1.metric("Daily Change", str(round(data['Close'].iloc[-1],2)), str(round(daily_change,2)))

def display_historical_data(data):
    if len(data) >= 10:
        last_10_df = data.tail(10).sort_index(ascending=False).round(3)
        fig_df = plotly_table(last_10_df)
        st.write('##### Historical Data (Last 10 Days)')
        st.plotly_chart(fig_df, use_container_width=True)
    else:
        st.error("Not enough data to display the last 10 days.")

def get_selected_period():
    period_mapping = {'5D': '5d', '1M': '1mo', '6M': '6mo', 'YTD': 'ytd', '1Y': '1y', '5Y': '5y', 'MAX': 'max'}
    col_labels = list(period_mapping.keys())
    cols = st.columns([1] * len(col_labels))
    num_period = ''
    for label, col in zip(col_labels, cols):
        if col.button(label):
            num_period = period_mapping[label]
    return num_period

def display_charts(ticker, num_period, chart_type, indicators):
    ticker_ = yf.Ticker(ticker)
    data1 = ticker_.history(period='max').reset_index()
    if num_period == '':
        period = '1y'
    else:
        period = num_period

    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1, period), use_container_width=True)
        st.plotly_chart(RSI(data1, period), use_container_width=True)
    elif chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1, period), use_container_width=True)
        st.plotly_chart(MACD(data1, period), use_container_width=True)
    elif chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(data1, period), use_container_width=True)
        st.plotly_chart(RSI(data1, period), use_container_width=True)
    elif chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(data1, period), use_container_width=True)
    elif chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(data1, period), use_container_width=True)
        st.plotly_chart(MACD(data1, period), use_container_width=True)

# Main execution
display_header()
ticker, start_date, end_date = get_user_inputs()
display_stock_info(ticker)
stock = yf.Ticker(ticker)
display_metrics(stock)
data = fetch_stock_data(ticker, start_date, end_date)
display_daily_change(data)
display_historical_data(data)
num_period = get_selected_period()
col1, col2, col3 = st.columns([1,1,4])
with col1:
    chart_type = st.selectbox('',('Candle','Line'))
with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('', ('RSI', 'MACD'))
    else:
        indicators = st.selectbox('',('RSI', 'Moving Average', 'MACD'))
display_charts(ticker, num_period, chart_type, indicators)
