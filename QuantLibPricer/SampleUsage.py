# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 14:14:05 2018

@author: Jax_GuoSen
"""

from OptionProduct import * 
from OptionPricer import *
import pandas as pd
import datetime as dt
import QuantLib as ql


'''Sample Input'''
'''
ovo1为香草欧式
ovo2为香草美式
oao1为离散亚欧式FixingDate = ValuationDate
oao2为离散亚欧式FixingDate > ValuationDate  #针对例如4个月的亚式，其中最后一个月才是平均值采价期
oao3为离散亚欧式FixingDate < ValuationDate  #针对亚式期权业务开展后，计算greeks及二次定价
'''

expiry_date = dt.datetime.strptime('20181003', '%Y%m%d')
fixing_date1 = valuation_date = dt.datetime.strptime('20180705', '%Y%m%d')
fixing_date2 = dt.datetime.strptime('20180805', '%Y%m%d')
fixing_date3 = dt.datetime.strptime('20180605', '%Y%m%d')
historical_average = 15300
ovo1 = VanillaOption(15000, 15000, valuation_date,expiry_date, 0.3, 0.01, 0, 'call','E')
ovo2 = VanillaOption(15000, 15000, valuation_date,expiry_date, 0.3, 0.01, 0, 'call','A')
oao1 = AsianOption(15000, 15000, valuation_date,expiry_date, 0.3, 0.01, 0, 'call','E')
oao1(fixing_date1,0)  #塞入个性化变量
oao2 = AsianOption(15000, 15000, valuation_date,expiry_date, 0.3, 0.01, 0, 'call','E')
oao2(fixing_date2,0)  #塞入个性化变量
oao3 = AsianOption(15000, 15000, valuation_date,expiry_date, 0.3, 0.01, 0, 'call','E')
oao3(fixing_date3,historical_average)  #塞入个性化变量

# ---------- testing pricing 香草欧式----------
pricer = Vanilla_BSM(ovo1)
option,process = pricer()
V = pricer.PricingFunc(option,process)
Greeks = pricer.GreeksFunc(option,process)
print('香草欧式价格为：',V)
print('香草欧式希腊字母为：',Greeks)

# ---------- testing pricing 香草美式----------
pricer = Vanilla_BSM(ovo2)
option,process = pricer()
V = pricer.PricingFunc(option,process)
Greeks = pricer.GreeksFunc(option,process)
print('香草美式价格为：',V)
print('香草美式希腊字母为：',Greeks)

# ---------- testing pricing 亚欧式 fixDay=valueDay----------       # exp-fixDay = exp-valueDay
pricer = AriAsian_MC(oao1)
option,process = pricer()
V = pricer.PricingFunc(option,process)
Greeks = pricer.GreeksFunc(option,process)
print('亚式1价格为：',V)
print('亚式希腊字母为：',Greeks)

# ---------- testing pricing 亚欧式 fixDay>valueDay----------      # exp-fixDay < exp-valueDay
pricer = AriAsian_MC(oao2)
option,process = pricer()
V = pricer.PricingFunc(option,process)
Greeks = pricer.GreeksFunc(option,process)
print('亚式2价格为：',V)
print('亚式希腊字母为：',Greeks)
# ---------- testing pricing 亚欧式 fixDay<valueDay----------      # exp-fixDay > exp-valueDay
pricer = AriAsian_MC(oao3)
option,process = pricer()
V = pricer.PricingFunc(option,process)
Greeks = pricer.GreeksFunc(option,process)
print('亚式3价格为：',V)
print('亚式希腊字母为：',Greeks)