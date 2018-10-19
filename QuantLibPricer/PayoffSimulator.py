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
        
        rsg_unif = ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator())
        rsg_gaussian = ql.GaussianRandomSequenceGenerator(rsg_unif)    
        
        # generate Gaussian Path
        '''process: 'StochasticProcess1D', length: 'Time', steps: 'Size', rsg: 'GaussianRandomSequenceGenerator', brownianBridge: 'bool' '''
        seq = ql.GaussianPathGenerator(process, length, timestep, rsg_gaussian, False)
        
        paths = np.zeros((num_paths, timestep+1))
        for i in range(num_paths):
            sample_path = seq.next()
            path = sample_path.value()
            time_list = [path.time(j) for j in range(len(path))]
            value = [path[j] for j in range(len(path))]
            paths[i, :] = np.array(value)           
        return np.array(time_list), paths


def get_PV_payoffs(paths, interest_rate, strike_floor, strike_premium):
    '''
    返回所有路径的payoff: numpy.ndarray
    '''
    PV_payoffs = np.zeros((len(paths),1)) #np.zeros((len(paths), 1))
    arr_month_payoffs = np.zeros((len(paths), 7))
    for i in range(len(paths)):
        PV_payoff_i, arr_month_payoff_i = get_PV_payoff_by_path(paths[i], interest_rate, strike_floor, strike_premium)
        PV_payoffs[i] = PV_payoff_i
        arr_month_payoffs[i] = arr_month_payoff_i
    return PV_payoffs, arr_month_payoffs
    
    
def get_PV_payoff_by_path(path, interest_rate, strike_floor, strike_premium):
    '''返回给定的一条7个月的价格路径的payoff折现后的价格
    以及各个（单月）期权的payout array(未折现)
    '''  
    #将长为7个月的path拆分成7条1个月的路径
    interval_paths = []
    arr_month_payoff = np.zeros((7)) #np.zeros((7, 1))
    arr_PV_month_payoff = np.zeros((7))
    PV_payoff = 0
         
    for j in range(1,8):
        path_month_j = path[1+30*(j-1):31+30*(j-1)]
        interval_paths.append(path[1+30*(j-1):31+30*(j-1)])
        payoff_j = get_payoff_month_j(path_month_j, strike_floor, strike_premium)
        arr_month_payoff[j-1] = payoff_j
        # discount the payoff to present
        time_to_maturity_j = j/12.0
        PV_month_payoff_j = payoff_j * np.exp(-interest_rate * time_to_maturity_j)
        arr_PV_month_payoff[j-1] = PV_month_payoff_j
        PV_payoff += PV_month_payoff_j

    return PV_payoff, arr_month_payoff


def get_payoff_month_j(path_month_j, strike_floor, strike_premium):
    '''
    根据（1个月）路径的最终跌价 X 和 执行价strike = max(KK, strike_floor) + strike_premium 计算payoff
    # path = paths[j-1]; p=path[1:-1].reshape((30,7))
    '''
    avg_month_j = getPathAvg(path_month_j)
    #strike_month_j = PayoffSimulator.getStrike(avg_month_j, strike_floor=13000, strike_premium=1000)
    strike_month_j = getStrike(avg_month_j, strike_floor, strike_premium)
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

  
def getPathAvg(path):
    return np.mean(path)    
    
        
def getStrike(KK, strike_floor, strike_premium):
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

#arr_PV_month_payoffs  #array, Nsample * 7
def getPriceDetails(matrix_month_payoffs):
    '''
    返回7个月每个月的（折现）价格
    '''
    expiry_in_months = matrix_month_payoffs.shape[1]
    arr_price = np.zeros((7))
    for j in range(expiry_in_months):
        month_j_payoffs = np.array(matrix_month_payoffs[:,j])  # Nsample * 1 matrix
        V_j, se_j = getPriceAndStd(month_j_payoffs)
        arr_price[j] = V_j
    return arr_price
        

def pricefunc(strike_floor, volatility, underlying_price):
    '''
    固定underlying_price = 12500
    调整 strike_floor和volatility 
    '''
    
    print('underlying_price:', underlying_price)
    print('strike_floor:', strike_floor)
    
    ovo = OptionProduct.VanillaOption(underlying_price,strike_price,valuation_date,expiry_date,volatility,interest_rate,dividend_rate,option_type,exercise_type)
    pricer = OptionPricer.Vanilla_BSM(ovo)
    option, process = pricer()

    payoffSimulator = PayoffSimulator(process, length, Nsample, Nstep)
    #生成paths, 计算各路径payoff
    time_list, paths = payoffSimulator.simulate_paths_for_process(process, length, Nsample, Nstep)
    
    PV_payoffs, arr_month_payoffs = get_PV_payoffs(paths, interest_rate, strike_floor, strike_premium)
    # (Nsample, expiry_in_months)2darray  -> (Nsample, expiry_in_months)矩阵 
    matrix_month_payoffs = np.asmatrix(arr_month_payoffs)
    price, std_error = getPriceAndStd(PV_payoffs)
    arr_price = getPriceDetails(matrix_month_payoffs)
    
    print('volatility:', volatility)
    print('蒙特卡洛模拟定价', price)
    print('定价标准差', std_error)  
    print('每月payout均值：', arr_price)


if __name__ == '__main__':
     
     # ---------- testing pricing 分段看跌，欧式----------
    
    underlying_price = 12500 #S0, 固定
    strike_premium = 1000
    
    strike_price = underlying_price #用于定义Vanilla平值期权的BSM过程
    valuation_date = dt.datetime.strptime('20181015', '%Y%m%d')
    #fixing_date = valuation_date
    expiry_in_months = 7
    expiry_in_days = 7*30
    expiry_date = valuation_date + dt.timedelta(days=expiry_in_days)  # 7个月

    interest_rate = 0.0
    dividend_rate = 0.0
    option_type = 'put'
    exercise_type = 'E'
    
    Nsample = num_paths = 500000;  
    Nstep = timestep = expiry_in_days #1000;  
    length = (expiry_date - valuation_date).days / 365  #in years
    expiry_in_years = expiry_in_days/365
    

#    volatility = 0.2
#    volatility = 0.25 
#    volatility = 0.3 
#    volatility = 0.35     
#    strike_floor = 13000
#    strike_floor = 12500
#    strike_floor = 12000
        
#    pricefunc(strike_floor=13000, volatility=0.25, underlying_price=13000)
    #蒙特卡洛模拟定价 9015.496776983266
#定价标准差 4.881300309400135
#每月payout均值： [1064.83010783 1189.12730746 1259.82227881 1314.0763557  1358.24033726
# 1397.19215285 1432.20823708]
    
    
    pricefunc(13000, 0.2, 12500)
    pricefunc(13000, 0.25, 12500)
    pricefunc(13000, 0.3, 12500)
    pricefunc(13000, 0.35, 12500)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
