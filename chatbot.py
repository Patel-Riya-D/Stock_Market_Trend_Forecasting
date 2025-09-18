import streamlit as st
from groq import Groq
from streamlit_chat import message
import yfinance as yf

client = Groq(api_key=st.secrets["groq"]["api_key"])

# ✅ Helper: fetch stock price
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            return round(data["Close"].iloc[-1], 2)
    except:
        return None
    return None

def show():
    st.title("💬 Ask Alvi — Stock Assistant")

    st.markdown("""
    <div class='chat-desc'>
        <ul>
            <li>📈 Stock predictions</li>
            <li>📊 RSI / Moving Averages</li>
            <li>📰 Company info / News impact</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask about stock forecast, indicators, etc...")

    # Show chat history
    for i, msg in enumerate(st.session_state.chat_history):
        is_user = msg["role"] == "user"
        message(msg["content"], is_user=is_user, key=str(i))

    if user_input:
        # Add user input
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        message(user_input, is_user=True, key=str(len(st.session_state.chat_history)-1))

        bot_reply = None
        with st.spinner("✍️ AIvi is typing..."):

            # ✅ Step 1: Check if query is about stock price
            keywords = ["price", "stock", "today", "closing", "current"]
            tickers = {"netflix": "NFLX", "meta": "META", "apple": "AAPL",
                       "microsoft": "MSFT", "google": "GOOGL", "amazon": "AMZN","nvidia": "NVDA"}

            matched_ticker = None
            for name, symbol in tickers.items():
                if name in user_input.lower():
                    matched_ticker = symbol
                    break

            if any(word in user_input.lower() for word in keywords) and matched_ticker:
                price = get_stock_price(matched_ticker)
                if price:
                    bot_reply = f"📊 The latest closing price of **{matched_ticker}** is **${price}**."
                else:
                    bot_reply = f"⚠️ Sorry, I couldn’t fetch {matched_ticker}'s price right now."

            # ✅ Step 2: Otherwise, send query to LLaMA model
            if not bot_reply:
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=st.session_state.chat_history + [
                            {"role": "system", "content": "Reply briefly in 2-3 lines. Be conversational and helpful."}
                        ],
                        temperature=0.7,
                    )
                    bot_reply = response.choices[0].message.content.strip()

                except Exception as e:
                    bot_reply = f"❌ AIvi Error: {e}"

        # Save assistant reply
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        message(bot_reply, is_user=False, key=str(len(st.session_state.chat_history)-1))
