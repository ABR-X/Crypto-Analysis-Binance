import pandas as pd
import pickle
from Coin import Coin
import datetime as dt
import streamlit as st

def prepare_btc_data_for_ml():
    today = str(dt.date.today()- dt.timedelta(days=1))
    start_date = str(dt.date.today() - dt.timedelta(days=100))

    original = Coin.gen_past_data('BTCUSDT', 'Jour', start_date, today)

    original = original[["Close time", "Close", "Volume"]]

    original = original.rename(columns={'Close time': 'Date'})

    dataframe = original.copy()
    dataframe = dataframe.set_index('Date')
    dataframe.reset_index(inplace=True)
    dataframe = dataframe.set_index("Date")
    dataframe.reset_index(drop=False, inplace=True)
    dataframe = dataframe.set_index("Date", drop=False).copy()
    return dataframe

def prepare_data_to_predict(period, start_date, df):

    # period = 7
    # Create a dataframe with the ds and period columns
    future = pd.DataFrame({'ds': pd.date_range(start=start_date, periods=period, freq='D')})
    future["Close"] = None
    future["Volume"] = None
    future = future.rename(columns={'ds': 'Date'}).set_index("Date", drop=False)
    df = df.append(future).copy()
    df.reset_index(drop=True, inplace=True)

    return df

def add_rolling_features(df):

    rolling_features = ["Close", "Volume"]
    window1 = 3
    window2 = 7
    window3 = 30

    # First convert our original df to a rolling df of 3d, 7d  and 30d
    df_rolled_3d = df[rolling_features].rolling(window=window1, min_periods=0)
    df_rolled_7d = df[rolling_features].rolling(window=window2, min_periods=0)
    df_rolled_30d = df[rolling_features].rolling(window=window3, min_periods=0)

    df_mean_3d = df_rolled_3d.mean().shift(1).reset_index()
    df_mean_7d = df_rolled_7d.mean().shift(1).reset_index()
    df_mean_30d = df_rolled_30d.mean().shift(1).reset_index()

    df_std_3d = df_rolled_3d.std().shift(1).reset_index()
    df_std_7d = df_rolled_7d.std().shift(1).reset_index()
    df_std_30d = df_rolled_30d.std().shift(1).reset_index()

    for feature in rolling_features:
        df[f"{feature}_mean_lag{window1}"] = df_mean_3d[feature]
        df[f"{feature}_mean_lag{window2}"] = df_mean_7d[feature]
        df[f"{feature}_mean_lag{window3}"] = df_mean_30d[feature]

        df[f"{feature}_std_lag{window1}"] = df_std_3d[feature]
        df[f"{feature}_std_lag{window2}"] = df_std_7d[feature]
        df[f"{feature}_std_lag{window3}"] = df_std_30d[feature]

    df.fillna(df.mean(), inplace=True)

    df.set_index("Date", drop=False, inplace=True)

    df["month"] = df.Date.dt.month
    df["week"] = df.Date.dt.week
    df["day"] = df.Date.dt.day
    df["day_of_week"] = df.Date.dt.dayofweek

    return df

def load_model():
    with open("D:\github_projects\Crypto-analysis-binance\ml_models_functions\model.pkl", 'rb') as f:
        loaded_model = pickle.load(f)
    return loaded_model

def gen_forecast(df, period):
    loaded_model = load_model()
    exogenous_features = ['Close_mean_lag3', 'Close_mean_lag7', 'Close_mean_lag30',
                          'Close_std_lag3', 'Close_std_lag7', 'Close_std_lag30',
                          'Volume_mean_lag3', 'Volume_mean_lag7',
                          'Volume_mean_lag30', 'Volume_std_lag3', 'Volume_std_lag7',
                          'Volume_std_lag30', 'month', 'week', 'day', 'day_of_week']

    exogenous_features_df = df.tail(period).copy()

    forecast = loaded_model.predict(exogenous_features_df[["Date"] + exogenous_features].rename(columns={"Date": "ds"}))

    forecast = forecast[["ds", "yhat"]].rename(columns={"ds": "Date", "yhat": "Forecast"}).set_index("Date", drop=True)
    return forecast

