import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc

# id is the name of the coin you want
# vs_currency is the currency you want the price in
# days is how many days back from today you want.
cg = CoinGeckoAPI()
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)

#we just need prices from bitcoin_data 
bitcoin_price_data = bitcoin_data['prices']
data = pd.DataFrame(bitcoin_price_data, columns=['TimeStamp', 'Price'])

# convert the timestamp to datetime and save it as a column called Date
data['date'] = data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))

# group by the Date and find the min, max, open, and close for the candlestick
candlestick_data = data.groupby(data.date, as_index=False).agg({"Price": ['min', 'max', 'first', 'last']})

#use plotly to create candlestick chart
fig = go.Figure(data=[go.Candlestick(x=candlestick_data['date'],
                open=candlestick_data['Price']['first'], 
                high=candlestick_data['Price']['max'],
                low=candlestick_data['Price']['min'], 
                close=candlestick_data['Price']['last'])
                ])

fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()
