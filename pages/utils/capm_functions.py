import plotly.express as px
import pandas as pd
import numpy as np
from scipy.stats import linregress

def interactive_plot(df):
    """
    Creates an interactive Plotly line chart for the given dataframe.

    Parameters:
    df (pd.DataFrame): DataFrame containing stock data with a 'Date' column.

    Returns:
    fig (plotly.graph_objects.Figure): Plotly figure object for the interactive line chart.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    fig = px.line()
    for col in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[col], name=col)
    fig.update_layout(width=800, height=500, margin=dict(t=50, b=20),
                      legend=dict(orientation='h', yanchor='bottom', xanchor='right', x=1, y=1.02))
    return fig

def normalize(df):
    """
    Normalizes the prices in the dataframe.

    Parameters:
    df (pd.DataFrame): DataFrame containing stock data with a 'Date' column.

    Returns:
    df (pd.DataFrame): DataFrame with normalized prices.
    """
    df = df.copy()
    df.iloc[:, 1:] = df.iloc[:, 1:].div(df.iloc[0, 1:]).sub(1)
    return df

def daily_return(df):
    """
    Calculates daily returns of the stocks in the dataframe.

    Parameters:
    df (pd.DataFrame): DataFrame containing stock data with a 'Date' column.

    Returns:
    df (pd.DataFrame): DataFrame with daily returns.
    """
    df_daily_return = df.copy()
    df_daily_return.iloc[:, 1:] = df.iloc[:, 1:].pct_change().mul(100).fillna(0)
    return df_daily_return

def calculate_beta_alpha(stocks_daily_return):
    """
    Calculates beta and alpha values for given stocks' daily returns.

    Parameters:
    stocks_daily_return (pd.DataFrame): DataFrame containing daily returns of stocks.

    Returns:
    beta (dict): Dictionary containing beta values of stocks.
    alpha (dict): Dictionary containing alpha values of stocks.
    """
    beta = {}
    alpha = {}
    for stock in stocks_daily_return.columns:
        if stock != 'Date' and stock != 'sp500':
            slope, intercept, _, _, _ = linregress(stocks_daily_return['sp500'], stocks_daily_return[stock])
            beta[stock] = slope
            alpha[stock] = intercept
    return beta, alpha

def calculate_r_squared(sp500_returns, stock_returns):
    """
    Calculates the R-squared value for the stock returns compared to SP500 returns.

    Parameters:
    sp500_returns (pd.Series): Series containing daily returns of SP500.
    stock_returns (pd.Series): Series containing daily returns of a stock.

    Returns:
    r_squared (float): R-squared value.
    """
    slope, intercept, r_value, p_value, std_err = linregress(sp500_returns, stock_returns)
    return r_value**2
