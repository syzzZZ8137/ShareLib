# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 14:25:15 2018

@author: gxjy-003
"""
import pandas as pd
import numpy as np
import datetime as dt
import QuantLib as ql

from OptionProduct import * 
from OptionPricer import *

class PayoffSimulator():
    
    def __init__(self, process, length, num_paths, timestep):
        self.process = process
        self.length = length
        self.num_paths = num_paths
        self.timestep = timestep

    def simulate_paths_for_process(self, process, length, num_paths, timestep):
        '''
        process: QuantLib.QuantLib.BlackScholesMertonProcess
        length: float (单位：年)
        num_paths: int, 
        '''    
        def generate_paths(num_paths, timestep):
            arr = np.zeros((num_paths, timestep+1))
            for i in range(num_paths):
                sample_path = seq.next()
                path = sample_path.value()
                time = [path.time(j) for j in range(len(path))]
                value = [path[j] for j in range(len(path))]
                arr[i, :] = np.array(value)
            return np.array(time), arr
        
        rsg_unif = ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator())
        rsg_gaussian = ql.GaussianRandomSequenceGenerator(rsg_unif)    
        
        # generate Gaussian Path
        '''process: 'StochasticProcess1D', length: 'Time', steps: 'Size', rsg: 'GaussianRandomSequenceGenerator', brownianBridge: 'bool' '''
        seq = ql.GaussianPathGenerator(process, length, timestep, rsg_gaussian, False)
        time, paths = generate_paths(num_paths, timestep)
            
        return time, paths
            
#TODO:  function get_payoff_by_path(self, path)         

    def get_payoffs(self, paths, pricer):
        '''
        返回所有路径的payoff: numpy.ndarray
        '''
#        def get_payoff_by_path(self, path, pricer):
#            '''返回给定的一条路径path的payoff'''
#            
#            X = pricer.product.strike_price.value() - path[-1] # 每吨跌价 = K-S_T
#            
#            if 0<X<=500:
#                payoff = X
#            elif 500<X<=1000:
#                payoff = 500 + 0.9* (X-500)
#            elif 1000<X<=1500:
#                payoff = 950 + 0.8* (X-1000)
#            elif 1500<X<=2000:
#                payoff = 1350 + 0.6* (X-1500)
#            elif X>2000:
#                payoff = 1650 + 0.4* (X-2000)
#            else:
#                #X<=0
#                payoff = 0    
#            
#            return payoff
        
        payoffs = np.zeros((len(paths), 1))
        for i in range(len(paths)):
            payoff_i = PayoffSimulator.get_payoff_by_path(self, paths[i], pricer)
            payoffs[i] = payoff_i
        return payoffs
    
    def get_payoff_by_path(self, path, pricer):
        '''返回给定的一条路径path的payoff'''
    
        X = pricer.product.strike_price.value() - path[-1] # 每吨跌价 = K-S_T
        if 0<X<=500:
            payoff = X
        elif 500<X<=1000:
            payoff = 500 + 0.9* (X-500)
        elif 1000<X<=1500:
            payoff = 950 + 0.8* (X-1000)
        elif 1500<X<=2000:
            payoff = 1350 + 0.6* (X-1500)
        elif X>2000:
            payoff = 1650 + 0.4* (X-2000)
        else:
            #X<=0
            payoff = 0    
        return payoff
    
def getPriceAndStd(payoffs, interest_rate, time_to_maturity):
    V = np.mean(np.exp(-interest_rate * time_to_maturity) * payoffs)
    Nsample = len(payoffs)
    se = np.sqrt((np.sum(payoffs**2)-Nsample*V**2)/Nsample/(Nsample-1))
    return V, se

   
if __name__ == '__main__':
 
     # ---------- testing pricing 分段看跌，欧式----------
     underlying_price = 12000
     strike_price = 13000
     valuation_date = fixing_date = dt.datetime.strptime('20181015', '%Y%m%d')
     expiry_in_months = 7
     expiry_in_days = 7*30
     expiry_date = valuation_date + dt.timedelta(days=expiry_in_days)  # 7个月
     volatility = 0.25
     interest_rate = 0
     dividend_rate = 0
     option_type = 'put'
     exercise_type = 'E'
         
     # ---------- 不拆分, MC模拟价格路径，自定义payoff function----------
     # set option and process
     #ovo = VanillaOption(13000, 13000, valuation_date, expiry_date, 0.25, 0, 0, 'put','E')
     ovo = VanillaOption(underlying_price,strike_price,valuation_date,expiry_date,volatility,interest_rate,dividend_rate,option_type,exercise_type)
     pricer = Vanilla_BSM(ovo)
     option, process = pricer()
     
     Nsample = num_paths = 100000;  
     Nstep = timestep = 1000;  
     length = (expiry_date - valuation_date).days / 365  #in years   

     payoffSimulator = PayoffSimulator(process, length, Nsample, Nstep)
     #生成paths, 计算各路径payoff
     time, paths = payoffSimulator.simulate_paths_for_process(process, length, Nsample, Nstep)
     payoffs = payoffSimulator.get_payoffs(paths, pricer)
     # payoffs -> price
     price, std_error = getPriceAndStd(payoffs, interest_rate, expiry_in_days)
     print('分段看跌欧式期权1定价', price)
     print('定价标准差', std_error)
     '''分段看跌欧式期权1定价 737.1083842646926
     定价标准差 8.645412156065138'''
     
    
    
    
    
