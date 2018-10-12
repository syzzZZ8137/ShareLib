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

    def get_payoffs(self, paths):
        '''
        返回所有路径的payoff: numpy.ndarray
        '''
        def get_payoff_by_path(self, path):
            '''返回给定的一条路径path的payoff'''
            payoff = max(path[-1] - path[0],0)    ########TODO
            return payoff
        
        payoffs = np.zeros((len(paths), 1))
        for i in range(len(paths)):
            payoff_i = get_payoff_by_path(self,paths[i])
            payoffs[i] = payoff_i
        return payoffs
    

if __name__ == '__main__':
    # set option and process
    expiry_date = dt.datetime.strptime('20181003', '%Y%m%d')
    fixing_date1 = valuation_date = dt.datetime.strptime('20180705', '%Y%m%d')
    fixing_date2 = dt.datetime.strptime('20180805', '%Y%m%d')
    fixing_date3 = dt.datetime.strptime('20180605', '%Y%m%d')
    historical_average = 15300
    
    # ---------- testing pricing 香草欧式----------
    ovo1 = VanillaOption(15000, 15000, valuation_date, expiry_date, 0.3, 0.01, 0, 'call','E')
    pricer = Vanilla_BSM(ovo1)
    option, process = pricer()
    
    Nsample = num_paths = 100
    Nstep = timestep = 1000
    length = (expiry_date - valuation_date).days / 365  #in years
    
    payoffSimulator = PayoffSimulator(process, length, Nsample, Nstep)
    #生成paths, 计算各路径payoff
    time, paths = payoffSimulator.simulate_paths_for_process(process, length, Nsample, Nstep)
    payoffs = payoffSimulator.get_payoffs(paths)
     

    
    
    
