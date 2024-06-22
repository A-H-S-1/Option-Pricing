import numpy as np
from scipy.stats import norm

from option_pricing_models.Option_pricing_interface import Option_Pricing_Model

class Black_Scholes_Model(Option_Pricing_Model):
    """
    Class implements the calculation for European option pricing using Black-Scholes Formula
    Call/Put option pricing calculated using the following assumptions:
     -> EU option can only be exercised on the maturity date
     -> During the option's lifetime the underlying stock does not pay divident
     -> Volatility and risk-free rate are constant
     -> Efficient Market Hypothesis (the market movements cannot be predicted)
     -> Underlying returns distribution is lognormal
    """

    def __init__(self, sigma, under_price, days_mature, strike_price, risk_free_rate):
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


    def _calc_call_option_price(self):
        """ Calculates price for call option using S*N(d_1) - Present_Value(K)*N(d_2)

        Risk-adjusted probability: option will be exercised"""
        d_1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))

        # Probability: receiving stock at expiration of option
        d_2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        return (self.S * norm.cdf(d_1, 0.0, 1.0) - self.K * np.exp(-self.r * self.T) * norm.cdf(d_2, 0.0, 1.0))

    def _calc_put_option_price(self):
        """ Calculates price for put option using Present_Value(K)*N(-d_2) - S*N(-d_1)

        Risk-adjusted probability: option will be exercised"""
        d_1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))

        # Probability: receiving stock at expiration of option
        d_2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        return (self.K * np.exp(-self.r * self.T) * norm.cdf(-d_2, 0.0, 1.0) - self.S * norm.cdf(-d_1, 0.0, 1.0))
