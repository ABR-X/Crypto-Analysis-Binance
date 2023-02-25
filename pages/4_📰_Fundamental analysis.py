
import streamlit as st
from ml_models_functions import sammurization as sm
from web_scrapping import news_scrapping as nws
from more import strip_unwanted_urls, create_output_array
import pandas as pd
from api_Config import set_client
from more import increment_session_var, refresh_progress

st.title("EFFECTUEZ VOS ANALYSES FONDAMENTALES!")
st.markdown("**Cette page vous permet d'analyser les dernières nouvelles liées à la crypto-monnaie que vous choisissez. Vous pouvez sélectionner l'une des crypto-monnaies les plus populaires, telles que Bitcoin, Ethereum, Solana, BNB, Ripple, Cardano, Matic et Dogecoin. Une fois que vous avez choisi une crypto-monnaie, cliquez sur le bouton 'Start search' pour obtenir les dernières nouvelles concernant cette crypto-monnaie. Les nouvelles sont extraites de sources fiables et sont résumées pour faciliter la lecture. De plus, la page fournit une évaluation du sentiment des nouvelles ainsi que la confiance associée à cette évaluation.**")
if "client" not in st.session_state:
    set_client()

ticker = st.selectbox(
    'Choisissez les crypto-monnaies a analyser!',
    ['BITCOIN', 'ETHEREUM', 'SOLANA', 'BNB', 'RIPPLE', 'CARDANO', 'MATIC', 'DOGECOIN'])
monitored_tickers = [ticker]

placeholder = st.empty()
search_btn = placeholder.button('Start search', disabled=False, key='1')
if search_btn:

    placeholder.button('Start search', disabled=True, key='2')
    if "news_progress_bar" not in st.session_state:
        st.session_state["progress"] = 0
        st.session_state["news_progress_bar"] = st.progress(st.session_state["progress"])
    print('Searching for stock news for', monitored_tickers)

    raw_urls = {ticker: nws.search_for_stock_news_links(ticker) for ticker in monitored_tickers}
    increment_session_var(5, "progress")
    refresh_progress("news_progress_bar", "progress")
    print('Cleaning URLs.')
    exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support', 'google']

    cleaned_urls = {ticker: strip_unwanted_urls(raw_urls[ticker], exclude_list) for ticker in monitored_tickers}
    print('Scraping news links.')

    increment_session_var(5, "progress")
    refresh_progress("news_progress_bar", "progress")

    articles = {ticker: nws.scrape_and_process(cleaned_urls[ticker]) for ticker in monitored_tickers}
    increment_session_var(30, "progress")
    refresh_progress("news_progress_bar", "progress")
    print('Summarizing articles.')
    print(articles)

    summaries = {ticker: sm.summarize(articles[ticker]) for ticker in monitored_tickers}
    increment_session_var(50, "progress")
    refresh_progress("news_progress_bar", "progress")
    print('Calculating sentiment.')
    sentiment = sm.load_transformers()
    increment_session_var(5, "progress")
    refresh_progress("news_progress_bar", "progress")
    scores = {ticker: sentiment(summaries[ticker]) for ticker in monitored_tickers}
    increment_session_var(5, "progress")
    refresh_progress("news_progress_bar", "progress")
    print('Exporting results')

    final_output = pd.DataFrame(create_output_array(summaries, scores, cleaned_urls, monitored_tickers))
    final_output = final_output.rename(columns={0: 'Ticker', 1: 'Summary', 2: 'Sentiment', 3: 'Score',
                                                4: 'URL'})
    st.session_state["news_progress_bar"].progress(100)
    st.session_state["progress"] = 0
    final_output = final_output.drop(columns=['Ticker'])
    final_output = final_output[final_output['Summary'] != 'We are aware of the issue and are working to resolve it.']
    st.header("LES NOUVEAUTÉS SUR " + ticker)
    for num in range(len(final_output)):
        expander = st.expander("**RÉSUMÉ : " + final_output.iloc[num].Summary + "**")
        expander.write("**IMPACT :** " + final_output.iloc[num].Sentiment.lower())
        expander.write("**PRÉCISION :** " + str(round(final_output.iloc[num].Score * 100, 2)) + "%")
        expander.write("**SOURCE :** " + final_output.iloc[num].URL)
    st.write("Veuillez noter que ces évaluations ne doivent être utilisées qu'à des fins éducatives et ne doivent pas être considérées comme une base pour prendre des décisions d'investissement.")
#    st.write(final_output)
    placeholder.button('Vider search', disabled=False, key='3')



