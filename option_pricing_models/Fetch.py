import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Fetch:
    """Class to fetch data from yahoo finance"""

    @staticmethod
    def retrieve_historical_data(ticker, start = None, end = None, days_cache = 1, data_cache = True):
        """
        Retrieve stock data from yahoo finance
        Default: request is cashed in sqlite db for 1 day
        Params:
         -> ticker: ticker symbol
         -> start:
         -> end:
         -> days_cache: True/False for caching fetched data into sqlite db
         -> date_cache: number of days data will stay in cache
        """
        try:
            tick = yf.Ticker(ticker)
            data = tick.history(period="max", auto_adjust=False, actions=False)
            data.reset_index(inplace=True)
            return data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_col(data):
        """retrieves columns from fetched stock data
         Params:
         data: fetched data represented in a dataframe"""
        if data is None:
            return None
        return [col for col in data.columns]

    @staticmethod
    def get_most_recent_price(data, col_name):
        """returns the last available price for a specified column
        params:
        data: fetched data represented in a dataframe
        col_name: name of specified column"""
        if data is None or col_name is None:
            return None
        if col_name not in Fetch.get_col(data):
            return None
        return data[col_name].iloc[-1]


    @staticmethod
    def plot_data(data, ticker, col_name):
        """plots specific column in relation to time"""
        #alter!!!!!!!!!!! and in other one
        try:
            if data is None:
                return
            x = data["Date"]
            y = data[col_name]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            plt.gca().xaxis.set_major_locator(mdates.YearLocator(5, month = 1, day = 1))
            plt.plot(x,y)
            plt.gcf().autofmt_xdate()
            #plt.locator_params(axis='x', nbins=5)
            plt.ylabel(f'{col_name}')
            plt.xlabel('Date')
            plt.title(f'Historical Data for {ticker}: {col_name}')
            plt.legend(loc = 'best')
            plt.show()
        except Exception as e:
            print(e)
            return


