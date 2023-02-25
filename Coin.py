import pandas as pd
import streamlit as st
from binance.client import Client
from cleaning import clean
from api_Config import set_client

st.set_option('deprecation.showPyplotGlobalUse', False)
if "client" not in st.session_state:
    set_client()


@st.cache
def get_all_symbols():
    symbols = pd.DataFrame(st.session_state["client"].get_products()["data"])
    symbols = symbols[["s"]]
    return symbols


@st.cache
def get_stats(selected_coins):
    data = pd.DataFrame(st.session_state["client"].get_products()["data"])
    data = data[["s", "cs", "c"]]
    data["m"] = data["cs"] * data["c"]
    result = pd.DataFrame(columns=['s', 'cs', 'c'])
    for selected_coin in selected_coins:
        result = pd.concat([result, data[selected_coin == data["s"]]])

    return result

@st.cache
def get_all_tickers():
    data = pd.DataFrame(st.session_state["client"].get_products()["data"])
    data = data["b"].values.tolist()
    data = list(set(data))
    return data


class Coin:
    coins = []
    symbols = get_all_symbols()

    def __init__(self, name):
        if Coin.coin_exists(name):
            print(name, " already exists, if you are trying to change value of it please",
                     " consider using setters.")

        else:
            self.name = name
            Coin.coins.append(self)



    @staticmethod
    def coin_exists(name):
        for coin in Coin.coins:
            if coin.name == name:
                return 1
        return 0

    @staticmethod
    def get_coin(name):
        for coin in Coin.coins:
            if coin.name == name:
                return coin
        return 0

    @staticmethod
    @st.cache(suppress_st_warning=True)
    def gen_past_data(name, interval, startdate, enddate):
        coin = Coin.get_coin(name)
        if coin == 0:
            coin = Coin(name)

        data = []
        try:
            if interval == 'Jour':
                data = st.session_state["client"].get_historical_klines(name, Client.KLINE_INTERVAL_1DAY, startdate
                                                                        , enddate)
            elif interval == 'Semaine':
                data = st.session_state["client"].get_historical_klines(name, Client.KLINE_INTERVAL_1WEEK, startdate
                                                                        , enddate)
            elif interval == 'Mois':
                data = st.session_state["client"].get_historical_klines(name, Client.KLINE_INTERVAL_1MONTH, startdate
                                                                        , enddate)

            columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                       'Num of trades', 'Tbba volume', 'Tbqa volume', 'Ignore']
            wanted_col = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time']
            dtypes = ['time', 'num', 'num', 'num', 'num', 'num', 'time']
            data = clean(data, columns, wanted_col, dtypes)
        except:
            print("error")
            return []
        return data





