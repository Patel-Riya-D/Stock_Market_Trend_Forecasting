# 📈 AI – Powered Stock Market Trend Forecasting Using LSTM and Real-Time Analytics

## 📌 Overview
This project presents an **AI-powered stock market forecasting dashboard** that combines **deep learning (LSTM)**, **statistical ARIMA**, and **real-time analytics** to predict stock price movements.  
It integrates **technical indicators (RSI, MACD, Bollinger Bands)**, **sentiment analysis**, and an **AI chatbot powered by LLaMA3 & Groq API** for interactive user queries.

The system aims to support **investors, analysts, and traders** in making informed decisions using **real-time data visualization** and **predictive modeling**.

---

## ✨ Features
- 📊 **LSTM & ARIMA Forecasting**  
  Predicts short-term closing prices of major stocks like Apple, Microsoft, Google, Amazon, etc.

- 📉 **Technical Indicators**  
  Includes RSI, MACD, and Bollinger Bands for trend and momentum analysis.

- 📰 **Sentiment & News Analysis**  
  Uses real-time financial news and sentiment scoring to improve prediction reliability.

- 📌 **Interactive Streamlit Dashboard**  
  - **Overview Panel** → Company info & stock fundamentals  
  - **Forecast Panel** → Animated stock prediction graphs  
  - **Indicators Panel** → RSI, MACD, Bollinger Bands  
  - **News Panel** → Live news feed with sentiment analysis  
  - **Market Pulse** → Sector performance & top gainers/losers  
  - **Ask AI (AIvi Assistant)** → Natural chatbot powered by Groq API  

---

## 🤖 AIvi — Your Personal Stock Assistant  

One of the most unique features of this dashboard is **AIvi**, an intelligent stock assistant chatbot powered by **Groq API + LLaMA3**.  

💡 **What AIvi can do for you:**  
- Answer natural questions about **stocks, forecasts, and indicators**.  
- Provide quick insights on **RSI, MACD, and moving averages**.  
- Summarize **latest news** and its impact on stock price.  
- Help you decide whether to **BUY, SELL, or HOLD** a stock.  
- Respond in **real-time**, like a virtual financial advisor.  

📸 *Demo:*  
![AIvi Assistant Screenshot](assets/chatbot_demo.png)  

> 🛠️ **Tech Note**: Unlike a rule-based chatbot, AIvi is powered by **LLaMA 3.1 + Groq**, ensuring **natural conversations** with real-time market data from Yahoo Finance and Finnhub.  

---

## ⚙️ System Architecture
- **Data Collection** → Yahoo Finance API (yfinance)  
- **Preprocessing** → Missing value handling, MinMax scaling  
- **Forecast Models** → LSTM & ARIMA hybrid approach  
- **Dashboard** → Streamlit app for visualization  
- **Chatbot** → Groq API with LLaMA3 for natural queries  
- **Evaluation** → Metrics like MSE, RMSE, MAE, MAPE  

---

## 🏗️ LSTM Model Architecture
1. **Input Layer** → Sequential stock price data  
2. **LSTM Layer 1** → 50 units, return sequences = True  
3. **LSTM Layer 2** → 50 units, return sequences = False  
4. **Dense Layer** → Fully connected, 1 unit  
5. **Output Layer** → Predicts next closing price  

---

## 📊 Results
- ✅ **LSTM consistently outperforms ARIMA** in terms of RMSE and MAE across volatile stocks.  
- ✅ Technical indicators improve interpretability.  
- ✅ Sector analysis + sentiment tracking provides **context-aware insights**.  
- ⚠️ ARIMA still performs well for **stable stocks** with predictable trends.  

---

## 🚀 Future Scope
- 🔮 Use advanced models like **Transformers** and hybrid AI approaches.  
- 📡 Add multimodal data (macroeconomic indicators, global events).  
- ⚡ Deploy with continuous **real-time streaming predictions**.  
- 🔍 Improve explainability & trust in AI predictions.  
- 🌍 Expand to **cryptocurrency and global indices**.  

---

## 📂 Tech Stack
- **Python** (NumPy, Pandas, Scikit-learn)  
- **Deep Learning** → TensorFlow / Keras (LSTM models)  
- **Statistics** → ARIMA, SARIMA  
- **Data APIs** → yfinance, Finnhub, Groq API  
- **Visualization** → Plotly, Matplotlib  
- **Dashboard** → Streamlit  
- **Chatbot** → LLaMA3 + Groq API  

---

## 📜 References
- [yfinance](https://pypi.org/project/yfinance/)  
- [Streamlit](https://streamlit.io/)  
- [Plotly](https://plotly.com/python/)  
- [Groq API](https://groq.com/)  

---

## 👩‍💻 Authors
- **Riya Patel** 
  
📧 Contact: `riya20.surat@gmail.com`
# Stock_Market_Trend_Forecasting
