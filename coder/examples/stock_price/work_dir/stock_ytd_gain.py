# filename: stock_ytd_gain.py

import yfinance as yf
from datetime import datetime

# Define the stock symbols
stocks = ['META', 'TSLA']

# Define the start and end dates
start_date = '2024-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

# Fetch the stock data
data = yf.download(stocks, start=start_date, end=end_date)

# Calculate the year-to-date gain
ytd_gains = {}
for stock in stocks:
    start_price = data['Adj Close'][stock].iloc[0]
    end_price = data['Adj Close'][stock].iloc[-1]
    ytd_gain = ((end_price - start_price) / start_price) * 100
    ytd_gains[stock] = ytd_gain

# Print the year-to-date gains
for stock, gain in ytd_gains.items():
    print(f"Year-to-date gain for {stock}: {gain:.2f}%")