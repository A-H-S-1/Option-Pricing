import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from option_pricing_models.Option_pricing_interface import Option_Pricing_Model

class Monte_Carlo_Simulation(Option_Pricing_Model):
    """
    Class implements the calculation for European option pricing using the Monte Carlo Simulation
    Simulate the underlying asset price on the expiry date using random stochastic process (brownian motion)
     -> Prices are generated at maturity: calculate and sum payoffs, average them, discount the final value
    The above calculation is the option price
    """
    def __init__(self, num_sims, sigma, under_price, days_mature, strike_price, risk_free_rate):
        """Initialize variables in Black-Scholes formulas
        sigma: standard deviation of asset's log return
        under_price: current stock/underlying spot price
        days_mature: option contract exercise/maturity date
        strike_price: the strike price for the option contract
        risk_free_rate: returns on risk-free assets assuming constant returns till expiry date
        """
        #Params for monte carlo simulation and brownian process
        self.S = under_price
        self.K = strike_price
        self.T = days_mature / 365
        self.r = risk_free_rate
        self.sigma = sigma
        self.N = num_sims
        self.num_steps = days_mature
        self.dt = self.T / self.num_steps


    def sim_price(self):
        """Simulate price movement using the brownian random process and saving the results"""

        np.random.seed(1234)
        self.sim_results = None

        # initialize price movements
        # Row: time index, Column: random price movements
        M = np.zeros((self.num_steps, self.N))

        # Current spot price is starting value for price movements
        M[0] = self.S

        for i in range(1, self.num_steps):
            RV = np.random.standard_normal(self.N) #random values (gaussian distribution)
            M[i] = M[i - 1] * np.exp((self.r - 0.5 * self.sigma**2) * self.dt + (self.sigma * np.sqrt(self.dt) * RV))

        self.sim_results_M = M

    def _calc_call_option_price(self):
        """ Calculate call option price
            -> calculate payoffs, summing, averiging, and discounting
            Call option payoff only if the price is higher than strike
            -> max(S_t - K, 0)
        """
        if self.sim_results_M is None:
            return -1
        return np.exp(-self.r * self.T) * 1 / self.N * np.sum(np.maximum(self.sim_results_M[-1] - self.K, 0))

    def _calc_put_option_price(self):
        """ Calculate call option price
            -> calculate payoffs, summing, averiging, and discounting
            Call option payoff only if the price is higher than strike
            -> max(K - S_t , 0)
        """
        if self.sim_results_M is None:
            return -1
        return np.exp(-self.r * self.T) * 1 / self.N * np.sum(np.maximum(self.K - self.sim_results_M[-1], 0))

    def plot_sim_results(self, num_move):
        plt.figure(figsize=(12, 9))
        plt.plot(self.sim_results_M[:, 0:num_move])
        plt.axhline(self.K, c='k', xmin=0, xmax=self.num_steps, label='Strike Price')
        plt.xlim([0, self.num_steps])
        plt.xlabel("Days in Future")
        plt.ylabel('Simulated Price Movements')
        plt.title(f'First {num_move}/{self.N} Random Price Movements')
        plt.legend(loc = 'best')
        plt.show()
