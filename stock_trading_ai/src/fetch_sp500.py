#fetching S&P500 using yahoo finance
import yfinance as yf
import pandas as pd

def fetch_sp500_tickers():
    sp500_tickers_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    tickers_df = pd.read_html(sp500_tickers_url)[0]
    tickers = tickers_df['Symbol'].tolist()
    
    #save tickers to csv file for later use
    pd.DataFrame(tickers, columns=["Ticker"]).to_csv('../data/sp500_tickers.csv', index=False)
    return tickers

if __name__ == "__main__":
    tickers = fetch_sp500_tickers()
    print(f"Fetched {len(tickers)} S&P 500 tickers.")