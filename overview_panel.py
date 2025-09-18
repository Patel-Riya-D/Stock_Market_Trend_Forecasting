# overview_panel.py
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from pathlib import Path

def get_index_change(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d")
        if len(data) < 2:
            return None
        prev = data["Close"].iloc[-2]
        latest = data["Close"].iloc[-1]
        change = ((latest - prev) / prev) * 100
        return round(change, 2)
    except:
        return None

def style_pct(val):
    if val is None:
        return "<span style='color:#aaa;'>N/A</span>"
    color = "#28e07c" if val > 0 else "#ff5f5f" if val < 0 else "#f1c40f"
    return f"<span style='color:{color};'>{val:+.2f}%</span>"

def show():
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.08); padding: 10px 15px; border-radius: 10px; margin-bottom: 25px; text-align:center; font-weight:500; font-size:14px;'>
        🌍 NASDAQ {style_pct(get_index_change("^IXIC"))} &nbsp;&nbsp; | 
        S&P 500 {style_pct(get_index_change("^GSPC"))} &nbsp;&nbsp; | 
        Sensex {style_pct(get_index_change("^BSESN"))}
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📦 Stock Overview")

    tickers = {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "GOOGL": "Alphabet",
        "AMZN": "Amazon",
        "META": "Meta",
        "TSLA": "Tesla",
        "NVDA": "NVIDIA",
        "TCS.NS": "TCS",
        "ADBE": "Adobe",
        "ORCL": "Oracle"  # Note: FMP may not support NSE stocks
    }

    cols = st.columns(3)

    for i, (symbol, name) in enumerate(tickers.items()):
        with cols[i % 3]:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="3mo")
                info = ticker.info

                close = hist["Close"].dropna()
                if len(close) < 30:
                    continue

                latest = close[-1]
                prev = close[-2]
                pct = round((latest - prev) / prev * 100, 2)

                signal = "🟢 BUY" if pct > 1 else "🔴 SELL" if pct < -1 else "🟡 HOLD"
                pe = info.get("trailingPE", "N/A")
                beta = info.get("beta", "N/A")
                cap = info.get("marketCap", "N/A")
                rating = info.get("recommendationKey", "N/A").upper()

                logo_path = Path("styles/logos") / f"{symbol}.png"
                if logo_path.exists():
                    st.image(str(logo_path), width=60)

                currency = st.session_state.get("currency", "USD")
                if symbol.endswith(".NS") and currency == "INR":
                    price_str = f"₹{latest:.2f}"
                else:
                    if currency == "INR":
                        latest *= 87.56  # Fixed INR conversion
                        price_str = f"₹{latest:.2f}"
                    else:
                        price_str = f"${latest:.2f}"

                st.markdown(f"""
                    <div class="card">
                        <div class="card-content">
                            <h4 style="margin-bottom:0.4rem;">{symbol} — {name}</h4>
                            <div class="stock-price-line">
                                <span class="price">{price_str} <span style="color: #f46d75;">({pct:+.2f}%)</span></span>
                                <span class="signal">{signal}</span>
                            </div>
                            <div class="metrics-row">
                                <span class="metric-pill">P/E: {round(pe, 2) if pe != 'N/A' else pe}</span>
                                <span class="metric-pill">Beta: {round(beta, 2) if beta != 'N/A' else beta}</span>
                                <span class="metric-pill">Cap: {round(cap/1e12, 2)}T</span>
                            </div>
                            <div class="metrics-row" style="margin-top: 6px;">
                                <span class="metric-pill rating-pill">🧠 Rating: {rating}</span>
                            </div>
                """, unsafe_allow_html=True)

                with st.container():
                    st.markdown("<div class='chart-block'>", unsafe_allow_html=True)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=close.index[-30:], y=close[-30:],
                        mode="lines+markers",
                        line=dict(color="#0dcaf0", width=3),
                        marker=dict(size=4, color="#0dcaf0"),
                        hovertemplate="%{y:.2f} on %{x|%b %d}"
                    ))
                    fig.update_layout(
                        height=140,
                        margin=dict(l=0, r=0, t=10, b=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(visible=True),
                        yaxis=dict(visible=True)
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=f"{symbol}_chart")
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Clean gauge chart with only one value and better label
                    gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=pct,
                        number={"suffix": "%"},
                        title={"text": "% Daily Change", "font": {"size": 14}},
                        gauge={
                            "axis": {"range": [-10, 10]},
                            "bar": {"color": "#0dcaf0"},
                            "steps": [
                                {"range": [-10, -2], "color": "#ffb3b3"},
                                {"range": [-2, 2], "color": "#fff2b2"},
                                {"range": [2, 10], "color": "#b2f2bb"},
                            ],
                            "threshold": {
                                "line": {"color": "red", "width": 4},
                                "thickness": 0.75,
                                "value": pct,
                            },
                        }
                    ))
                    gauge.update_layout(
                        height=180,
                        margin=dict(t=20, b=10, l=10, r=10),
                        template="plotly_dark",
                        font=dict(color="#ffffff")
                    )
                    st.plotly_chart(gauge, use_container_width=True)

                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"{symbol}: {e}")
