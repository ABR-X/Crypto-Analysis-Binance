import streamlit as st
import matplotlib.pyplot as plt
from ml_models_functions import runmodel as rm
import pandas as pd
from more import increment_session_var, refresh_progress


st.title("Prédiction du prix du Bitcoin à court terme")


st.markdown("**Cette section utilise des techniques de Machine Learning pour prédire les prix futurs du Bitcoin. Les données passées du Bitcoin sont préparées pour entraîner un modèle de prédiction, qui est ensuite utilisé pour générer des prévisions de prix pour les jours suivants.**")
placeholder = st.empty()
search_btn = placeholder.button('Generer la Prediction', disabled=False, key='1')
if search_btn:
    if "news_progress_bar" not in st.session_state:
        st.session_state["progress"] = 0
        st.session_state["news_progress_bar"] = st.progress(st.session_state["progress"])
    

    placeholder.button('Generer la Prediction', disabled=True, key='2')
    period = 7
    original = rm.prepare_btc_data_for_ml()
    increment_session_var(20, "progress")
    refresh_progress("news_progress_bar", "progress")
    start_date = original['Date'].max() + pd.Timedelta(days=1)

    df = rm.prepare_data_to_predict(period, start_date, original)
    increment_session_var(10, "progress")
    refresh_progress("news_progress_bar", "progress")
    df = rm.add_rolling_features(df)
    increment_session_var(20, "progress")
    refresh_progress("news_progress_bar", "progress")
    forecast = rm.gen_forecast(df, period)
    increment_session_var(20, "progress")
    refresh_progress("news_progress_bar", "progress")
    past = pd.DataFrame(df.copy()["Close"]).head(100).tail(50)
    increment_session_var(20, "progress")
    refresh_progress("news_progress_bar", "progress")

    fig, ax = plt.subplots(figsize=(16, 8))
    plt.title("BTCUSDT")
    past["Close"].plot(ax=ax, label="Actual Close Prices")
    forecast["Forecast"].plot(ax=ax, label="Predicted Close Prices")
    plt.legend()
    st.session_state["news_progress_bar"].progress(100)
    st.session_state["progress"] = 0
    st.write(fig)
    st.write("Veuillez noter que ces prévisions ne sont fournies qu'à titre éducatif et ne doivent pas être utilisées comme base pour prendre des décisions d'investissement. La prédiction est basée sur des techniques de machine learning appliquées à l'historique des prix du Bitcoin et n'a pas été validée par des professionnels de l'investissement.")




