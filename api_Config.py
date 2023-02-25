import streamlit as st
from binance.client import Client

def set_client():
    key=st.secrets["key"]
    secret=st.secrets["secret"]
    client = Client(key, secret)
    st.session_state["client"] = client

