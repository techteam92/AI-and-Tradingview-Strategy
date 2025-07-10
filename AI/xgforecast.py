import numpy as np
import pandas as pd
from pandas import DataFrame, concat
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

def forecast(series, n):
    # Convert time series to supervised learning format
    def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
        df = DataFrame(data)
        cols = []
        # Input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
        # Forecast sequence (t, t+1, ... t+n-1)
        for i in range(0, n_out):
            cols.append(df.shift(-i))
        agg = concat(cols, axis=1)
        if dropnan:
            agg.dropna(inplace=True)
        return agg.values

    # Split dataset into train and test sets
    def train_test_split(data, n_test):
        return data[:-n_test, :], data[-n_test:, :]

    # Fit XGBoost model and make one-step forecast
    def xgboost_forecast(train, testX):
        train = np.asarray(train)
        trainX, trainy = train[:, :-1], train[:, -1]
        model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)
        model.fit(trainX, trainy)
        yhat = model.predict(np.asarray([testX]))
        return yhat[0]

    # Walk-forward validation for time series
    def walk_forward_validation(data, n_test):
        predictions = []
        train, test = train_test_split(data, n_test)
        history = [x for x in train]
        for i in range(len(test)):
            testX, testy = test[i, :-1], test[i, -1]
            yhat = xgboost_forecast(history, testX)
            predictions.append(yhat)
            history.append(test[i])
        error = mean_absolute_error(test[:, -1], predictions)
        return error, test[:, -1], predictions

    values = series.values

    # Transform series into supervised learning with 6 lag observations
    data = series_to_supervised(values, n_in=n)

    # Evaluate model with last 12 samples as test set
    mae, y_true, y_pred = walk_forward_validation(data, 30)
    print(f'Mean Absolute Error: {mae:.3f}')

    return y_pred, mae