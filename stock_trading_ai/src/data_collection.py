import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = ['KO', 'PEP'] #download data
data = yf.download(tickers, start='2015-01-01', end='2024-09-12')['Close']

data.to_csv('../data/ko_pep_data.csv') #saves data to csv file

data.plot(figsize=(10, 6))
plt.title("KO vs PEP Stock Prices")
plt.show()

