from AI.data_collection import pred_function
import numpy as np

def trend_prediction():
    pred_calculation, close_series = pred_function()

    print(pred_calculation)

    min_predArray = min(pred_calculation)
    max_predArray = max(pred_calculation)
    current_price = pred_calculation[-(len(pred_calculation))]
    short_ma = np.mean(pred_calculation[-5:])  # 5-period MA
    long_ma = np.mean(pred_calculation[-10:])  # 10-period MA
    long_signal = short_ma > long_ma and current_price - 2 < min_predArray and current_price - min_predArray < max_predArray - current_price
    short_signal = short_ma < long_ma and current_price + 2 > max_predArray and current_price - min_predArray > max_predArray - current_price
    print(f"{short_signal} {long_signal}")
    trend_status = "Normal"
    actual_slope = np.polyfit(range(5), close_series[-5:], 1)[0]
    predicted_slope = np.polyfit(range(5), pred_calculation[-5:], 1)[0]

    print(actual_slope)
    print(predicted_slope)

    if actual_slope > 0 and predicted_slope < 0:
        trend_status = "Bearish divergence detected"
        print(trend_status)
    elif actual_slope < 0 and predicted_slope > 0:
        trend_status = "Bullish divergence detected"
        print(trend_status)

    def generate_signal(pred_series, actual_price):
        trend = "bullish" if pred_series[-1] > pred_series[-5] else "bearish"
        volatility = np.std(pred_series[-10:])
        confidence = 1 / np.std(pred_series[-3:])
        if trend == "bullish" and confidence > 0.8:
            entry = actual_price + 0.3 * volatility
            stop_loss = actual_price - 1.8 * volatility
            return ("BUY", entry, stop_loss)
        elif trend == "bearish" and confidence > 0.8:
            entry = actual_price - 0.3 * volatility
            stop_loss = actual_price + 1.8 * volatility
            return ("SELL", entry, stop_loss)
        return ("HOLD", None, None)
    return "Long" if long_signal else "Short", trend_status
