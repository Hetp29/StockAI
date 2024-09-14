#load sp500 tickers
#fetch real time daily stock data using yahoo finance
#save each stock data in individual csv file
import yfinance as yf
import pandas as pd
import os

def load_sp500_tickers():
    return pd.read_csv('../data/sp500_tickers.csv')['Ticker'].tolist()

def fetch_stock_data(tickers):
    stock_data = {}
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist_data = stock.history(period='5y', interval='1d') #last 5 years of daily data
            
            if not hist_data.empty:
                stock_data[ticker] = hist_data
                print(f"Fetched data for {ticker}")
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    return stock_data

def save_stock_data(stock_data):
    if not os.path.exists('../data/stock_data/'):
        os.makedirs('../data/stock_data/')
        
    for ticker, data in stock_data.items():
        data.to_csv(f'../data/stock_data/{ticker}.csv')
        
if __name__ == '__main__':
    tickers = load_sp500_tickers()
    stock_data = fetch_stock_data(tickers)
    save_stock_data(stock_data)
    print(f"Saved fata for {len(stock_data)} stocks.")