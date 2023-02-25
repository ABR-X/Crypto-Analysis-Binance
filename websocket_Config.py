import streamlit as st
import websocket
import json


# websocket configuration
websocket_status = 0


def on_open(ws):
    print("connected successfully!")


def on_close(ws):
    global websocket_status
    websocket_status = 0
    print("connection failed!")


def on_error(ws, error):
    print("error accured!", error)


def on_message(ws, message):
    data = json.loads(message)
    st.write("live close : ", data["k"]["c"])
    st.write("volume : ", data["k"]["v"])
    st.write("symbol : ", data["k"]["s"])

    global websocket_status
    websocket_status = 1


def get_live_data(coin, tf):
    socket = 'wss://fstream.binance.com/ws/' + coin + '@kline_' + tf
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_error=on_error, on_message=on_message)
    ws.run_forever()
