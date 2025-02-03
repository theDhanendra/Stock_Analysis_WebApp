import os
import requests
import streamlit as st
import yfinance as yf
from dotenv import load_dotenv

# Set Page Config
st.set_page_config(
    page_title="Investment Portal",
    page_icon="📈",
    layout="wide"
)

def display_header():
    st.title("Welcome to the Ultimate Investment Portal 📈")
    st.subheader("Empowering Your Investment Journey with Real-Time Insights and Tools")
    st.image("app.jpg")
    st.markdown("---")

# Load API Key from .env file
load_dotenv() 
API_KEY = os.getenv("NEWS_API_KEY")

# ✅ Cache News API data to avoid multiple requests
@st.cache_data
def fetch_news_ticker():
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        news = response.json().get("articles", [])
        news_items = [
            (
                article.get("title", "No Title"),
                article.get("url", "#"),
                article.get("urlToImage", ""),
                article.get("description", ""),
                article.get("publishedAt", "")[:10]  # YYYY-MM-DD
            )
            for article in news[:6]  # Limiting to 6 articles
        ]
        return news_items
    return []

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
                            <img src="{thumbnail}" width="300" style="border-radius:5px;">
                            <h4><a href="{url}" target="_blank">{title}</a></h4>
                            <p><em>{date}</em></p>
                            <p>{description}</p>
                        </div>
                        """, unsafe_allow_html=True
                    )
    else:
        st.warning("No news available at the moment.")

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
    ]
    for service in services:
        st.markdown(f"#### {service['icon']} {service['title']}")
        st.markdown(f"{service['description']}")

    st.markdown("---")


# ✅ Cache stock data to avoid multiple API calls
@st.cache_data
def fetch_featured_stocks():
    tickers = ["TSLA", "AAPL", "AMZN"]
    stock_data = yf.download(tickers, period="1d")["Close"]

    featured_stocks = {}
    for ticker in tickers:
        close_price = stock_data[ticker].iloc[0] if ticker in stock_data else "N/A"
        stock_info = yf.Ticker(ticker).info
        featured_stocks[ticker] = {
            "price": f"${close_price:.2f}" if close_price != "N/A" else "N/A",
            "description": stock_info.get("shortName", "No description available"),
            "market_cap": f"{stock_info.get('marketCap', 'N/A'):,}" if stock_info.get("marketCap") else "N/A",
            "volume": f"{stock_info.get('volume', 'N/A'):,}" if stock_info.get("volume") else "N/A",
            "url": f"https://finance.yahoo.com/quote/{ticker}",
        }
    return featured_stocks

def display_featured_stocks():
    st.markdown("### Featured Stocks 🏆")
    featured_stocks = fetch_featured_stocks()
    cols = st.columns(len(featured_stocks))  # Dynamic columns
    for col, (ticker, info) in zip(cols, featured_stocks.items()):
        col.markdown(
            f"""
            <div style="border:2px solid #ddd; padding:10px; margin-bottom:10px; border-radius:5px;">
                <h4>{ticker} - {info['description']}</h4>
                <p><strong>Current Price:</strong> {info['price']}</p>
                <p><strong>Market Cap:</strong> {info['market_cap']}</p>
                <p><strong>Volume:</strong> {info['volume']}</p>
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
