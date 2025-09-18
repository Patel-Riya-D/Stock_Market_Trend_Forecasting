import yfinance as yf
import numpy as np
import pandas as pd
import re
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import plotly.graph_objects as go

def predict_lstm(ticker, forecast_days=30):
    df = yf.Ticker(ticker).history(period='2y')
    close = df['Close'].dropna().values.reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(close)

    # Prepare training data
    X, y = [], []
    for i in range(60, len(scaled)):
        X.append(scaled[i-60:i, 0])
        y.append(scaled[i, 0])
    X = np.array(X).reshape(-1, 60, 1)
    y = np.array(y).reshape(-1, 1)

    # Define model and load weights
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(60, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # ✅ Sanitize filename
    sanitized_ticker = re.sub(r'\W+', '', ticker.lower())
    model.load_weights(f"models/{sanitized_ticker}_weights.h5")

    # Predict training data (for evaluation)
    preds = model.predict(X)
    inv_preds = scaler.inverse_transform(preds)
    inv_y = scaler.inverse_transform(y)

    # Metrics
    mae = mean_absolute_error(inv_y, inv_preds)
    rmse = np.sqrt(mean_squared_error(inv_y, inv_preds))
    accuracy = 100 - (mae / np.mean(inv_y)) * 100
    metrics = {"accuracy": accuracy, "mae": mae, "rmse": rmse}

    # Forecast
    last_sequence = scaled[-60:].reshape(1, 60, 1)
    future_predictions = []
    for _ in range(forecast_days):
        next_pred = model.predict(last_sequence)[0]
        future_predictions.append(next_pred[0])
        last_sequence = np.append(last_sequence[:, 1:, :], [[[next_pred[0]]]], axis=1)

    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()
    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=forecast_days)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index[-200:], y=inv_y.flatten()[-200:], name="Historical",
        line=dict(color='white')
    ))
    fig.add_trace(go.Scatter(
        x=future_dates, y=future_predictions,
        name="Forecast", line=dict(color='orange')
    ))
    fig.update_layout(title=f"{ticker} — LSTM Forecast",
                      xaxis_title="Date", yaxis_title="Price",
                      template="plotly_dark", height=450)

    trend = "Expected to rise 📈" if future_predictions[-1] > future_predictions[0] else "Might fall 📉"

    return fig, metrics, trend, inv_y.flatten().tolist(), inv_preds.flatten().tolist()
