# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 11:39:14 2018

@author: merz
"""

# 90 days 
# asian put
# s = 17000
# x = 16000
# v = 0.2
# r = 0.01

import datetime
import pandas as pd
import QuantLib as ql

def cast_datetime_to_ql_date(dt):
    return ql.Date(dt.day, dt.month,dt.year)


# calendar set up
calendar = ql.China()
day_counter = ql.ActualActual()

valuation_date = pd.datetime(2018,7,5)
expiry_date = pd.datetime(2018,10,3)
expiry_date_1 = expiry_date + datetime.timedelta(days = 1)

ql_valuation_date = cast_datetime_to_ql_date(valuation_date)
ql_expiry_date = cast_datetime_to_ql_date(expiry_date_1)

fixing_dates = [cast_datetime_to_ql_date(s) 
                for s in pd.date_range(valuation_date, expiry_date, freq = 'D')]

past_fixs = 0
running_sum = 0

ql.Settings.instance().evaluationDate = ql_valuation_date


# option params
option_type = ql.Option.Call

average_type = ql.Average.Arithmetic

strike_price = ql.SimpleQuote(15000)

underlying_price = ql.SimpleQuote(15000)

risk_free_rate = ql.SimpleQuote(0.01)

volatility = ql.SimpleQuote(0.3)

dividend_rate = ql.SimpleQuote(0)


# curve setup
dividend_curve = ql.FlatForward(0,ql.TARGET(), ql.QuoteHandle(dividend_rate), day_counter)
interest_curve = ql.FlatForward(0,ql.TARGET(), ql.QuoteHandle(risk_free_rate), day_counter)
volatility_curve = ql.BlackConstantVol(0, ql.TARGET(),ql.QuoteHandle(volatility), day_counter)

# option exercise type
exercise = ql.EuropeanExercise(ql_expiry_date)
#exercise = ql.AmericanExercise(ql_valuation_date,ql_expiry_date)

# quote handling
underlying_h = ql.QuoteHandle(underlying_price)
# yield term structure handling
flat_rf_term_structure = ql.YieldTermStructureHandle(interest_curve)
flat_dividend_term_structure = ql.YieldTermStructureHandle(dividend_curve)

# volatility structure handling
flat_vol_term_structure = ql.BlackVolTermStructureHandle(volatility_curve)

# BS equation behind
bsm_process = ql.BlackScholesMertonProcess(underlying_h, flat_dividend_term_structure, flat_rf_term_structure, flat_vol_term_structure)

# fix???
# payoff
payoff_asian_option = ql.PlainVanillaPayoff(option_type, strike_price.value())

# discretely-averaged asian option
discrete_asian_option = ql.DiscreteAveragingAsianOption(average_type, running_sum, past_fixs, fixing_dates, payoff_asian_option, exercise)

# pricing engine
mc_str = 'PseudoRandom'
is_bb = True
is_av = True
is_cv = True
n_require = 100000
tolerance = 0.02
n_max = 1500000
seed = 101

price_engine = ql.MCDiscreteArithmeticAPEngine(bsm_process, mc_str, is_bb, is_av, is_cv, n_require, tolerance, n_max, seed)
discrete_asian_option.setPricingEngine(price_engine)

print('='*40)
print('Price is : %.4f.'%discrete_asian_option.NPV())

#%% greeks
u0 = underlying_price.value()
p0 = discrete_asian_option.NPV()
h = 0.01

underlying_price.setValue(u0 + h)
p_plus = discrete_asian_option.NPV() 

underlying_price.setValue(u0 - h)
p_minus = discrete_asian_option.NPV()

underlying_price.setValue(u0)

a_delta = (p_plus - p_minus)/(2 * h)

print('Delta is : %.4f.'%a_delta)

a_gamma = (p_plus - 2 * p0 + p_minus)/(h * h)

print('Gamma is : %.4f.'%a_gamma)

r0 = risk_free_rate.value()
h = 0.0001
risk_free_rate.setValue(r0 + h)
p_plus = discrete_asian_option.NPV()

risk_free_rate.setValue(r0)

a_rho = (p_plus - p0)/h

print('Rho is   : %.4f.'%a_rho)

v0 = volatility.value()
h = 0.0001
volatility.setValue(v0 + h)
p_plus = discrete_asian_option.NPV()

volatility.setValue(v0)

a_vega = (p_plus - p0)/h

print('Vega is  : %.4f.'%a_vega)

ql.Settings.instance().evaluationDate = ql_valuation_date + 1
p1 = discrete_asian_option.NPV()
h = 1/365.0
a_theta = (p1 - p0)/h
ql.Settings.instance().evaluationDate = ql_valuation_date

print('Theta is : %.4f.'%a_theta)
print('='*40)

