#linear regression to determine cointegration 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.stattools import adfuller

data = pd.read_csv('../data/ko_pep_data.csv', index_col='Date', parse_dates=True)

x = data['PEP'].values.reshape(-1, 1)
y = data['KO'].values

model = LinearRegression()
model.fit(x, y)

spread = data['KO'] - model.predict(x)

adf_result = adfuller(spread)

print(f"ADF Test Statistic: {adf_result[0]}")
print(f"p-value: {adf_result[1]}")

plt.figure(figsize=(10, 6))
plt.plot(spread, label='Price Spread (KO - PEP)')
plt.axhline(spread.mean(), color='red', linestyle='--', label='Mean Spread')
plt.title("Price Spread Between KO and PEP")
plt.legend()
plt.show()

if adf_result[1] < 0.05:
    print("KO and PEP are cointegrated (p < 0.05, spread is stationary)")
else:
    print("KO and PEP are not cointegrated (p >= 0.05, spread is not stationary)")
    
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