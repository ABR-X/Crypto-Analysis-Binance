# Cryptocurrency Analysis Project

## Project Description
**This project involves the development of a user-friendly platform for analyzing data related to different cryptocurrencies using data science techniques. The platform includes functionalities for generating forecasts of future prices of Bitcoin, summarizing news articles related to different cryptocurrencies, analyzing fundamental factors affecting the cryptocurrency market, and visualizing data in an interactive way. The project was implemented using various tools and technologies, including FBProphet, Pegasus, Streamlit, Plotly, Matplotlib, Pandas, Seaborn, and Binance API.**


## Installation
To use this project, you will need to have Python 3.8 installed on your system. You can then install the required dependencies using pip and the provided requirements.txt file:

  `pip install -r requirements.txt`

In addition, you will need to replace the st.secrets["key"] and st.secrets["secret"] placeholders in the api_config.py file with your Binance API key and secret.

## Project Structure
The project is structured into several files, each containing functionalities related to specific aspects of the platform. These files are:

* **run_model.py:** This file provides functions for generating forecasts of future prices of Bitcoin using FBProphet.

* **summarize.py:** This file contains functions for summarizing news articles related to different cryptocurrencies using Pegasus.

* **fundamental_analysis.py:** This file is a Streamlit web application for analyzing fundamental factors affecting the cryptocurrency market, including news sentiment analysis, using data scraped from Yahoo Finance.

* **predictive_analysis.py:** This file is a Streamlit web application for generating forecasts of future prices of Bitcoin using machine learning techniques and visualizing data using Matplotlib.

* **coin.py:** This file contains functions for retrieving data related to different cryptocurrencies from the Binance API and displaying them in a user-friendly way in a Streamlit app.

* **about.py:** This file is a Streamlit page providing information about the project and the developer.

* **functions.py:** This file contains various functions related to cryptocurrency analysis, including performance analysis and data cleaning.

* **api_config.py:** This file contains a function for creating a Binance API client object.

* **scrapping.py:** This file contains functions for web scraping news articles related to different cryptocurrencies from Yahoo Finance.

* **clean.py:** This file contains a function for cleaning data.

## Project Requirements
The project requires the following libraries and frameworks:

* beautifulsoup4
* binance
* matplotlib
* numpy
* pandas
* Pillow
* plotly
* python_binance
* requests
* seaborn
* streamlit
* torch
* transformers

## Credits
This project was created by **Abderrahmane Aitelmouddene**. Special thanks to the **Streamlit** and **Binance** teams for providing the tools and APIs used in this project.

## Conclusion
This project demonstrates the implementation of a platform for analyzing cryptocurrency data using data science techniques. While the project successfully achieved its objectives, there are still limitations and opportunities for future improvements, such as incorporating more sources of news data and implementing more advanced machine learning models. The project was developed by a single student and utilized various open-source tools and libraries, including FBProphet, Pegasus, and Streamlit.
