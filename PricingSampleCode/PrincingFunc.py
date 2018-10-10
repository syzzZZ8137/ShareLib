# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 10:01:02 2018

@author: Jax_GuoSen
"""

import pandas as pd
import datetime as dt
import QuantLib as ql


class PricingFunc(object):
    '''
    定价类-抽象,定义一个输入模板Constructor    
    '''

    def __init__(self,underlying_price,strike_price,valuation_date,expiry_date,volatility,interest_rate,dividend_rate,option_type ):
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
        self.option_type = option_type
        



class Vanilla_BSM(PricingFunc):
    '''
    香草期权定价类
    先执行Set_Param函数
    '''
    def Set_Process(self,exercise_type):
        
        '''定义Payoff'''
        if self.option_type == 'call':
            put_or_call = ql.Option.Call
        elif self.option_type == 'put':
            put_or_call = ql.Option.Put
        else:
            print('unknown option type:', self.option_type)
            return(-1)
        payoff = ql.PlainVanillaPayoff(put_or_call,self.strike_price.value())  #根据call/put，产生相应Payoff对象

        '''定义Exercise'''
        #shift expiry date forward by 1 day, so that calculation can be done on the expiry day
        self.exercise_type = exercise_type
        expiry_date_1 = self.expiry_date + dt.timedelta(days=1)
        eDate = ql.Date(expiry_date_1.day, expiry_date_1.month, expiry_date_1.year)
        self.valuation_date = min(self.expiry_date, self.valuation_date)
        self.vDate = ql.Date(self.valuation_date.day, self.valuation_date.month, self.valuation_date.year)
        if self.exercise_type == 'E':
            exercise = ql.EuropeanExercise(eDate)
        elif self.exercise_type == 'A':
            exercise = ql.AmericanExercise(self.vDate, eDate)
        else:
            print('unknown option type:', self.exercise_type)
            return(-1)
        
        
        '''定义Calendar'''
        #Set the valuation date, by default it will use today's date
        ql.Settings.instance().evaluationDate = self.vDate
        calendar = ql.China()
        day_counter = ql.ActualActual()


        '''定义Option,输入PayOff与Exercise'''
        option = ql.VanillaOption(payoff, exercise)
        
        '''定义TermStructure(Vol,Dividend,Int)'''
        #dividend_curve = ql.FlatForward(self.vDate, self.dividend_rate.value(), day_counter)
        #interest_curve = ql.FlatForward(self.vDate, self.interest_rate.value(), day_counter)
        #volatility_curve = ql.BlackConstantVol(self.vDate, calendar, self.volatility.value(), day_counter)
        dividend_curve = ql.FlatForward(0,ql.TARGET(), ql.QuoteHandle(self.dividend_rate), day_counter)
        interest_curve = ql.FlatForward(0,ql.TARGET(), ql.QuoteHandle(self.interest_rate), day_counter)
        volatility_curve = ql.BlackConstantVol(0, ql.TARGET(),ql.QuoteHandle(self.volatility), day_counter)
        
        u = ql.QuoteHandle(self.underlying_price)
        d = ql.YieldTermStructureHandle(dividend_curve)
        r = ql.YieldTermStructureHandle(interest_curve)
        v = ql.BlackVolTermStructureHandle(volatility_curve)
        process = ql.BlackScholesMertonProcess(u, d, r, v)
        
        return option,process

#         Setup Black Scholes Merton Process
        
    def PricingFunc(self,option,process):
        '''------------- Set pricing engine, return both option and process -------------'''
        if self.exercise_type == 'E':
            engine = ql.AnalyticEuropeanEngine(process)
        elif self.exercise_type == 'A':
            engine = ql.BaroneAdesiWhaleyEngine(process)
            #engine = ql.BinomialVanillaEngine(process, "crr", 100)
        else:
            pass
        option.setPricingEngine(engine)
        return option.NPV()
    
    def GreeksFunc(self,option,process):
        if self.exercise_type == 'E':
            engine = ql.AnalyticEuropeanEngine(process)
            option.setPricingEngine(engine)
            Greeks = pd.DataFrame([option.delta(),option.gamma(),option.vega()/100,option.theta()/365,option.rho()/100],\
                                   index=['Delta','Gamma','Vega(%)','ThetaPerDay','Rho(%)'])
        elif self.exercise_type == 'A':
            #用离散法计算Greeks
            engine = ql.BaroneAdesiWhaleyEngine(process)
            #engine = ql.BinomialVanillaEngine(process, "crr", 100)  #BTM
            option.setPricingEngine(engine)
            
            #Delta Gamma
            u0 = self.underlying_price.value()
            p0 = option.NPV()
            h = 0.01 #dS
            self.underlying_price.setValue(u0 + h)
            p_plus = option.NPV() 
            #print(p_plus)
            self.underlying_price.setValue(u0 - h)
            p_minus = option.NPV()
            self.underlying_price.setValue(u0)
            delta = (p_plus - p_minus)/(2 * h)
            gamma = (p_plus - 2 * p0 + p_minus)/(h * h)
            
            #Vega
            v0 = self.volatility.value()
            h = 0.1
            self.volatility.setValue(v0 + h)
            print(self.volatility.value())
            p_plus = option.NPV()
            print(p_plus)
            self.volatility.setValue(v0)
            vega = (p_plus - p0)/h
            
            #Theta
            ql.Settings.instance().evaluationDate = self.vDate + 1
            p1 = option.NPV()
            h = 1/365.0
            theta = (p1 - p0)/h
            ql.Settings.instance().evaluationDate = self.vDate
            
            #Rho
            r0 = self.interest_rate.value()
            h = 0.0001
            self.interest_rate.setValue(r0 + h)
            p_plus = option.NPV()
            self.interest_rate.setValue(r0)
            rho = (p_plus - p0)/h
            
            Greeks = pd.DataFrame([delta,gamma,vega/100,theta/365,rho/100],\
                                   index=['Delta','Gamma','Vega(%)','ThetaPerDay','Rho(%)'])
            
        else:
            pass

        return Greeks



class AriAsian_MC(PricingFunc):
    pass

'''实例'''

expiry_date = dt.datetime.strptime('20170324', '%Y%m%d')
valuation_date = dt.datetime.strptime('20170322', '%Y%m%d')
# ---------- testing pricing 香草欧式----------
pricer = Vanilla_BSM(1023, 1000, valuation_date,expiry_date, 0.3, 0, 0.05, 'call')
option,process = pricer.Set_Process('E')
V = pricer.PricingFunc(option,process)
Greeks = pricer.GreeksFunc(option,process)
print('香草欧式价格为：',V)
print('香草欧式希腊字母为：',Greeks)

# ---------- testing pricing 香草美式----------
pricer = Vanilla_BSM(1023, 1000, valuation_date,expiry_date, 0.3, 0, 0.05, 'call')
option,process = pricer.Set_Process('A')
V = pricer.PricingFunc(option,process)
Greeks = pricer.GreeksFunc(option,process)
print('香草美式价格为：',V)
print('香草美式希腊字母为：',Greeks)
# ---------- testing pricing 亚欧式----------



