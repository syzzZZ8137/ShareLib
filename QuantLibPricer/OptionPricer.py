# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 11:14:45 2018

@author: Jax_GuoSen
"""

import pandas as pd
import numpy as np
import datetime as dt
import QuantLib as ql


       
def PortfolioPricingFunc(pricer_list, weight_list):
    
    num_product = len(pricer_list)

    if len(weight_list) != num_product:
        print('Invalid Input! Inputs pricer_list and weight_list have different length. Please try again!')
        raise ValueError
    else:
        V_portfolio = 0
        V_arr = np.zeros((len(pricer_list), 1))
        Greeks_portfolio = pd.DataFrame([0, 0, 0, 0, 0], columns = [''], index=['Delta','Gamma','Vega(%)','ThetaPerDay','Rho(%)'])        
        
        for i in range(num_product):
            pricer = pricer_list[i]
            option, process = pricer()
            V_arr[i] = V_i = pricer.PricingFunc(option, process)
            Greeks_i = pricer.GreeksFunc(option, process) # pd.DataFrame([option.delta(),option.gamma(),option.vega()/100,option.theta()/365,option.rho()/100], columns = [''], index=['Delta','Gamma','Vega(%)','ThetaPerDay','Rho(%)'])
            V_portfolio += V_i * weight_list[i]
            Greeks_portfolio += Greeks_i
        #V_portfolio = V_arr * weight_list
        print ('期权组合价格：', V_portfolio)
        print ('期权组合希腊字母：', Greeks_portfolio)
        return V_portfolio, Greeks_portfolio
        

class PricingFunc(object):
    '''
    定价类-抽象, product为OptionProduct.Option对象   
    '''
    def __init__(self,product):
        '''
        Constructor
        '''
        self.product = product
    
    def __call__(self):
        raise NotImplementedError
    
    def PricingFunc(self):
        raise NotImplementedError
    
    def GreeksFunc(self):
        raise NotImplementedError    
    
    def PreWork(self):
        '''      
        返回 payoff,exercise,process
        payoff：QuantLib.PlainVanillaPayoff类型, 
        excercise：QuantLib.EuropeanExercise或QuantLib.AmericanExercise类型, 与self.product的行权方式对应
        process: QuantLib.BlackScholesMertonProcess类型
        '''        
        #定义Payoff
        if self.product.option_type == 'call':
            put_or_call = ql.Option.Call
        elif self.product.option_type == 'put':
            put_or_call = ql.Option.Put
        else:
            print('unknown option type:', self.product.option_type)
            return(-1)
        payoff = ql.PlainVanillaPayoff(put_or_call,self.product.strike_price.value())  #根据call/put，产生相应Payoff对象

        #定义Exercise
        #shift expiry date forward by 1 day, so that calculation can be done on the expiry day
        expiry_date_1 = self.product.expiry_date + dt.timedelta(days=1)
        eDate = ql.Date(expiry_date_1.day, expiry_date_1.month, expiry_date_1.year)
        self.product.valuation_date = min(self.product.expiry_date, self.product.valuation_date)
        self.vDate = ql.Date(self.product.valuation_date.day, self.product.valuation_date.month, self.product.valuation_date.year)
        if self.product.exercise_type == 'E':
            exercise = ql.EuropeanExercise(eDate)
        elif self.product.exercise_type == 'A':
            exercise = ql.AmericanExercise(self.vDate, eDate)
        else:
            print('unknown option type:', self.product.exercise_type)
            return(-1)
        
        #定义Calendar
        #Set the valuation date, by default it will use today's date
        ql.Settings.instance().evaluationDate = self.vDate
        calendar = ql.China()
        day_counter = ql.ActualActual()
        
        #定义Vol,Dividend,InterestRate的期限结构
        # 假定股息、无风险利率和波动率曲线是平的
        dividend_curve = ql.FlatForward(0,ql.TARGET(), ql.QuoteHandle(self.product.dividend_rate), day_counter)
        interest_curve = ql.FlatForward(0,ql.TARGET(), ql.QuoteHandle(self.product.interest_rate), day_counter)
        volatility_curve = ql.BlackConstantVol(0, ql.TARGET(),ql.QuoteHandle(self.product.volatility), day_counter)
        
        u = ql.QuoteHandle(self.product.underlying_price)
        d = ql.YieldTermStructureHandle(dividend_curve)
        r = ql.YieldTermStructureHandle(interest_curve)
        v = ql.BlackVolTermStructureHandle(volatility_curve)
        
        # 标准BSM process
        process = ql.BlackScholesMertonProcess(u, d, r, v)
        return payoff,exercise,process
    

    def Numerical_Greeks(self,option):
        '''
        数值方法计算希腊字母 (Delta, Gamma, Vega(%), ThetaPerDay, Rho(%))
        Greeks: pandas.DataFrame
        '''
        
        #Delta Gamma
        u0 = self.product.underlying_price.value()
        p0 = option.NPV()
        h = 0.01 #dS
        self.product.underlying_price.setValue(u0 + h)
        p_plus = option.NPV() 
        #print(p_plus)
        self.product.underlying_price.setValue(u0 - h)
        p_minus = option.NPV()
        self.product.underlying_price.setValue(u0)
        delta = (p_plus - p_minus)/(2 * h)
        gamma = (p_plus - 2 * p0 + p_minus)/(h * h)
        
        #Vega
        v0 = self.product.volatility.value()
        h = 0.1
        self.product.volatility.setValue(v0 + h)
        p_plus = option.NPV()
        self.product.volatility.setValue(v0)
        vega = (p_plus - p0)/h
        
        #Theta
        ql.Settings.instance().evaluationDate = self.vDate + 1
        p1 = option.NPV()
        h = 1/365.0
        theta = (p1 - p0)/h
        ql.Settings.instance().evaluationDate = self.vDate
        
        #Rho
        r0 = self.product.interest_rate.value()
        h = 0.0001
        self.product.interest_rate.setValue(r0 + h)
        p_plus = option.NPV()
        self.product.interest_rate.setValue(r0)
        rho = (p_plus - p0)/h
        
        #greeks, pandas.DataFrame
        Greeks = pd.DataFrame([delta,gamma,vega/100,theta/365,rho/100], columns = [''], \
                               index=['Delta','Gamma','Vega(%)','ThetaPerDay','Rho(%)'])
        
        return Greeks

class Vanilla_BSM(PricingFunc):
    '''
    香草期权定价类, PricingFunc的子类
    先执行Set_Param函数
    '''
    def __call__(self):
        '''计算PayOff与Exercise，定义Option为QuantLib标准VanillaOption对象'''
        payoff, exercise, process = self.PreWork()
        option = ql.VanillaOption(payoff, exercise)
        return option,process
        
    def PricingFunc(self,option,process):
        '''设置定价引擎，返回 option, process'''
        if self.product.exercise_type == 'E':
            engine = ql.AnalyticEuropeanEngine(process)
        elif self.product.exercise_type == 'A':
            engine = ql.BaroneAdesiWhaleyEngine(process)
            #engine = ql.BinomialVanillaEngine(process, "crr", 100)
        else:
            pass
        option.setPricingEngine(engine)
        return option.NPV()
    
    def GreeksFunc(self,option,process):
        if self.product.exercise_type == 'E':
            engine = ql.AnalyticEuropeanEngine(process)
            option.setPricingEngine(engine)
            Greeks = pd.DataFrame([option.delta(),option.gamma(),option.vega()/100,option.theta()/365,option.rho()/100], columns = [''], \
                                   index=['Delta','Gamma','Vega(%)','ThetaPerDay','Rho(%)'])
        elif self.product.exercise_type == 'A':
            #用离散法计算Greeks
            engine = ql.BaroneAdesiWhaleyEngine(process)
            #engine = ql.BinomialVanillaEngine(process, "crr", 100)  #BTM
            option.setPricingEngine(engine)
            Greeks = self.Numerical_Greeks(option)  #进入离散法计算Greeks
        else:
            pass
        return Greeks

class Barrier_BSM(PricingFunc):
    '''
    障碍期权定价类, PricingFunc的子类
    '''
    def __call__(self, barrierType, barrier, rebate):
        '''计算PayOff与Exercise，定义Option为QuantLib标准BarrierOption对象'''
        payoff, exercise, process = self.PreWork() # Vanilla Payoff, European/American, BSM process
        option = ql.BarrierOption(barrierType, barrier, rebate, payoff, exercise)
        return option,process
    
    def PricingFunc(self,option,process):
        '''设置定价引擎'''
        # 欧式、美式均为QuantLib.AnalyticBarrierEngine
        if self.product.exercise_type == 'E':
            engine = ql.AnalyticBarrierEngine(process)
        elif self.product.exercise_type == 'A':
            engine = ql.BaroneAdesiWhaleyEngine(process)
        else:
            pass
        option.setPricingEngine(engine)
        return option.NPV()
    
    def GreeksFunc(self,option,process):
        engine = ql.AnalyticBarrierEngine(process)
        option.setPricingEngine(engine)
        
        try:
            if self.product.exercise_type == 'E':
                engine = ql.AnalyticBarrierEngine(process)
                option.setPricingEngine(engine)
                Greeks = pd.DataFrame([option.delta(),option.gamma(),option.vega()/100,option.theta()/365,option.rho()/100], columns = [''], \
                                       index=['Delta','Gamma','Vega(%)','ThetaPerDay','Rho(%)'])
            elif self.product.exercise_type == 'A':
                    #用BaroneAdesiWhaley离散法计算Greeks
                    engine = ql.BaroneAdesiWhaleyEngine(process)
                    #engine = ql.BinomialVanillaEngine(process, "crr", 100)  #BTM
                    option.setPricingEngine(engine)
                    Greeks = self.Numerical_Greeks(option)
            else:
                raise ValueError #传入的参数self.product.exercise_type 无效
                
        #缺少解析解时用离散法蒙特卡洛模拟，计算Greeks
        except:
            engine = ql.MCDiscreteArithmeticAPEngine(process, self.product.mc_str, self.product.is_bb, self.product.is_av, self.product.is_cv, self.product.n_require, self.product.tolerance, self.product.n_max, self.product.seed)
            option.setPricingEngine(engine)
            Greeks = self.Numerical_Greeks(option)  
            
        return Greeks

class AriAsian_MC(PricingFunc):
    def __call__(self):
        payoff,exercise,process = self.PreWork()
        average_type = ql.Average.Arithmetic
        past_fixs = 0  if (self.product.valuation_date-self.product.fixing_date).days<=0 else (self.product.valuation_date-self.product.fixing_date).days
        #过去的fixed天数
        running_sum = self.product.historical_average*past_fixs  #过去总和，若无则设为0
        fixing_dates = [self.cast_datetime_to_ql_date(s) 
                for s in pd.date_range(self.product.fixing_date, self.product.expiry_date, freq = 'D')]
        
        option = ql.DiscreteAveragingAsianOption(average_type, running_sum, past_fixs, fixing_dates, payoff, exercise)
        return option,process

    def cast_datetime_to_ql_date(self,dt):
        return ql.Date(dt.day, dt.month,dt.year)
    
    def PricingFunc(self,option,process):
        '''
        设置engine为QuantLib中相应的定价引擎，返回 option, process
        '''
        #无论亚美还是亚欧都一样
        engine = ql.MCDiscreteArithmeticAPEngine(process, self.product.mc_str, self.product.is_bb, self.product.is_av, self.product.is_cv, self.product.n_require, self.product.tolerance, self.product.n_max, self.product.seed)
        option.setPricingEngine(engine)
        return option.NPV()
        
    
    def GreeksFunc(self,option,process):

        try:
            if self.product.exercise_type == 'E':
                engine = ql.AnalyticEuropeanEngine(process)
                option.setPricingEngine(engine)
                Greeks = pd.DataFrame([option.delta(),option.gamma(),option.vega()/100,option.theta()/365,option.rho()/100], columns = [''], \
                                       index=['Delta','Gamma','Vega(%)','ThetaPerDay','Rho(%)'])
            elif self.product.exercise_type == 'A':
                    #用BaroneAdesiWhaley离散法计算Greeks
                    engine = ql.BaroneAdesiWhaleyEngine(process)
                    #engine = ql.BinomialVanillaEngine(process, "crr", 100)  #BTM
                    option.setPricingEngine(engine)
                    Greeks = self.Numerical_Greeks(option)
            else:
                raise ValueError #传入的参数self.product.exercise_type 无效
            
        #缺少解析解时用离散法蒙特卡洛模拟，计算Greeks
        except:
            engine = ql.MCDiscreteArithmeticAPEngine(process, self.product.mc_str, self.product.is_bb, self.product.is_av, self.product.is_cv, self.product.n_require, self.product.tolerance, self.product.n_max, self.product.seed)
            option.setPricingEngine(engine)
            Greeks = self.Numerical_Greeks(option)  
            
# =============================================================================
#         #无论亚美还是亚欧都一样
#         engine = ql.MCDiscreteArithmeticAPEngine(process, self.product.mc_str, self.product.is_bb, self.product.is_av, self.product.is_cv, self.product.n_require, self.product.tolerance, self.product.n_max, self.product.seed)
#         option.setPricingEngine(engine)
#         Greeks = self.Numerical_Greeks(option)  #进入离散法计算Greeks
# =============================================================================
        
        return Greeks
