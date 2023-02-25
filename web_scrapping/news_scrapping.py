import streamlit as st
from bs4 import BeautifulSoup
import requests

@st.cache
def search_for_stock_news_links(ticker):
    search_url = 'https://www.google.com/search?q=yahoo+finance+{}&tbm=nws'.format(ticker)
    r = requests.get(search_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    atags = soup.find_all('a')
    hrefs = [link['href'] for link in atags]
    return hrefs


@st.cache
def scrape_and_process(urls):
    articles = []
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('p')
        text = [res.text for res in results]
        words = ' '.join(text).split(' ')[:350]
        article = ' '.join(words)
        articles.append(article)

    return articles
