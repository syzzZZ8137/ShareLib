# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 15:22:37 2018

@author: gxjy-003
"""

from OptionProduct import * 
from OptionPricer import *
import pandas as pd
import datetime as dt
import QuantLib as ql


if __name__ == '__main__':
 
     # ---------- testing pricing 分段看跌，欧式----------
    underlying_price = 13000
    strike_price = 13000
    valuation_date = fixing_date = dt.datetime.strptime('20181015', '%Y%m%d')
    expiry_date = dt.datetime.strptime('20190513', '%Y%m%d');
#    expiry_in_months = 7
#    expiry_in_days = 7*30
#    expiry_date = valuation_date + dt.timedelta(days=expiry_in_days)  # 7个月
        
    volatility = 0.25
    interest_rate = 0
    dividend_rate = 0
    option_type = 'put'
    exercise_type = 'E'
    
    strike_price_1 = strike_price;  
    strike_price_2 = strike_price-500;
    strike_price_3 = strike_price-1000;
    strike_price_4 = strike_price-1500; 
    strike_price_5 = strike_price-2000; 

    # 5个 Vanilla European Put Option
    ovo1 = VanillaOption(underlying_price, strike_price_1, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer1 = Vanilla_BSM(ovo1)    
     
    ovo2 = VanillaOption(underlying_price, strike_price_2, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer2 = Vanilla_BSM(ovo2)
    
    ovo3 = VanillaOption(underlying_price, strike_price_3, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer3 = Vanilla_BSM(ovo3)   
    
    ovo4 = VanillaOption(underlying_price, strike_price_4, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer4 = Vanilla_BSM(ovo4)

    ovo5 = VanillaOption(underlying_price, strike_price_5, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer5 = Vanilla_BSM(ovo5)    
    
    pricer_list = [pricer1, pricer2, pricer3, pricer4, pricer5]
    weight_list = [1.0, -0.1, -0.1, -0.2, -0.2]

    V_result, Greeks_result = PortfolioPricingFunc(pricer_list, weight_list)
    