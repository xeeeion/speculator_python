import yfinance as yf
import matplotlib.pyplot as plt
import seaborn

msft = yf.Ticker("MSFT")

# get stock info
print(msft.info)

# get historical market data
hist = msft.history(period="5d")

hist['Close'].plot(figsize=(16, 9))

data_df = yf.download("MSFT", start="2021-03-01", end="2021-04-30")
data_df.to_csv('MSFT.csv')

msft.history(period="1y")
msft.actions