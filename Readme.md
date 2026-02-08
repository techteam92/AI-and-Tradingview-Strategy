# 🧭 Kraken API Trading & Trend Prediction [Project ID: P-12334]

A FastAPI-based service that integrates with the Kraken API for balance checks and order execution, and uses AI-driven trend prediction (XGBoost, seasonal decomposition, divergence detection) to guide buy/sell decisions.

---

## 📚 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Screenshots](#-screenshots)
- [API Documentation](#-api-documentation)
- [Contact](#-contact)
- [Acknowledgements](#-acknowledgements)

---

## 🧩 About

This project provides a lightweight API for interacting with Kraken (balance, orders) and automates trading logic using trend signals. It fetches market data (via Binance for SOL/USDT), decomposes the series into trend/seasonal/residual components, forecasts with XGBoost and SARIMAX, and detects bullish/bearish divergences to trigger or exit positions. The goal is to combine Kraken execution with a simple, transparent trend-following strategy.

---

## ✨ Features

- **Balance API** – Get Kraken account balance (e.g. USDT) via authenticated endpoint.
- **Order execution** – Create market buy/sell orders on Kraken with signed API requests.
- **Trend prediction** – Long/Short and divergence signals from moving averages and slope comparison (actual vs predicted).
- **Data pipeline** – Binance klines → seasonal decomposition → XGBoost + SARIMAX forecasting.
- **Divergence detection** – Bearish/Bullish divergence triggers for exit or position adjustment.
- **FastAPI server** – REST endpoints for balance and order creation, ready for integration or dashboards.

---

## 🧠 Tech Stack

| Category   | Technologies |
|-----------|--------------|
| **Languages** | Python 3.x |
| **Frameworks** | FastAPI |
| **APIs** | Kraken REST API, Binance API |
| **Data / ML** | pandas, NumPy, XGBoost, statsmodels (SARIMAX, seasonal_decompose) |
| **Tools** | python-dotenv, Pydantic, uvicorn |

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Kraken_test-main.git

# Navigate to the project directory
cd Kraken_test-main

# Create and activate a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/macOS

# Install dependencies
pip install fastapi uvicorn python-dotenv pydantic pandas numpy xgboost statsmodels python-binance
```

---

## 🚀 Usage

```bash
# Start the API server
uvicorn main:app --reload
```

Then open your browser or use a client:

👉 **API docs:** [http://localhost:8000/docs](http://localhost:8000/docs)  
👉 **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧾 Configuration

Create a `.env` file in the project root with your Kraken API credentials:

```env
# User / balance (user.py, main.py balance endpoint)
USER_PUBLIC_KEY=your_kraken_public_key
USER_PRIVATE_KEY=your_kraken_private_key

# Orders (order.py, main.py create order)
ORDER_PUBLIC_KEY=your_kraken_public_key
ORDER_PRIVATE_KEY=your_kraken_private_key

# Optional: if reusing same keys elsewhere
PUBLIC_KEY=your_kraken_public_key
PRIVATE_KEY=your_kraken_private_key
```

For AI/data (Binance klines in `AI/data_collection.py`), set API key/secret in code or via env if you add support:

```env
BINANCE_API_KEY=your_binance_key
BINANCE_API_SECRET=your_binance_secret
```

---

## 🖼 Screenshots

Add demo images, GIFs, or UI preview screenshots here.

*Example: API docs (Swagger), sample balance/order response, or chart of trend/forecast.*

---

## 📜 API Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/user/balance` | Get account balance (e.g. USDT). |
| **POST** | `/order/create/` | Create a market order. Body: `{ "pair": "SOLUSDT", "type": "buy" \| "sell", "volume": "0.1" }`. |

**Order logic (handled in backend):**

- Buy when trend is Long; sell when trend is Short.
- Exit buy on `exit_buy` or Bearish divergence; exit sell on `exit_sell` or Bullish divergence.

---

## 📬 Contact

| | |
|---|---|
| **Email** | 100terry001@gmail.com |
| **GitHub** | [https://github.com/techteam92](https://github.com/techteam92) |
| **Whatsapp** | +1 (343) 512-7592 |

---

## 🌟 Acknowledgements

- [Kraken API](https://docs.kraken.com/rest/) for exchange integration.
- [Binance API](https://python-binance.readthedocs.io/) for kline data in the AI pipeline.
- [FastAPI](https://fastapi.tiangolo.com/), [XGBoost](https://xgboost.readthedocs.io/), [statsmodels](https://www.statsmodels.org/) for API and forecasting.

---

*Last updated: May 2025*

