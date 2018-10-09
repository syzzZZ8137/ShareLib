# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:42:57 2018

@author: Yizhou

"""

import pandas as pd
import datetime as dt
import QuantLib as ql


class OptionPricer_BSM(object):
    '''
    Black Scholes Merton option class and its access functions
    option_style: European / American
    option_type: Call / Put
    QuantLib pricing engine: Analytic(Black Scholes Merton; Finite-Difference)  /  Monte-Carlo
        
    '''
    
    
    def __init(self, option_type, strike_price, maturity_date, valuation_date, underlying_price, dividend_rate, interest_rate, volatility):
                
#         ------------- Option setup -------------
        if option_type.lower() in ['c', 'call']:
            _option_type = ql.Option.Call
        elif option_type.lower() in ['p', 'put']:
            _option_type = ql.Option.Put
        else:
            print('unknown option type:', option_type)
            #return(-1)
        
        
        payoff = ql.PlainVanillaPayoff(put_or_call, strike_price)        
        
        
        
        
        self._maturity_date = maturity_date
        self._spot_price = underlying_price
        self._strike_price = strike_price
        self._
        
        
        
    def pricing(self):
#         ------------- Option setup -------------
        
        
        
        
