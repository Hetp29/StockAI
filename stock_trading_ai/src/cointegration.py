import pandas as pd
import statsmodels.api as sm #type-ignore
from statsmodels.tsa.stattools import coint #type-ignore
import itertools
import os
def load_stock_data(tickers):
    stock_data = {}
    for ticker in tickers:
        try:
            data = pd.read_csv(f'../data/stock_data/{ticker}.csv', index_cols='Date', parse_dates=True)
            stock_data[ticker] = data['Close'] #close price for integration
            #a stock's closing price is price at which stock trades at end, most recent valuation of security until next trading session begins
        except Exception as e:
            print(f"Error loading data for {ticker}: {e}")
    
    return stock_data

def test_cointegration(stock1, stock2):
    score, p_value, _ = coint(stock1, stock2)
    return p_value

def find_cointegrated_pairs(tickers, threshold=0.05):
    stock_data = load_stock_data(tickers)
    cointegrated_pairs = []
    
    for ticker1, ticker2 in itertools.combinations(stock_data.keys(), 2):
        try:
            p_value = test_cointegration(stock_data[ticker1], stock_data[ticker2])
            if p_value < threshold:
                cointegrated_pairs.append((ticker1, ticker2, p_value))
                print(f"Cointegrated pair found: {ticker1} ad {ticker2} with p-value {p_value}")
        
        except Exception as e:
            print(f"Error testing pair {ticker1} and {ticker2}: {e}")
            
    if cointegrated_pairs:
        pd.DataFrame(cointegrated_pairs, columns=["Ticker1", "Ticker2", "p-value"]).to_csv('../data/cointegrated_pairs.csv', index=False)
        print(f"Saved {len(cointegrated_pairs)} cointegrated pairs.")
    else:
        print("No cointegrated pairs found.")
if __name__ == "__main__":
    tickers = pd.read_csv('../data/sp500_tickers.csv')['Ticker'].tolist()[:495]
    find_cointegrated_pairs

#Blue line is the difference between KO's actual price and predicted prices based on PEP's prices. 
#How much KO is "overvalued" or "undervalued" compared to PEP based on their relationship

#Red line is mean spread, over time we expect spread to fluctuate around this mean if two stocks are cointegrated
#large deviations from mean can signal trading opportunities

#stock cointegration is when 2 or more stocks move together in long term, despite short-term price differences
#if one stocks price goes up while other goes down, they are likely to come back to their usual relationship, allowing traders to profit from temporary deviations

#The goal is to profit from temporary deviations in price relationship between KO and PEP
#if spread moves far away from mean (either too high or too low), you can expect spread to revert to mean overtime

#if spread is too high, you could short KO (expect it to fall) and buy PEP (expect it to rise)
#if spread becomes too low, you could buy KO and short PEP, expecting spread to revert to mean
#Example: KO price is $50
#PEP price is $100
#spread is the difference between KO and predicted KO price based on relationship with PEP

#spread becomes too high
#KO reaches $70 while PEP remains at $100. 
#new spread = 70 - (100/2) = 70 - 50 = 20
#spread is 20, this suggests KO is overpriced
#short KO, bet KO will fall (because it's too high compared to PEP)
#buy PEP, bet PEP price will rise or KO's will fall, bringing spread to normal

#spread becomes too low
#KO falls to $40 while PEP remains at $100
#spread is: 40 - (100/2) = 40 - 50 = -10
#spread is -10, KO is underpriced relative to PEP
#buy KO, bet KO will rise (because it's too low compared to PEP)
#short PEP, bet PEP price will fall or KO's will rise, bringing spread back to normal

#buy signal when spread is below mean, you expect the prices to come back 
#sell signal when spread is above mean, you expect the prices to come back

#ADF test (augmented dickey-fuller test) is statistical test used to determine whether time series is
#stationary (meaning its values do not depend on time)
