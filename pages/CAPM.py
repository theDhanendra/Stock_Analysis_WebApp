import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import plotly.express as px
from pages.utils import capm_functions

def main():
    st.set_page_config(page_title="CAPM", page_icon="📈", layout="wide")
    st.title("Capital Asset Pricing Model")

    stocks_list, year = get_user_input()
    if not stocks_list or not year:
        st.error("Please select valid input for stocks and number of years.")
        return

    try:
        with st.spinner("Downloading data..."):
            stocks_df, SP500 = download_data(stocks_list, year)
        if stocks_df is None or SP500 is None:
            return
        
        display_dataframes(stocks_df, SP500)
        plot_prices(stocks_df)
        stocks_daily_return = capm_functions.daily_return(stocks_df)
        display_beta_and_return(stocks_daily_return, stocks_list)
    except Exception as e:
        st.error(f"An error occurred: {e}")

def get_user_input():
    col1, col2 = st.columns([1, 1])
    with col1:
        stocks_list = st.multiselect("Choose 4 stocks", ['TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA',   
     'GOOGL', 'FB', 'INTC', 'CSCO', 'PYPL', 'ADBE', 'CMCSA', 'PEP', 'KO', 'V', 'MA', 'T', 'PFE',  'MRNA', 'ASML', 'NKE', 'AMD', 'CRM', 'NFLX',   
     'HON', 'IBM', 'QCOM', 'TXN', 'SBUX', 'ZM', 'BABA', 'ORCL', 'WMT', 'LMT', 'BA', 'AVGO', 'CAT', 'MDT', 'COST', 'CVX', 'XOM', 'TGT',    
     'PAYC', 'MCO', 'SPGI', 'UNH', 'MDLZ', 'DHR', 'TROW', 'NOW', 'LRCX', 'ATVI', 'CHKP', 'WBA',  
     'SYK', 'TMO', 'ISRG', 'ADP', 'AON', 'NDAQ'], ['TSLA', 'AAPL', 'AMZN'])
    with col2:
        year = st.number_input("Number of years", 1, 10)
    return stocks_list, year

def download_data(stocks_list, year):
    try:
        end = datetime.date.today()
        start = datetime.date.today() - datetime.timedelta(days=365 * year)
        SP500 = yf.download('^GSPC', start=start, end=end)

        stocks_df = pd.DataFrame()
        for stock in stocks_list:
            stock_data = yf.download(stock, start=start, end=end)
            stocks_df[stock] = stock_data['Close']

        stocks_df.reset_index(inplace=True)
        SP500.reset_index(inplace=True)
        SP500 = SP500[['Date', 'Close']]
        SP500.columns = ['Date', 'sp500']
        stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
        SP500['Date'] = pd.to_datetime(SP500['Date'])

        stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')
        return stocks_df, SP500
    except Exception as e:
        st.error(f"An error occurred while downloading data: {e}")
        return None, None

def display_dataframes(stocks_df, SP500):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("## Dataframe head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("## Dataframe tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

def plot_prices(stocks_df):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Price of all the Stocks")
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))
    with col2:
        st.markdown("### Price of all the Stocks (After Normalizing)")
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))

def display_beta_and_return(stocks_daily_return, stocks_list):
    beta, alpha = capm_functions.calculate_beta_alpha(stocks_daily_return)
    beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Calculated Beta Value')
        st.dataframe(beta_df, use_container_width=True)

    rf = 0
    rm = stocks_daily_return['sp500'].mean() * 252
    return_df = pd.DataFrame()
    return_value = [str(round(rf + (value * (rm - rf)), 2)) for stock, value in beta.items()]
    return_df['Stock'] = stocks_list
    return_df['Return Value'] = return_value

    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.dataframe(return_df, use_container_width=True)

    # Additional Metrics (Example: R-squared)
    r_squared = {stock: capm_functions.calculate_r_squared(stocks_daily_return['sp500'], stocks_daily_return[stock]) for stock in stocks_list}
    r_squared_df = pd.DataFrame(list(r_squared.items()), columns=['Stock', 'R-squared'])
    
    st.markdown('### Additional Metrics')
    st.dataframe(r_squared_df, use_container_width=True)

if __name__ == '__main__':
    main()
