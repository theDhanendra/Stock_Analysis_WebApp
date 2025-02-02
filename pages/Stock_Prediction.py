import streamlit as st  
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling  
import pandas as pd  
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast  
from pages.utils.patched_lib.squeeze_pro import squeeze_pro

st.set_page_config(  
    page_title="Stock Prediction",  
    page_icon="chart_with_downwards_trend",  
    layout="wide",  
)  

st.title("Stock Prediction")  
col1, col2, col3 = st.columns(3)  

with col1:  
    ticker = st.text_input('Stock Ticker', 'AAPL')  

rmse = 0  

try:
    st.subheader('Predicting Next 30 days Close Price for: ' + ticker)  
    close_price = get_data(ticker)
    
    # Check if close_price data is empty
    if close_price.empty:
        st.error("No data found for ticker symbol: " + ticker)
    else:
        # Format the datetime
        close_price.index = close_price.index.strftime('%d-%m-%Y')

        # Debugging: Print the first few rows of the close_price data
        close_price_table = plotly_table(close_price.sort_index(ascending=True).round(3))
        close_price_table.update_layout(height=220)  
        
        rolling_price = get_rolling_mean(close_price)  
        differencing_order = get_differencing_order(rolling_price)  
        scaled_data, scaler = scaling(rolling_price)  
        rmse = evaluate_model(scaled_data, differencing_order)
        
        st.write("Model RMSE Score:", rmse)  
        
        forecast = get_forecast(scaled_data, differencing_order)  
        
        forecast['Close'] = inverse_scaling(scaler, forecast['Close'])  
        
        # Format the datetime
        forecast.index = forecast.index.strftime('%d-%m-%Y')
        
        # Display Forecast Data in a smaller size
        forecast_table = plotly_table(forecast.sort_index(ascending=True).round(3))
        forecast_table.update_layout(height=220)  
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("#### Close Price Data")
            st.plotly_chart(close_price_table, use_container_width=True)
        with col2:
            st.write("#### Forecast Data (Next 30 days)")
            st.plotly_chart(forecast_table, use_container_width=True)
        
        forecast = pd.concat([rolling_price, forecast])  
                
        st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width=True)
except Exception as e:
    st.error(f"An error occurred: {e}")
