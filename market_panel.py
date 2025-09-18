import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.express as px

# Sector ETF symbols
SECTOR_TICKERS = {
    'Technology': 'XLK',
    'Healthcare': 'XLV',
    'Financials': 'XLF',
    'Energy': 'XLE',
    'Consumer Discretionary': 'XLY',
    'Utilities': 'XLU',
    'Industrials': 'XLI',
    'Materials': 'XLB',
    'Real Estate': 'XLRE',
    'Consumer Staples': 'XLP',
    'Communication Services': 'XLC'
}

def get_sector_change():
    data = []
    for sector, ticker in SECTOR_TICKERS.items():
        df = yf.Ticker(ticker).history(period="2d")
        if len(df) >= 2:
            change = ((df['Close'][-1] - df['Close'][-2]) / df['Close'][-2]) * 100
            data.append({"Sector": sector, "Change (%)": round(change, 2)})
    df_change = pd.DataFrame(data).sort_values(by="Change (%)", ascending=False).reset_index(drop=True)
    return df_change

def get_5d_data():
    data = []
    for sector, ticker in SECTOR_TICKERS.items():
        df = yf.Ticker(ticker).history(period="6d")
        if len(df) >= 5:
            change = ((df['Close'][-1] - df['Close'][0]) / df['Close'][0]) * 100
            data.append({"Sector": sector, "5D % Change": round(change, 2)})
    return pd.DataFrame(data)

def show():
    st.markdown("## 🔥 Sector Trend Watch")

    # Apply custom CSS for gradient cards
    st.markdown("""
        <style>
        .gradient-card {
            padding: 1rem;
            border-radius: 15px;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        .card-title {
            font-weight: bold;
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    df = get_sector_change()

    # 🔺 Top Gainers
    top3 = df.head(3)
    top_html = "<div class='gradient-card'><div class='card-title'>🔺 Top 3 Sectors Up</div>"
    for _, row in top3.iterrows():
        top_html += f"<div>{row['Sector']}: <b>{row['Change (%)']}%</b></div>"
    top_html += "</div>"
    st.markdown(top_html, unsafe_allow_html=True)

    # 🔻 Top Losers
    bottom3 = df.tail(3).sort_values(by="Change (%)")
    bottom_html = "<div class='gradient-card'><div class='card-title'>🔻 Top 3 Sectors Down</div>"
    for _, row in bottom3.iterrows():
        bottom_html += f"<div>{row['Sector']}: <b>{row['Change (%)']}%</b></div>"
    bottom_html += "</div>"
    st.markdown(bottom_html, unsafe_allow_html=True)

    # 📊 Normal Bar Chart (No Change)
    #st.markdown("### 📊 Sector Performance Bar Chart")
    #st.bar_chart(df.set_index("Sector")["Change (%)"])

    # 📉 Modern 5-Day Performance Graph
    st.markdown("### 📉 5-Day Performance of Sectors")
    df_5d = get_5d_data()
    fig = px.bar(
        df_5d,
        x="Sector",
        y="5D % Change",
        color="5D % Change",
        color_continuous_scale="bluered",
        template="plotly_dark",
        title="",
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        margin=dict(t=10, b=40),
        coloraxis_colorbar=dict(title="5D % Change"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ⏰ Last Updated
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
        <div class='gradient-card'>
            <div class='card-title'>⏰ Last Updated</div>
            <div>{now}</div>
        </div>
    """, unsafe_allow_html=True)

    # 🧠 AI Insight (Simple static logic)
    leader = top3.iloc[0]['Sector']
    insight = f"""
    <div class='gradient-card'>
        <div class='card-title'>🧠 AI Insight</div>
        {leader} sector is leading the market today, likely due to positive sentiment and strong earnings signals.
    </div>
    """
    st.markdown(insight, unsafe_allow_html=True)
