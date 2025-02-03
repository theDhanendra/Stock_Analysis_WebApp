import streamlit as st
import yfinance as yf  
from statsmodels.tsa.stattools import adfuller  
from sklearn.metrics import mean_squared_error  
from statsmodels.tsa.arima.model import ARIMA  
import numpy as np  
from sklearn.preprocessing import StandardScaler  
from datetime import datetime, timedelta  
import pandas as pd  

# Cache stock data to prevent multiple API calls
@st.cache_data
def get_data(ticker):  
    stock_data = yf.download(ticker, start="2024-01-01")  
    return stock_data["Close"] if "Close" in stock_data else pd.Series()

def stationary_check(close_price):  
    adf_test = adfuller(close_price)  
    return round(adf_test[1], 3)  

def get_rolling_mean(close_price):  
    return close_price.rolling(window=7).mean().dropna()  

def get_differencing_order(close_price):  
    d = 0  
    while stationary_check(close_price) > 0.05:  
        d += 1  
        close_price = close_price.diff().dropna()  
    return d  

# Cache model training to prevent repeated computations
@st.cache_resource
def train_arima_model(data, differencing_order):  
    model = ARIMA(data, order=(5, differencing_order, 5))  # Optimized order (5, d, 5)
    return model.fit()

def fit_model(data, differencing_order):  
    model_fit = train_arima_model(data, differencing_order)  
    forecast = model_fit.get_forecast(steps=30)  
    return forecast.predicted_mean

def evaluate_model(original_price, differencing_order):  
    train_data, test_data = original_price[:-30], original_price[-30:]  
    predictions = fit_model(train_data, differencing_order)  
    return round(np.sqrt(mean_squared_error(test_data, predictions)), 2)  

def scaling(close_price):  
    scaler = StandardScaler()  
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))  
    scaler_params = {"mean": scaler.mean_[0], "scale": scaler.scale_[0]}  # ✅ Convert scaler to a dictionary  
    return scaled_data, scaler_params  

# Fix: Convert scaler to a dictionary so it can be cached
@st.cache_resource
def train_and_forecast(scaled_data, differencing_order, scaler_params):  
    rmse = evaluate_model(scaled_data, differencing_order)
    forecast = get_forecast(scaled_data, differencing_order)
    forecast["Close"] = inverse_scaling(scaler_params, forecast["Close"])
    return rmse, forecast

def get_forecast(original_price, differencing_order):  
    predictions = fit_model(original_price, differencing_order)  
    forecast_index = pd.date_range(start=datetime.now(), periods=30, freq="D")  
    return pd.DataFrame(predictions, index=forecast_index, columns=["Close"])  

# Fix: Perform inverse scaling using scaler parameters instead of `StandardScaler` object
def inverse_scaling(scaler_params, scaled_data):  
    return (scaled_data * scaler_params["scale"]) + scaler_params["mean"]
