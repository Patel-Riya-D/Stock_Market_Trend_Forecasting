import streamlit as st
import feedparser
import yfinance as yf
import random

def get_tag_emoji(title):
    title = title.lower()
    if "ai" in title:
        return "🤖"
    if "oil" in title or "energy" in title:
        return "🛢"
    if "bank" in title or "finance" in title:
        return "💰"
    if "stock" in title or "market" in title or "share" in title:
        return "📈"
    if "inflation" in title:
        return "📉"
    return random.choice(["🔍", "💹", "🔮"])

def spotlight_stock():
    stocks = {
        "NFLX": "Netflix",
        "IBM": "IBM",
        "INTC": "Intel",
        "PYPL": "PayPal",
        "BA": "Boeing",
        "UBER": "Uber",
        "SBUX": "Starbucks",
        "SHOP": "Shopify"
    }
    symbol, name = random.choice(list(stocks.items()))
    try:
        info = yf.Ticker(symbol).info
        price = info.get("currentPrice", "N/A")
        cap = info.get("marketCap", "N/A")
        sector = info.get("sector", "N/A")
        rating = info.get("recommendationKey", "N/A").upper()
        cap_text = f"{round(cap / 1e9, 1)}B" if isinstance(cap, (int, float)) else cap

        return {
            "symbol": symbol,
            "name": name,
            "price": price,
            "cap": cap_text,
            "sector": sector,
            "rating": rating
        }
    except:
        return None

def show():
    st.subheader("📰 Market News", anchor=False)

    # Spotlight section first
    st.markdown("### 🌟 In the Spotlight")
    spotlight = spotlight_stock()
    if spotlight:
        st.markdown(f"""
        <div class='card' style='margin:10px 0;padding:12px;background:rgba(0,245,212,0.05);border-left:4px solid #00f5d4;border-radius:10px;'>
            <h4>🚀 {spotlight['name']} ({spotlight['symbol']})</h4>
            <ul>
                <li>💰 Price: ${spotlight['price']}</li>
                <li>🏢 Sector: {spotlight['sector']}</li>
                <li>💼 Market Cap: {spotlight['cap']}</li>
                <li>📊 Analyst Rating: {spotlight['rating']}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠ Could not fetch spotlight stock info.")

    st.markdown("### 📢 Trending Headlines")
    feed = feedparser.parse("https://finance.yahoo.com/news/rssindex")

    for entry in feed.entries[:6]:
        title = entry.title
        published = entry.published
        link = entry.link
        tag = get_tag_emoji(title)

        st.markdown(f"""
            <div class="news-card" style="margin-bottom:1rem;padding:10px;border-left:5px solid #0dcaf0;background:rgba(255,255,255,0.02);border-radius:10px;">
                <h4>{tag} {title}</h4>
                <p style="font-size:13px; color:#bbb;">🕒 {published}</p>
                <a href="{link}" target="_blank" style="color:#0dcaf0;">🔗 Read More</a>
            </div>
        """, unsafe_allow_html=True)

    #st.markdown("---")
    #st.info("📅 News may include updates from 12th & 10th July (not always real-time)")