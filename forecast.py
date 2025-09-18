import streamlit as st
import yfinance as yf
from predictor import predict_lstm
from arima_model import run_arima

def show():
    st.subheader("📈 Stock Forecast")

    stock = st.selectbox("Select Stock", ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "ADBE", "ORCL", "TCS.NS"], key="forecast_stock")
    df = yf.Ticker(stock).history(period="2y")

    if df.empty or "Close" not in df.columns or df["Close"].dropna().empty:
        st.warning(f"⚠️ No valid data for {stock}")
        st.stop()

    model_type = st.radio("Choose Forecasting Model:", ["LSTM", "ARIMA"], horizontal=True, key="model_radio")

    st.markdown(f"<div class='model-badge'>Model: {model_type}</div>", unsafe_allow_html=True)
    st.markdown(f"### 📈 Forecast using {model_type} Model")

    if model_type == "LSTM":
        try:
            fig, metrics, trend, y_true, y_pred = predict_lstm(stock)
            st.plotly_chart(fig, use_container_width=True)
            st.success(f"📊 AI Summary: {trend}")

            if metrics:
                st.session_state["lstm_metrics"] = metrics
                st.session_state["lstm_eval"] = {"actual": y_true, "predicted": y_pred}
                st.markdown(f"""
                <div class='model-metrics'>
                    <strong>Accuracy:</strong> {metrics['accuracy']:.2f}%<br>
                    <strong>MAE:</strong> {metrics['mae']:.2f}<br>
                    <strong>RMSE:</strong> {metrics['rmse']:.2f}
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ LSTM error: {e}")

    elif model_type == "ARIMA":
        try:
            fig, accuracy, mae, rmse, y_true, y_pred = run_arima(stock)
            st.plotly_chart(fig, use_container_width=True)

            if accuracy is not None:
                st.session_state["arima_metrics"] = {
                    "accuracy": accuracy,
                    "mae": mae,
                    "rmse": rmse
                }
                st.session_state["arima_eval"] = {
                    "actual": y_true,
                    "predicted": y_pred
                }
                st.markdown(f"""
                <div class='model-metrics'>
                    <strong>Accuracy:</strong> {accuracy:.2f}%<br>
                    <strong>MAE:</strong> {mae:.2f}<br>
                    <strong>RMSE:</strong> {rmse:.2f}
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ ARIMA error: {e}")
