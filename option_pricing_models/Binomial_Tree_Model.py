import numpy as np
from scipy.stats import norm

from option_pricing_models.Option_pricing_interface import Option_Pricing_Model

class Binomial_Tree_Model(Option_Pricing_Model):
    """
    Class implements the calculation for European option pricing using the Binomial Option Pricing Model (BOPM)
    In a specified number of time points between the date of valuation and exersice date, it calculates the option price using discrete time (lattice based)
    Pricing model has 3 steps:
     -> Price tree generation
     -> Calculate option value at each of the nodes
     -> Sequentially calculates the option value at preceding nodes
    """

    def __init__(self, sigma, under_price, num_time_steps, days_mature, strike_price, risk_free_rate):
       """Initialize variables in Black-Scholes formulas
       sigma: standard deviation of asset's log return
       under_price: current stock/underlying spot price
       num_time_steps: number of time periods between valuation date and the exercise date
       days_mature: option contract exercise/maturity date
       strike_price: the strike price for the option contract
       risk_free_rate: returns on risk-free assets assuming constant returns till expiry date
       """

       self.S = under_price
       self.K = strike_price
       self.T = days_mature / 365
       self.r = risk_free_rate
       self.sigma = sigma
       self.num_time_steps = num_time_steps

    def _calc_call_option_price(self):
        """Calculates call option price using the Binomial formula"""
        delta_T = self.T / self.num_time_steps
        up = np.exp(self.sigma * np.sqrt(delta_T) )
        down = 1.0 / up
        PV = np.zeros(self.num_time_steps + 1) # initialize price vector

        # underlying asset prices at different points in time
        AP_T = np.array([(self.S * (up**i) * down**(self.num_time_steps - i)) for i in range(self.num_time_steps + 1)])

        comp_return = np.exp(self.r * delta_T) # risk-free compounded return
        up_prob = (comp_return - down) / (up - down) #risk neutral up probability
        down_prob = 1.0 - up_prob #risk neutral down probability
        PV[:] = np.maximum(AP_T - self.K, 0.0)

        #overriding option price
        for i in range(self.num_time_steps - 1, -1, -1):
            PV[:-1] = np.exp(-self.r * delta_T) * (up_prob * PV[1:] + down_prob * PV[:-1])

        return PV[0]

    def _calc_put_option_price(self):
        """Calculates put option price using the Binomial formula"""
        delta_T = self.T / self.num_time_steps
        up = np.exp(self.sigma * np.sqrt(delta_T))
        down = 1.0 / up
        PV = np.zeros(self.num_time_steps + 1) # initialize price vector

        # underlying asset prices at different points in time
        AP_T = np.array([(self.S * (up**i) * down**(self.num_time_steps - i)) for i in range(self.num_time_steps + 1)])

        comp_return = np.exp(self.r * delta_T) # risk-free compounded return
        up_prob = (comp_return - down) / (up - down) #risk neutral up probability
        down_prob = 1.0 - up_prob #risk neutral down probability
        PV[:] = np.maximum(AP_T - self.K, 0.0)

        #overriding option price
        for i in range(self.num_time_steps - 1, -1, -1):
            PV[:-1] = np.exp(-self.r * delta_T) * (up_prob * PV[1:] + down_prob * PV[:-1])

        return PV[0]

