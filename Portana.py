import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date

# initializing portfolio details and time-frame to study data
# TO BE TAKEN AS INPUT
start_date = "2023-01-01"
end_date = "2023-01-31"
portfolio_assets = []

print("Welcome to Dev's Portfolio Analysis tool!")
initial_investment = int(input("Enter your initial investment (Dollars): "))
while True:
    symb = input("Enter your asset symbol: ")
    wt = float(input("Enter its weight in your portfolio"))
    portfolio_assets.append({"symbol": symb, "weight": wt})
    q = input("Enter another asset? Y/N: ")
    if q != "Y":
        break

# obtaining historic data
asset_data = {}
for asset in portfolio_assets:
    asset_data[asset['symbol']] = yf.download(asset['symbol'], start=start_date, end=end_date)


returns_data = pd.DataFrame()
for asset in portfolio_assets:
    asset_symbol = asset["symbol"]
    returns_data[asset_symbol + "_Return"] = asset_data[asset_symbol]["Adj Close"].pct_change()

#returns_data['AAPL'] has daily return of Apple in given timeframe   

returns_data["Portfolio_Return"] = np.sum(
    returns_data[asset["symbol"] + "_Return"] * asset["weight"] for asset in portfolio_assets
    #np.fromiter(returns_data[asset["symbol"] + "_Return"] * asset["weight"] for asset in portfolio_assets)
)

#returns_data["Portfolio_Return"] * 100


# CALCULATING VOLATILITY
volatality = returns_data["Portfolio_Return"].std()
# basically standard deviation of daily returns

# USING S&P 500 as metric to calculate beta
benchmark_data = yf.download("^GSPC",start = start_date, end = end_date)
benchmark_returns = benchmark_data['Adj Close'].pct_change()
#benchmark_returns

for asset in portfolio_assets:
    cov_matrix = np.cov(returns_data[asset['symbol'] + "_Return"].dropna(),benchmark_returns.dropna())
    asset['beta'] = cov_matrix[0,1]/benchmark_returns.var()
    

# Calulating Value at Risk
confidence_level = 0.95  # how sure you want to be about your estimate
initial_investment = 100000 # take as input by user

returns_data.dropna(inplace=True)
returns_data.sort_values(by="Portfolio_Return", inplace=True)
var_index = int(len(returns_data) * (1 - confidence_level))
var = -returns_data["Portfolio_Return"].iloc[var_index] * initial_investment


print("Portfolio Risk Analysis Results for Janury 2023:")
print(f"Portfolio Volatility: {volatality:.4f}")
print("Asset Betas:")
for asset in portfolio_assets:
    print(f"{asset['symbol']} beta: {asset['beta']:.4f}")
print(f"Portfolio VaR ({confidence_level*100}%): ${var:.2f}")

returns_data["Portfolio_Return"].plot(title="Portfolio Returns")
plt.show()
