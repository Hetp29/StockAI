#preprocess data and calculate daily returns
import pandas as pd

data = pd.read_csv('../data/ko_pep_data.csv', index_col='Date', parse_dates=True)

data = data.dropna()
returns = data.pct_change().dropna()

returns.to_csv('../data/ko_pep_returns.csv')