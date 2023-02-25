import matplotlib.pyplot as plt
import streamlit as st
from api_Config import set_client
import traceback
from Coin import Coin, get_stats
import pandas as pd
import more
from ploting import functions as fc


st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Analyse de marché")



if "client" not in st.session_state:
    set_client()

st.markdown("**Bienvenue sur la page d'analyse du marché des crypto-monnaies! Cette page vous permet d'analyser les performances des différentes crypto-monnaies en fonction de leur prix, capitalisation    et volatilité.**")
col1, col2 = st.columns(2)
with col1:
    timeframe = st.selectbox(
        'Interval',
        ('Jour', 'Semaine', 'Mois'))

symbols = Coin.symbols
symbols = pd.DataFrame(symbols)

with col2:
    selected_coins = st.multiselect(
        'Coins',
        symbols,
        default="BTCUSDT")

try:

    tab1, tab2, tab3 = st.tabs(["📈 Prix", "Market cap", "Volatility"])

    more.set_dates()

    more.set_data_dates()

    with tab1:
        st.markdown("**Analyse des prix et de la corrélation de différentes crypto-monnaies.**")
        st.subheader("Visualization de prix")

        combined = more.gen_combined_data(selected_coins, timeframe, "Close")
        fig, ax = fc.multiline_pyplot(combined, selected_coins)
        st.pyplot(plt.show())
        st.write("Ce graph affiche les prix de clôture des crypto-monnaies sélectionnées sur une période donnée, en fonction de l'interval choisi. Cette visualisation permet de comparer facilement les prix historiques des différentes crypto-monnaies et d'identifier les tendances du marché")
        if len(combined.columns) >1:
            st.subheader("corrélation entre les prix des différentes crypto-monnaies")

            fig, ax = fc.correlation(combined)
            # Show the plot
            st.pyplot(fig)
            st.write("Cette visualisation montre la corrélation entre les prix des différentes crypto-monnaies sélectionnées. Elle permet de déterminer si les prix de deux crypto-monnaies ont tendance à évoluer dans la même direction ou dans des directions opposées, ce qui peut être utile pour prendre des décisions d'investissement éclairées.")



    with tab2:
        st.subheader("Capitalisation boursière")
        stats_data = get_stats(selected_coins)
        fig, ax = plt.subplots()
        ax.bar(stats_data["s"], stats_data["m"])
        st.pyplot(fig)
        st.write("Ce graphique montre la capitalisation boursière des crypto-monnaies sélectionnées. La capitalisation boursière est calculée en multipliant le prix actuel de chaque crypto-monnaie par son offre totale en circulation. Il peut aider à comprendre la part de marché de chaque crypto-monnaie et comment elle évolue.")

    with tab3:
        st.subheader("Volatilité des crypto-monnaies")
        data = more.gen_combined_data(selected_coins, "Jour", "Close")
        volatility = pd.DataFrame(columns=["Coin", "Volatility"]).set_index("Coin", inplace=True)

        with plt.style.context("seaborn-whitegrid"):
            fig, ax = plt.subplots()

            for selected_coin in selected_coins:
                volatility = more.get_volatility(selected_coin, data)
                ax.scatter(volatility.index.values, volatility["Volatility"])

            ax.set_ylabel("Volatility")
            ax.legend(selected_coins)

            st.pyplot(fig)

            st.write("Ce graphique affiche la volatilité des crypto-monnaies sélectionnées. La volatilité est une mesure de la variation des prix d'un actif sur une période donnée. Ce graphique peut aider à évaluer le risque associé à chaque crypto-monnaie et à identifier les périodes de forte volatilité.")



except Exception as e:
    print("exception")
    print(e)
    traceback.print_exc()

add_slider = st.sidebar.slider(
    "Periode?",
    st.session_state["date_5y_ago"],
    st.session_state["now"],
    (st.session_state["date_1y_ago"], st.session_state["now"]),
    on_change=more.slider_change,
    key="slider",
    format="YY-MM-DD")




