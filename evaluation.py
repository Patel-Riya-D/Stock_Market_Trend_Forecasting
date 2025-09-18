import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def show():
    st.subheader("📊 Model Evaluation")

    # === LSTM Chart ===
    if "lstm_eval" in st.session_state:
        actual = st.session_state["lstm_eval"]["actual"]
        predicted = st.session_state["lstm_eval"]["predicted"]

        df = pd.DataFrame({
            "Day": list(range(1, len(actual)+1)),
            "Actual": actual,
            "Predicted": predicted
        })

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Day"], y=df["Actual"], mode='lines+markers',
                                 name='Actual', line=dict(color='#ffffff')))
        fig.add_trace(go.Scatter(x=df["Day"], y=df["Predicted"], mode='lines+markers',
                                 name='Predicted', line=dict(color='#0dcaf0')))
        fig.update_layout(
            title="Predicted vs Actual — LSTM",
            height=350,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color='white'),
            xaxis_title="Time",
            yaxis_title="Price"
        )
        st.plotly_chart(fig, use_container_width=True)

    # === ARIMA Chart ===
    if "arima_eval" in st.session_state:
        actual = st.session_state["arima_eval"]["actual"]
        predicted = st.session_state["arima_eval"]["predicted"]

        df = pd.DataFrame({
            "Day": list(range(1, len(actual)+1)),
            "Actual": actual,
            "Predicted": predicted
        })

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Day"], y=df["Actual"], mode='lines+markers',
                                 name='Actual', line=dict(color='#ffffff')))
        fig.add_trace(go.Scatter(x=df["Day"], y=df["Predicted"], mode='lines+markers',
                                 name='Predicted', line=dict(color='orange')))
        fig.update_layout(
            title="Predicted vs Actual — ARIMA",
            height=350,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color='white'),
            xaxis_title="Time",
            yaxis_title="Price"
        )
        st.plotly_chart(fig, use_container_width=True)

    # === LSTM Metrics ===
    if "lstm_metrics" in st.session_state:
        m = st.session_state["lstm_metrics"]
        st.markdown(f"""<div class="card" style="margin-top:1rem;">
            <h4>📈 LSTM Performance</h4>
            <div class="metric-line">Accuracy: <span class="pill">{m['accuracy']:.2f}%</span></div>
            <div class="metric-line">MAE: <span class="pill">{m['mae']:.2f}</span> | RMSE: <span class="pill">{m['rmse']:.2f}</span></div>
        </div>""", unsafe_allow_html=True)

    # === ARIMA Metrics ===
    if "arima_metrics" in st.session_state:
        a = st.session_state["arima_metrics"]
        st.markdown(f"""<div class="card" style="margin-top:1rem;">
            <h4>📉 ARIMA Performance</h4>
            <div class="metric-line">Accuracy: <span class="pill">{a['accuracy']:.2f}%</span></div>
            <div class="metric-line">MAE: <span class="pill">{a['mae']:.2f}</span> | RMSE: <span class="pill">{a['rmse']:.2f}</span></div>
        </div>""", unsafe_allow_html=True)

    if not any(k in st.session_state for k in ["lstm_eval", "lstm_metrics", "arima_eval", "arima_metrics"]):
        st.info("📭 No evaluation data available yet. Please run a forecast first.")
