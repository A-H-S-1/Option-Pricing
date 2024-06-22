from enum import Enum
from abc import ABC, abstractmethod

class OPTION_TYPE(Enum):
    CALL = 'Call Option'
    PUT = 'Put Option'

class Option_Pricing_Model(ABC):
    """Abstract class defining the interface for option pricing models

    Calculates call and put option price using the option_type indicated"""
    def calc_option_price(self, option_type):
        if option_type == OPTION_TYPE.CALL.value:
            return self._calc_call_option_price()
        elif option_type == OPTION_TYPE.PUT.value:
            return self._calc_put_option_price()
        else:
            return -1

    #Calculates option price for the call option
    @abstractmethod
    def _calc_call_option_price(self):
        pass

    #Calculates option price for the call option
    @abstractmethod
    def _calc_put_option_price(self):
        pass
