import yfinance as yf
from option_pricing_models import Binomial_Tree_Model, Black_Scholes_Model, Monte_Carlo_Simulation, Fetch
data =  Fetch.Fetch.retrieve_historical_data('TSLA')
print( Fetch.Fetch.get_col(data))
print( Fetch.Fetch.get_most_recent_price(data, 'Adj Close'))
Fetch.Fetch.plot_data(data, 'TSLA', 'Adj Close')
