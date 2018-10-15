# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 11:05:24 2018

@author: Jax_GuoSen
"""
import pandas as pd
import datetime as dt
import QuantLib as ql


class Option(object):
    def __init__(self,underlying_price,strike_price,valuation_date,expiry_date,volatility,interest_rate,dividend_rate,option_type,exercise_type ):
        '''
        Constructor
        '''
        self.underlying_price = ql.SimpleQuote(underlying_price)
        self.strike_price = ql.SimpleQuote(strike_price)
        self.valuation_date = valuation_date
        self.expiry_date = expiry_date
        self.volatility = ql.SimpleQuote(volatility)
        self.interest_rate = ql.SimpleQuote(interest_rate)
        self.dividend_rate = ql.SimpleQuote(dividend_rate)
        self.option_type = option_type  #C/P
        self.exercise_type = exercise_type  #E/A
        

class VanillaOption(Option):
    def __call__(self):
        pass

class AsianOption(Option):
    def __call__(self,fixing_date,historical_average):
        self.fixing_date = fixing_date
        self.historical_average = historical_average
        self.mc_str = 'PseudoRandom'
        self.is_bb = True
        self.is_av = True
        self.is_cv = True
        self.n_require = 10000
        self.tolerance = 0.2
        self.n_max = 1500000
        self.seed = 101
        
        
class BarrierOption(Option):
    def __call__(self, barrierType, barrier):
        self.barrierType = barrierType
        self.barrier = barrier


'''Sample Input'''
# =============================================================================
 expiry_date = dt.datetime.strptime('20190513', '%Y%m%d')
 valuation_date = fixing_date = dt.datetime.strptime('20181015', '%Y%m%d')
# historical_average = 1005
# ovo = VanillaOption(1023, 1000, valuation_date,expiry_date, 0.3, 0, 0.05, 'call','E')
# oao = AsianOption(1023, 1000, valuation_date,expiry_date, 0.3, 0, 0.05, 'call','E')
# oao(fixing_date,historical_average)
 
 barrierType = ql.Barrier.DownOut; 
 barrier0 = 13000; 
 barrier1 = 13000-500;
 barrier2 = 13000-1000;
 barrier3 = 13000-1500;
 
 obo0 = BarrierOption(13000, barrier0, valuation_date, expiry_date, 0.25, 0, 0, 'put', 'E' ) 
 obo0(barrierType, barrier0)
 obo1 = BarrierOption(13000, barrier1, valuation_date, expiry_date, 0.25, 0, 0, 'put', 'E' ) 
 obo1(barrierType, barrier1)
 obo2 = BarrierOption(13000, barrier2, valuation_date, expiry_date, 0.25, 0, 0, 'put', 'E' ) 
 obo2(barrierType, barrier2)
 obo3 = BarrierOption(13000, barrier3, valuation_date, expiry_date, 0.25, 0, 0, 'put', 'E' ) 
 obo3(barrierType, barrier3)

# =============================================================================

 cash_or






