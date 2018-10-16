# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:34:00 2018

@author: gxjy-003
"""

if __name__ == '__main__':
 
     # ---------- testing pricing 分段看跌，欧式----------
     underlying_price = 12000
     strike_price = 13000
     valuation_date = fixing_date = dt.datetime.strptime('20181015', '%Y%m%d')
     
     expiry_in_months = 7
     expiry_in_days = 7*30
     expiry_date = valuation_date + dt.timedelta(days=expiry_in_days)  # 7个月
     
     expiry_date = dt.datetime.strptime('20190513', '%Y%m%d')
     
     volatility = 0.25
     interest_rate = 0
     dividend_rate = 0
     option_type = 'put'
     exercise_type = 'E'

     
    # 1个 Vanilla European Put Option
    ovo = VanillaOption(underlying_price, strike_price, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
    pricer = Vanilla_BSM(ovo)
    option,process = pricer();     V = pricer.PricingFunc(option,process);     Greeks_ovo = pricer.GreeksFunc(option,process)
     
     # 4个 down-and-out , H < underlying_price
     barrierType = ql.Barrier.DownOut; 
     strike0 = strike_price;  barrier0 = strike0-500; 
     strike1 = strike_price-500; barrier1 = strike_price-1000;
     strike2 = strike_price-1000; barrier2 = strike_price-1500;
     strike3 = strike_price-1500; barrier3 = strike_price-2000;
    
     
     barrier0 = strike_price; 
     barrier1 = strike_price-500;
     barrier2 = strike_price-1000;
     barrier3 = strike_price-1500;
     
     obo0 = BarrierOption(strike_price, barrier0, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
     obo0(barrierType, barrier0)
     obo1 = BarrierOption(strike_price, barrier1, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type)  
     obo1(barrierType, barrier1)
     obo2 = BarrierOption(strike_price, barrier2, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
     obo2(barrierType, barrier2)
     obo3 = BarrierOption(strike_price, barrier3, valuation_date, expiry_date, volatility, interest_rate, dividend_rate, option_type, exercise_type) 
     obo3(barrierType, barrier3)
    
    rebate = 0; ##########?????????????????????????????
    pricer = Barrier_BSM(obo0)
    option, process = pricer(barrierType, barrier0, rebate);     V0 = pricer.PricingFunc(option,process);  ###Greeks_obo0 = pricer.GreeksFunc(option,process)
    pricer = Barrier_BSM(obo1)
    option, process = pricer(barrierType, barrier1, rebate);     V1 = pricer.PricingFunc(option,process);  
    pricer = Barrier_BSM(obo2)
    option, process = pricer(barrierType, barrier2, rebate);     V2 = pricer.PricingFunc(option,process);  
    pricer = Barrier_BSM(obo3)
    option, process = pricer(barrierType, barrier3, rebate);     V3 = pricer.PricingFunc(option,process);  

    # 4个CashOrNothingPayoff
    #TODO




    print('QuantLib 拆分 解析解定价')