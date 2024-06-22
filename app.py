from datetime import datetime, timedelta
from enum import Enum
import streamlit as st
from option_pricing_models import Binomial_Tree_Model, Black_Scholes_Model, Monte_Carlo_Simulation, Fetch


class OPTION_PRICING_MODEL(Enum):
    BINOMIAL = 'Binomial Model'
    MONTE = 'Monte Carlo Simulation'
    SCHOLES = 'Black-Scholes Model'


st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Option Pricing')
price_method = st.sidebar.radio('Select option pricing method', options = [m.value for m in OPTION_PRICING_MODEL])
st.subheader(f'Pricing Method: {price_method}')

if price_method == OPTION_PRICING_MODEL.BINOMIAL.value:
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 0)
    risk_free_rate = st.slider('Risk-Free Rate (%)', 0, 100, 10)
    sigma = st.slider('Sigma (%)', 0, 100, 10)
    exer_date = st.date_input('Exercise date', min_value = datetime.today() + timedelta(days=1), value = datetime.today() + timedelta(days=365))
    num_steps = st.slider('Number of Time Steps', 5000, 100000, 15000)

    if st.button(f'Calculate option price for {ticker}'):
        data = Fetch.Fetch.retrieve_historical_data(ticker)
        st.write(data.tail())
        Fetch.Fetch.plot_data(data, ticker, 'Adj Close')
        st.pyplot()
        price =  Fetch.Fetch.get_most_recent_price(data, 'Adj Close')
        risk_free_rate = risk_free_rate/100
        sigma = sigma/100
        days_mature = (exer_date - datetime.now().date()).days
        btm =  Binomial_Tree_Model.Binomial_Tree_Model(sigma, price, num_steps, days_mature, strike_price, risk_free_rate)
        cop = btm.calc_option_price('Call Option')
        pop = btm.calc_option_price('Put Option')
        st.subheader(f'Call Option Price: {cop}')
        st.subheader(f'Put Option Price: {pop}')

elif price_method == OPTION_PRICING_MODEL.MONTE.value:
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 0)
    risk_free_rate = st.slider('Risk-Free Rate (%)', 0, 100, 10)
    sigma = st.slider('Sigma (%)', 0, 100, 10)
    exer_date = st.date_input('Exercise date', min_value = datetime.today() + timedelta(days=1), value = datetime.today() + timedelta(days=365))
    num_sim = st.slider('Number of Simulations', 100, 100000, 10000)
    num_moves = st.slider('Number of Price Movement Simulations Visualized', 0, int(num_sim))

    if st.button(f'Calculate option price for {ticker}'):
        data =  Fetch. Fetch.retrieve_historical_data(ticker)
        st.write(data.tail())
        Fetch.Fetch.plot_data(data, ticker, 'Adj Close')
        st.pyplot()
        price =  Fetch.Fetch.get_most_recent_price(data, 'Adj Close')
        risk_free_rate = risk_free_rate/100
        sigma = sigma/100
        days_mature = (exer_date - datetime.now().date()).days
        mc =  Monte_Carlo_Simulation.Monte_Carlo_Simulation(num_sim, sigma, price, days_mature, strike_price, risk_free_rate)
        mc.sim_price()
        mc.plot_sim_results(num_moves)
        st.pyplot()
        cop = mc.calc_option_price('Call Option')
        pop = mc.calc_option_price('Put Option')
        st.subheader(f'Call Option Price: {cop}')
        st.subheader(f'Put Option Price: {pop}')


elif price_method == OPTION_PRICING_MODEL.SCHOLES.value:
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 0)
    risk_free_rate = st.slider('Risk-Free Rate (%)', 0, 100, 10)
    sigma = st.slider('Sigma (%)', 0, 100, 10)
    exer_date = st.date_input('Exercise date', min_value = datetime.today() + timedelta(days=1), value = datetime.today() + timedelta(days=365))

    if st.button(f'Calculate option price for {ticker}'):
        data =  Fetch. Fetch.retrieve_historical_data(ticker)
        st.write(data.tail())
        Fetch.Fetch.plot_data(data, ticker, 'Adj Close')
        st.pyplot()
        price =  Fetch.Fetch.get_most_recent_price(data, 'Adj Close')
        risk_free_rate = risk_free_rate/100
        sigma = sigma/100
        days_mature = (exer_date - datetime.now().date()).days
        bsm = Black_Scholes_Model.Black_Scholes_Model(sigma, price, days_mature, strike_price, risk_free_rate)
        cop = bsm.calc_option_price('Call Option')
        pop = bsm.calc_option_price('Put Option')
        st.subheader(f'Call Option Price: {cop}')
        st.subheader(f'Put Option Price: {pop}')

