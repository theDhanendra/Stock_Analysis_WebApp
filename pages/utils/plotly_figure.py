import plotly.graph_objects as go
import datetime
import pandas as pd
import pandas_ta as pta
from dateutil.relativedelta import relativedelta
import plotly.express as px

def plot_stock_chart(df):
    sampled_df = df.iloc[::5]  # Every 5th data point
    fig = px.line(sampled_df, x=sampled_df.index, y="Close")
    return fig


def plotly_table(dataframe):
    """
    Create a Plotly table for given dataframe.
    """
    headerColor = 'grey'
    rowEvenColor = '#F8FAFD'
    rowOddColor = '#E0EFFF'
    

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b></b>"]+["<b>"+str(i)[:10]+"</b>" for i in dataframe.columns],
            line_color='#0078ff', fill_color='#0078ff',
            align='center', font=dict(color='white', size=15), height=35,
        ),
        cells=dict(
            values=[["<b>" + str(i) + "</b>" for i in dataframe.index]] + [dataframe[i] for i in dataframe.columns],
            fill_color=[
                [rowOddColor if i % 2 == 0 else rowEvenColor for i in range(len(dataframe))]
            ] * (len(dataframe.columns) + 1),
            align='center', line_color='white', font=dict(color="black", size=15)
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig

def filter_data(dataframe, num_period):
    """
    Filter dataframe based on the selected time period.
    """
    if not isinstance(dataframe.index, pd.DatetimeIndex):
        dataframe.index = pd.to_datetime(dataframe.index)
    
    if num_period == '1mo':
        date = dataframe.index[-1] + relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1)
    else:
        date = dataframe.index[0]

    return dataframe[dataframe.index > date]

def create_scatter_chart(dataframe, column_names, title):
    """
    Create a scatter chart for given dataframe and columns.
    """
    fig = go.Figure()
    for column in column_names:
        fig.add_trace(go.Scatter(
            x=dataframe['Date'], y=dataframe[column],
            mode='lines', name=column, line=dict(width=2)
        ))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500, margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white', paper_bgcolor='#e0efff',
        title=title,
        legend=dict(xanchor='right', yanchor='top')
    )
    return fig

def close_chart(dataframe, num_period=False):
    """
    Create a close chart with Open, Close, High, Low prices.
    """
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    column_names = ['Open', 'Close', 'High', 'Low']
    return create_scatter_chart(dataframe, column_names, "Close Chart")

def candlestick(dataframe, num_period):
    """
    Create a candlestick chart for given dataframe and period.
    """
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dataframe['Date'], open=dataframe['Open'], high=dataframe['High'],
        low=dataframe['Low'], close=dataframe['Close'], name='Candlestick'
    ))
    fig.update_layout(
        showlegend=True, height=500, margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white', paper_bgcolor='#e0f7fa',
        legend=dict(
            x=0, y=1, xanchor='left', yanchor='top',
            traceorder='normal', bgcolor='#e0f7fa',
            bordercolor='#444', borderwidth=1
        )
    )
    return fig

def RSI(dataframe, num_period):
    """
    Create an RSI chart for given dataframe and period.
    """
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe.RSI, name='RSI',
        marker_color='orange', line=dict(width=2, color='orange')
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=[70] * len(dataframe), name='Overbought',
        marker_color='red', line=dict(width=2, color='red', dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=[30] * len(dataframe), name='Oversold',
        marker_color='#79da84', line=dict(width=2, color='#79da84', dash='dash'),
        fill='tonexty'
    ))
    fig.update_layout(
        yaxis_range=[0, 100], height=200,
        plot_bgcolor='white', paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation='h', xanchor='right', x=1, yanchor='top')
    )
    return fig

def Moving_average(dataframe, num_period):
    """
    Create a moving average chart for given dataframe and period.
    """
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], length=50)
    dataframe = filter_data(dataframe, num_period)
    column_names = ['Open', 'Close', 'High', 'Low', 'SMA_50']
    return create_scatter_chart(dataframe, column_names, "Moving Average Chart")

def MACD(dataframe, num_period):
    """
    Create an MACD chart for given dataframe and period.
    """
    macd_values = pta.macd(dataframe['Close'], fast=12, slow=26, signal=9)
    dataframe['MACD'] = macd_values['MACD_12_26_9']
    dataframe['Signal Line'] = macd_values['MACDs_12_26_9']
    dataframe['Histogram'] = macd_values['MACDh_12_26_9']
    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['MACD'], name='MACD',
        line=dict(width=2, color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Signal Line'], name='Signal Line',
        line=dict(width=2, color='orange', dash='dash')
    ))
    fig.add_trace(go.Bar(
        x=dataframe['Date'], y=dataframe['Histogram'], name='Histogram',
        marker_color=['green' if h > 0 else 'red' for h in dataframe['Histogram']]
    ))
    fig.update_layout(
        height=500, plot_bgcolor='white', paper_bgcolor='#e0f7fa',
        margin=dict(l=0, r=20, t=20, b=0), legend=dict(orientation="h")
    )
    return fig

def Moving_average_forecast(forecast):
    """
    Create a moving average forecast chart for the given forecast.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast.index[-30:], y=forecast['Close'].iloc[-30:],
        mode='lines', name='Close Price', line=dict(width=2, color='black')
    ))
    fig.add_trace(go.Scatter(
        x=forecast.index[-31:], y=forecast['Close'].iloc[-31:],
        mode='lines', name='Future Close Price', line=dict(width=2, color='red')
    ))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white',
        paper_bgcolor='#E0FFFF', legend=dict(yanchor="top", xanchor="right")
    )
    return fig