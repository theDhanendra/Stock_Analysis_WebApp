import os
import requests
import streamlit as st
import yfinance as yf
from dotenv import load_dotenv

os.system('sh /mount/src/stock_analysis_webapp/modify_squeeze_pro.sh')


# Set Page Config
st.set_page_config(
    page_title="Investment Portal",
    page_icon="chart_with_upwards_trend",
    layout="wide"
)

def display_header():
    st.title("Welcome to the Ultimate Investment Portal :chart_with_upwards_trend:")
    st.subheader("Empowering Your Investment Journey with Real-Time Insights and Tools")
    st.image("app.jpg")

    st.markdown("---")

# Load API Key from .env file
load_dotenv() 
API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news_ticker():
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        news = response.json()["articles"]
        news_items = []
        for article in news[:6]:  # Limiting to 6 articles for a 2x3 collage
            title = article['title']
            url = article['url']
            thumbnail = article['urlToImage']
            description = article['description'] if article['description'] else ""
            date = article['publishedAt'][:10]  # Extracting the date (YYYY-MM-DD)
            news_items.append((title, url, thumbnail, description, date))
        return news_items
    return 

def display_news_ticker():
    st.markdown("### Latest Financial News 📰")
    news_items = fetch_news_ticker()
    if news_items:
        for i in range(0, len(news_items), 2):
            cols = st.columns(2)  # Create 2 columns
            for col, item in zip(cols, news_items[i:i+2]):
                title, url, thumbnail, description, date = item
                with col:
                    st.markdown(
                        f"""
                        <div style="border:2px solid #ddd; padding:10px; margin-bottom:10px; border-radius:5px;">
                            <img src="{thumbnail}" width="300" style="float:right; margin-right:15px; border-radius:5px;">
                            <h4><a href="{url}" target="_blank">{title}</a></h4>
                            <br>Date: <em>{date}</em></br>
                            <p>{description}</p>
                        </div>
                        """, unsafe_allow_html=True
                    )
    else:
        st.markdown("No news available at the moment.")

    st.markdown("---")

def display_services():
    st.markdown("### Our Comprehensive Services 🚀")
    services = [
        {
            "title": "Detailed Stock Information",
            "description": "Gain access to in-depth details about various stocks, including sector classifications, number of employees, daily price fluctuations, and more.",
            "icon": "📊"
        },
        {
            "title": "Stock Price Prediction",
            "description": "Utilize advanced forecasting models and historical data analysis to predict future closing prices for the next 30 days. Stay ahead with accurate predictions.",
            "icon": "🔮"
        },
        {
            "title": "CAPM Expected Return",
            "description": "Calculate the expected return of stocks using the Capital Asset Pricing Model (CAPM). Understand the risk-return tradeoff for better investment decisions.",
            "icon": "📈"
        },
        {
            "title": "CAPM Beta Calculation",
            "description": "Determine the Beta value and Expected Return for individual stocks to evaluate their risk-adjusted returns. Make informed decisions with precise data.",
            "icon": "📉"
        },
        {
            "title": "Market Insights",
            "description": "Stay updated with the latest market trends, news, and insights. Access real-time data and analysis to make well-informed investment choices.",
            "icon": "🌐"
        },
        {
            "title": "Portfolio Management",
            "description": "Manage your investment portfolio with ease. Monitor performance, assess risk, and optimize your holdings for maximum returns.",
            "icon": "📁"
        }
    ]

    for service in services:
        st.markdown(f"#### {service['icon']} {service['title']} :")
        st.write(f"##### {service['description']}")

    st.markdown("---")

def fetch_featured_stocks():
    # List of tickers to fetch
    tickers = ['TSLA', 'AAPL', 'AMZN']
    trending_stocks = yf.Tickers(tickers)
    stock_data = trending_stocks.history(period='1d')

    featured_stocks = {}
    for ticker in tickers:
        close_price = stock_data['Close'][ticker].iloc[0]
        stock_info = yf.Ticker(ticker).info
        short_description = stock_info.get('shortName', 'No description available')
        market_cap = f"{stock_info.get('marketCap', 'N/A'):,}"  # Adding commas
        volume = f"{stock_info.get('volume', 'N/A'):,}"  # Adding commas
        more_info_url = f"https://finance.yahoo.com/quote/{ticker}"

        featured_stocks[ticker] = {
            'price': f"{close_price:.2f}",
            'description': short_description,
            'market_cap': market_cap,
            'volume': volume,
            'url': more_info_url
        }

    return featured_stocks

def display_featured_stocks():
    st.markdown("### Featured Stocks 🏆")
    featured_stocks = fetch_featured_stocks()
    # Creating a single row with three columns for featured stocks
    cols = st.columns(3)
    for col, (stock, info) in zip(cols, featured_stocks.items()):
        col.markdown(
            f"""
            <div style="border:2px solid #ddd; padding:10px; margin-bottom:10px; border-radius:5px;">
                <h4>{stock} - {info['description']}</h4>
                <table style="width:100%">
                    <tr>
                        <td><strong>Current Price:</strong></td>
                        <td>${info['price']}</td>
                    </tr>
                    <tr>
                        <td><strong>Market Cap:</strong></td>
                        <td>${info['market_cap']}</td>
                    </tr>
                    <tr>
                        <td><strong>Volume:</strong></td>
                        <td>{info['volume']}</td>
                    </tr>
                </table>
                <a href="{info['url']}" target="_blank">More Info</a>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown("---")
    
def display_footer():
    st.markdown("---")
    st.markdown("### Explore More")
    st.write("Dive into each section for valuable insights and tools to make informed investment decisions. Let's achieve financial success together!")

# Display components
display_header()
display_news_ticker()
display_services()
display_featured_stocks()
display_footer()
