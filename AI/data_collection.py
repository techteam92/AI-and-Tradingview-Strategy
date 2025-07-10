from binance.client import Client
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from AI.xgforecast import forecast  # Your custom forecast function
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf

# --- Binance API setup ---
client = Client(api_key='', api_secret='')

klines = client.get_klines(symbol='SOLUSDT', interval=Client.KLINE_INTERVAL_30MINUTE, limit=300)

kline_keys = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume'
]

parsed_klines = []
for kline in klines:
    kline_dict = dict(zip(kline_keys, kline[:11]))
    kline_dict['open_time'] = pd.to_datetime(kline_dict['open_time'], unit='ms')
    kline_dict['close_time'] = pd.to_datetime(kline_dict['close_time'], unit='ms')
    for key in ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']:
        kline_dict[key] = float(kline_dict[key])
    kline_dict['number_of_trades'] = int(kline_dict['number_of_trades'])
    parsed_klines.append(kline_dict)

df = pd.DataFrame(parsed_klines)
df.set_index('open_time', inplace=True)

close_series = df['close']

def perform_decomposition(series, period):
    try:
        decomposition = seasonal_decompose(series, model='additive', period=period)
        return decomposition
    except ValueError as e:
        print(f"Seasonal decomposition error: {e}")
        return None
# Example: Decompose 1-minute data with period = 60 (hourly seasonality)
# Requires at least 120 data points (2 full cycles)
decomposition_1min = perform_decomposition(close_series, period=48)

def pred_function():
    if decomposition_1min:
        # Extract components and drop NaN values where necessary
        trend = decomposition_1min.trend.dropna()
        seasonal = decomposition_1min.seasonal  # usually no NaN
        resid = decomposition_1min.resid.dropna()

        # Calculate time difference between last valid trend and seasonal values (in minutes)
        trend_last_time = trend.index[-1]
        seasonal_last_time = seasonal.index[-1]
        difference = (trend_last_time - seasonal_last_time) / pd.Timedelta(minutes=30)
        p = 1  # AR term
        d = 1  # Differencing
        q = 1  # MA term
        P = 1  # Seasonal AR term
        D = 1  # Seasonal differencing
        Q = 1  # Seasonal MA term
        s = 12  # Number of periods in each season

        # Forecasting
        steps = int(30 - difference)
        trend_pred, trend_mae = forecast(trend, steps)
        seasonal_model = SARIMAX(close_series, order=(p, d, q), seasonal_order=(P, D, Q, s)).fit()
        fitted_values = seasonal_model.fittedvalues
        seasonal_pred, seasonal_mae = forecast(fitted_values,steps)

        resid_pred, noise_mae = forecast(resid, steps)

        diff_int = int(difference)
        n = min(len(trend_pred), len(seasonal_pred))
        trend_arr = np.array(trend_pred[-n:])
        seasonal_arr = np.array(seasonal_pred[-n:])
        pred = trend_arr * seasonal_mae/(seasonal_mae+trend_mae) + seasonal_arr * trend_mae/(seasonal_mae+trend_mae)

        last_time = df.index[-1]               # Last observed timestamp
        num_pred = len(pred)                   # Number of predicted values
        freq = pd.Timedelta(minutes=30)         # 30-minute frequency

        # Generate the datetime index for predictions
        pred_times = pd.date_range(start=last_time + freq, periods=num_pred, freq=freq)
        # plt.figure(figsize=(12, 6))
        # # plt.plot(df.index, df['close'], label='Actual Close Price')
        # plt.plot(pred_times, pred, label='Forecast', color='red')
        # plt.title('SOLUSDT Close Price and Forecast')
        # plt.xlabel('Datetime')
        # plt.ylabel('Close Price')
        # plt.legend()
        # plt.show()
        return pred, close_series
    else:
        print("Decomposition failed. Not enough data or invalid parameters.")
