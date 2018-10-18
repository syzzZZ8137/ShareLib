# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 14:25:15 2018

@author: gxjy-003 (yizhou)
"""
#import pandas as pd
import numpy as np
import datetime as dt
import QuantLib as ql
import time
import OptionProduct
import OptionPricer

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
                time_list = [path.time(j) for j in range(len(path))]
                value = [path[j] for j in range(len(path))]
                arr[i, :] = np.array(value)
            return np.array(time_list), arr
        
        rsg_unif = ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator())
        rsg_gaussian = ql.GaussianRandomSequenceGenerator(rsg_unif)    
        
        # generate Gaussian Path
        '''process: 'StochasticProcess1D', length: 'Time', steps: 'Size', rsg: 'GaussianRandomSequenceGenerator', brownianBridge: 'bool' '''
        seq = ql.GaussianPathGenerator(process, length, timestep, rsg_gaussian, False)
        time_list, paths = generate_paths(num_paths, timestep)
            
        return time_list, paths
       

    def get_PV_payoffs(self, paths, interest_rate, strike_floor, strike_premium):
        '''
        返回所有路径的payoff: numpy.ndarray
        '''
        
        PV_payoffs = np.zeros((len(paths), 1))
        for i in range(len(paths)):
            PV_payoff_i = PayoffSimulator.get_PV_payoff_by_path(self, paths[i], interest_rate, strike_floor, strike_premium)
            PV_payoffs[i] = PV_payoff_i
        return PV_payoffs
    
# =============================================================================
#     def get_payoff_by_path(self, path, pricer):
#         '''返回给定的一条路径path的payoff'''
#     
#         X = pricer.product.strike_price.value() - path[-1] # 每吨跌价 = K-S_T
#         if 0<X<=500:
#             payoff = X
#         elif 500<X<=1000:
#             payoff = 500 + 0.9* (X-500)
#         elif 1000<X<=1500:
#             payoff = 950 + 0.8* (X-1000)
#         elif 1500<X<=2000:
#             payoff = 1350 + 0.6* (X-1500)
#         elif X>2000:
#             payoff = 1650 + 0.4* (X-2000)
#         else:
#             #X<=0
#             payoff = 0    
#         return payoff
# =============================================================================
    
    
    def get_PV_payoff_by_path(self, path, interest_rate, strike_floor, strike_premium):
         '''返回给定的一条7个月的价格路径的payoff折现后的价格'''
            
         def get_payoff_month_j(self, path_month_j, strike_floor, strike_premium):
            '''
            根据（1个月）路径的最终跌价 X 和 执行价strike = max(KK, strike_floor) + strike_premium 计算payoff
            # path = paths[j-1]; p=path[1:-1].reshape((30,7))
            '''
            avg_month_j = PayoffSimulator.getPathAvg(path_month_j)
            strike_month_j = PayoffSimulator.getStrike(avg_month_j, strike_floor=13000, strike_premium=1000)
            X = strike_month_j - path_month_j[-1] # 每吨跌价 = K-S_T
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
        
         #将长为7个月的path拆分成7条1个月的路径
         interval_paths = []
         arr_payoff = np.zeros((7, 1))
         PV_payoff = 0
         
         for j in range(1,8):
             path_month_j = path[1+30*(j-1):31+30*(j-1)]
             interval_paths.append(path[1+30*(j-1):31+30*(j-1)])
             payoff_j = get_payoff_month_j(self, path_month_j, strike_floor, strike_premium)
             arr_payoff[j-1] = payoff_j
             # discount the payoff to present
             time_to_maturity_j = j/12.0
             PV_payoff += payoff_j * np.exp(-interest_rate * time_to_maturity_j)
         return PV_payoff
  
    def getPathAvg(path):
        return np.mean(path)    
    
        
    def getStrike(KK, strike_floor=13000, strike_premium=1000):
        '''
        strike = max(KK, strike_floor) + strike_premium
        '''
        return max(KK, strike_floor) + strike_premium

    
    def getPriceAndStd(PV_payoffs):
        #PV_payoff = Sum (PV_payoff_j * np.exp(-interest_rate * time_to_maturity_j) )
        V = np.mean(PV_payoffs)
        Nsample = len(PV_payoffs)
        se = np.sqrt((np.sum(PV_payoffs**2)-Nsample*V**2)/Nsample/(Nsample-1))
        return V, se


if __name__ == '__main__':
     
     # ---------- testing pricing 分段看跌，欧式----------
    
    t_start = time.time()
#    underlying_price = 13000 #S0
    underlying_price = 100
    
    strike_price = underlying_price #用于定义Vanilla平值期权的BSM过程
    valuation_date = dt.datetime.strptime('20181015', '%Y%m%d')
    #fixing_date = valuation_date
    expiry_in_months = 7
    expiry_in_days = 7*30
    expiry_date = valuation_date + dt.timedelta(days=expiry_in_days)  # 7个月
    volatility = 0.25 
#    volatility = 0.3 
#    volatility = 0.35 
#    volatility = 0.4
    
    interest_rate = 0.0
    dividend_rate = 0.0
    option_type = 'put'
    exercise_type = 'E'

    # ---------- MC模拟价格路径，自定义payoff function----------
    # set option and process
    #ovo = VanillaOption(13000, 13000, valuation_date, expiry_date, 0.25, 0, 0, 'put','E')
    ovo = OptionProduct.VanillaOption(underlying_price,strike_price,valuation_date,expiry_date,volatility,interest_rate,dividend_rate,option_type,exercise_type)
    pricer = OptionPricer.Vanilla_BSM(ovo)
    option, process = pricer()
    
    Nsample = num_paths = 500000;  
    Nstep = timestep = expiry_in_days #1000;  
    length = (expiry_date - valuation_date).days / 365  #in years
    expiry_in_years = expiry_in_days/365

    payoffSimulator = PayoffSimulator(process, length, Nsample, Nstep)
    #生成paths, 计算各路径payoff
    time_list, paths = payoffSimulator.simulate_paths_for_process(process, length, Nsample, Nstep)
    
    strike_floor = underlying_price
    strike_premium = 1000
#    strike_premium = underlying_price/13.0
    
    PV_payoffs = payoffSimulator.get_PV_payoffs(paths, interest_rate, strike_floor, strike_premium)
    price, std_error = PayoffSimulator.getPriceAndStd(PV_payoffs)
    
    print('volatility:', volatility)
    print('strike_floor:', strike_floor)
    print('每月回看看跌欧式期权蒙特卡洛模拟定价', price)
    print('定价标准差', std_error)
    print('用时：', time.time() - t_start, 'seconds')
#    '''定价 736.4435151762555
#    定价标准差  '''
   
    
    
    
