import streamlit as st
import datetime as dt
from Coin import Coin
import pandas as pd
import numpy as np
import re


def slider_change():

    st.session_state["Coin_s_date"] = date_to_ms_timestamp(st.session_state["slider"][0])
    st.session_state["Coin_e_date"] = date_to_ms_timestamp(st.session_state["slider"][1])
    print("slider changed")


def set_dates():

    st.session_state["now"] = dt.date.today()
    st.session_state["date_5y_ago"] = st.session_state["now"] - dt.timedelta(days=5 * 365)
    st.session_state["date_1y_ago"] = st.session_state["date_5y_ago"] + dt.timedelta(days=4 * 365)

@st.cache
def date_to_ms_timestamp(date):
    result = str(dt.datetime.combine(date, dt.datetime.min.time())
                                          .replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
    return result

@st.cache
def ms_timestamp_to_date(ts):
    return str(dt.date.fromtimestamp(float(ts) / 1000))



def set_data_dates():

    if "Coin_s_date" not in st.session_state and "Coin_e_date" not in st.session_state:
        st.session_state["Coin_s_date"] = date_to_ms_timestamp(st.session_state["date_1y_ago"])
        st.session_state["Coin_e_date"] = date_to_ms_timestamp(st.session_state["now"])



def gen_combined_data(selected_coins, timeframe, col):

    cols = []
    combined = []
    temp = True
    for selected_coin in selected_coins:
        past_data = Coin.gen_past_data(selected_coin, timeframe, st.session_state["Coin_s_date"],
                                       st.session_state["Coin_e_date"])
        #past_data["Close time"] = 
        past_data = past_data.set_index("Close time")
        if temp:
            combined = past_data[[col]].copy()
            cols.append(selected_coin)
            combined.columns = cols
            temp = False
        else:
            combined = combined.join(past_data[col])
            cols.append(selected_coin)
            combined.columns = cols

    return combined


@st.cache
def get_volatility(coin, close_data):

    volatility = pd.DataFrame(columns=["Coin", "Volatility"]).set_index("Coin", inplace=True)
    close_data["LR"] = np.log(close_data[coin] / close_data[coin].shift(1))

    close_data["VY"] = round(close_data['LR']
                             .rolling(window=len(close_data) - 1).std() * np.sqrt(len(close_data) - 1), 2)
    volatility = pd.concat([volatility, pd.DataFrame({"Volatility": float(close_data["VY"].tail(1))}, index=[coin])])
    return volatility


@st.cache
def strip_unwanted_urls(urls, exclude_list):
    val = []
    for url in urls:
        if 'https://' in url and not any(exc in url for exc in exclude_list):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            val.append(res)

    return list(set(val))


@st.cache
def create_output_array(summaries, scores, urls, monitored_tickers):
    output = []
    for ticker in monitored_tickers:
        for counter in range(len(summaries[ticker])):
            output_this = [
                            ticker,
                            summaries[ticker][counter],
                            scores[ticker][counter]['label'],
                            scores[ticker][counter]['score'],
                            urls[ticker][counter]
                          ]
            output.append(output_this)

    return output


def increment_session_var(num, label):
    if label not in st.session_state:
        return 0
    st.session_state[label] += num


def refresh_progress(bar, progress):
    if bar not in st.session_state or progress not in st.session_state:
        return 0
    st.session_state[bar] = st.session_state[bar].progress(st.session_state[progress])


# def test_file():
#     import os
#     for f in os.listdir("./ml_models_functions/"):
#         print(f)



