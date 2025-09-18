import streamlit as st
import overview_panel
import forecast
import indicators
import news_panel
import evaluation
import chatbot
import market_panel

def load_css():
    try:
        with open("styles/style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Could not load style.css: {e}")

def footer():
    st.markdown("""
        <hr style="margin-top: 2rem; margin-bottom: 0.5rem;">
        <div style='text-align: center; padding: 10px 0; font-size: 14px; color: #bbb;'>
            🛠️ Crafted with ❤️ by <strong>Riya Patel</strong> • Driven by <strong>AI</strong>
        </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="📈 Tracker — AI Stock Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    load_css()

    st.markdown("""
        <div class="tracker-title">
            <div class="tracker-title-text">📈 Tracker — <span class="faint-subtitle">AI Stock Dashboard</span></div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.title("🌐 Navigation")
    tab = st.sidebar.selectbox("Choose a section", [
        "📦 Overview",
        "📈 Forecast",
        "📉 Indicators",
        "📰 News",
        "📊 Evaluation",
        "🚨 Market Pulse",
        "💬 Ask AI"
    ])

    # Currency selector
    st.sidebar.markdown("### 💱 Currency")
    currency = st.sidebar.radio("Display prices in", ["USD", "INR"], horizontal=True)
    st.session_state.currency = currency

    try:
        if tab == "📦 Overview":
            overview_panel.show()
        elif tab == "📈 Forecast":
            forecast.show()
        elif tab == "📉 Indicators":
            indicators.show()
        elif tab == "📰 News":
            news_panel.show()
        elif tab == "📊 Evaluation":
            evaluation.show()
        elif tab == "🚨 Market Pulse":
            market_panel.show()
        elif tab == "💬 Ask AI":
            chatbot.show()
    except Exception as e:
        st.error(f"🚨 Error loading '{tab}' panel:")
        st.exception(e)

    footer()

if __name__ == "__main__":
    main()
