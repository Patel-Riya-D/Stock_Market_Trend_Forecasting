import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np

def show():
    st.subheader("📉 Technical Indicators")

    stock = st.selectbox("Choose Stock", ["AAPL", "MSFT", "GOOGL", "AMZN", "META","NVDA", "TSLA", "ADBE", "ORCL", "TCS.NS"], key="indicator_stock")
    ticker = yf.Ticker(stock)
    df = ticker.history(period="6mo")

    if df.empty or "Close" not in df.columns or df["Close"].dropna().empty:
        st.warning(f"⚠️ No valid data for {stock}")
        return

    df["MA20"] = df["Close"].rolling(20).mean()
    std = df["Close"].rolling(20).std()
    df["Upper"] = df["MA20"] + 2 * std
    df["Lower"] = df["MA20"] - 2 * std
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = np.where(avg_loss == 0, 0, avg_gain / avg_loss)
    df["RSI"] = 100 - (100 / (1 + rs))
    df["MACD"] = df["Close"].ewm(span=12, adjust=False).mean() - df["Close"].ewm(span=26, adjust=False).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close", line=dict(color="cyan")))
    fig.add_trace(go.Scatter(x=df.index, y=df["MA20"], name="MA20", line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=df.index, y=df["Upper"], name="Upper Band", line=dict(color="gray", dash="dot")))
    fig.add_trace(go.Scatter(x=df.index, y=df["Lower"], name="Lower Band", line=dict(color="gray", dash="dot")))
    fig.update_layout(title=f"{stock} - Bollinger Bands", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 RSI & MACD")
    st.line_chart(df[["RSI", "MACD"]])
