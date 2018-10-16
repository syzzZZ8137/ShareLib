# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:49:43 2018

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
    pricer = Vanilla_BSM(ovo1)
    option, process = pricer();     
    V1 = pricer.PricingFunc(option,process);     
    Greeks_ovo1 = pricer.GreeksFunc(option,process)
     
    ovo2 = VanillaOption(underlying_price, strike_price_2, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer = Vanilla_BSM(ovo2)
    option, process = pricer();     
    V2 = pricer.PricingFunc(option,process);     
    Greeks_ovo2 = pricer.GreeksFunc(option,process)

    ovo3 = VanillaOption(underlying_price, strike_price_3, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer = Vanilla_BSM(ovo3)
    option, process = pricer();     
    V3 = pricer.PricingFunc(option,process);     
    Greeks_ovo3 = pricer.GreeksFunc(option,process)
    
    ovo4 = VanillaOption(underlying_price, strike_price_4, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer = Vanilla_BSM(ovo4)
    option, process = pricer();     
    V4 = pricer.PricingFunc(option,process);     
    Greeks_ovo4 = pricer.GreeksFunc(option,process)
    
    ovo5 = VanillaOption(underlying_price, strike_price_5, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer = Vanilla_BSM(ovo5)
    option, process = pricer();     
    V5 = pricer.PricingFunc(option,process);     
    Greeks_ovo5 = pricer.GreeksFunc(option,process)
    
    V_portfolio = V1 - 0.1*V2 - 0.1*V3 -0.2*V4 -0.2*V5;
    #Greeks_portfolio = Greeks_ovo1 - 0.1*Greeks_ovo2 - 0.1*Greeks_ovo3 -0.2*Greeks_ovo4 -0.2*Greeks_ovo5;

    print('QuantLib 拆分 解析解定价:', V_portfolio)
    