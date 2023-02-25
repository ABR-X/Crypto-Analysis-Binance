import streamlit as st
from Coin import Coin
import pandas as pd
from api_Config import set_client
import more
from plotly import express as px
import matplotlib.pyplot as plt
import seaborn as sns


if "client" not in st.session_state:
    set_client()

st.title("Analyse pour une crypto-monnaie")
st.markdown("**Cette page vous permet d'analyser les données historiques d'une crypto-monnaie de votre choix. Elle affiche également des graphiques pour visualiser l'évolution du prix de la crypto-monnaie et propose des outils d'analyse tels que le Daily Lag et le KDE Plot.**")

col1, col2 = st.columns(2)
with col1:
    timeframe = st.selectbox(
        'Interval',
        ('Jour', 'Semaine', 'Mois'))

symbols = Coin.symbols
symbols = pd.DataFrame(symbols)
with col2:
    selected_coin = st.selectbox(
        'Choisissez la crypto-monnaie que vous souhaitez prédire!',
        symbols)


try:

    more.set_dates()
    more.set_data_dates()

    past_data = Coin.gen_past_data(selected_coin, timeframe, st.session_state["Coin_s_date"]
                                , st.session_state["Coin_e_date"])


    add_slider = st.slider(
        "Periode?",
        st.session_state["date_5y_ago"],
        st.session_state["now"],
        (st.session_state["date_1y_ago"], st.session_state["now"]),
        on_change=more.slider_change,
        key="slider",
        format="YY-MM-DD")

    st.header("Graphique de l'historique des prix de " + selected_coin)
    fig = px.line(past_data, x='Close time', y='Close', title='Prix de cloture')
    fig.update_layout(hovermode="x")

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=2, label="2y", step="year", stepmode="backward"),
                dict(step="all")
                
            ])
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write("Ce graphique montre l'historique des prix de la crypto-monnaie sélectionnée sur une période donnée. Vous pouvez zoomer sur le graphique en utilisant les boutons de sélection, et passer la souris sur les points du graphique pour obtenir des informations détaillées sur les prix à des moments précis.")

    
    fig, ax = plt.subplots(figsize=(10, 5))
    pd.plotting.lag_plot(past_data['Close'], lag=1, ax=ax) # lag
    if timeframe == "Jour":
        st.header('Décalage quotidien du ' + selected_coin)
    elif timeframe == "Semaine":
        st.header('Décalage hebdomadaire du ' + selected_coin)
    else:
        st.header('Décalage mensuel du ' + selected_coin)
    st.pyplot(fig)
    st.write("Cette visualisation montre le décalage de la crypto-monnaie par rapport à elle-même en utilisant un graphique de décalage. Si le décalage est proche de la ligne droite, cela suggère que le comportement de la crypto-monnaie est fortement corrélé avec son propre comportement dans le temps. Le titre du graphique varie en fonction de l'intervalle de temps sélectionné (quotidien, hebdomadaire, mensuel)")

    st.header("Distribution de la valeur de clôture")
    fig = plt.figure(figsize=(10, 4))
    sns.kdeplot(past_data['Close'], shade=True)
    st.pyplot(fig)
    st.write("Cette section affiche un graphique de densité de distribution de la valeur de clôture (Close) de la crypto-monnaie sélectionnée. La distribution de probabilité est estimée à l'aide d'une estimation de densité par noyau (Kernel Density Estimation - KDE) qui permet de visualiser la forme de la distribution des valeurs de clôture. Les zones ombrées représentent les zones de densité plus élevées et les zones non ombrées représentent les zones de densité plus faibles. Cela peut aider à comprendre la distribution des valeurs de clôture et donc à mieux comprendre la tendance de la crypto-monnaie sélectionnée.")
except:
    st.write("An Error Accured, please come back later ..")