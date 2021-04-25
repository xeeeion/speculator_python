import yfinance as yf


aflt = yf.Ticker("aflt.me")

# get stock info
print(aflt.info)

# get historical market data
hist = aflt.history(period="5d")

hist['Close'].plot(figsize=(16, 9))

data_df = yf.download("aflt.me", start="2021-03-01", end="2021-04-24")
data_df.to_csv('aflt.csv')

aflt.history(period="1y")
aflt.actions