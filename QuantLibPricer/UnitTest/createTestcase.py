# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 13:17:31 2018

@author: gxjy-003
"""
import pandas as pd
import numpy as np
import itertools

def createTestCase(underlying_price):   
    '''外生变量underlying_price可以改'''
    
    strike_percentile_array = np.array([80.0, 90.0, 100.0, 110.0, 120.0]);
    strike_price_array = 0.01 * strike_percentile_array * underlying_price;
    #2d array
    volatility_array = 0.01 * np.array([0.01, 1.0, 10.0, 50.0, 100.0, 150.0]);
    interest_rate_array = 0.01 * np.array([0.0, 2.0]);
    dividend_rate_array = 0.01 * np.array([0.0, 2.0]);
    option_type_array = np.array(['call', 'put']);
    exercise_type_array = np.array(['A', 'E']);
    option_style_array = np.array(['Vanilla','Asian']);
    Nsample_array = np.array([100.0, 1000.0]);
    Nstep_array = np.array([1000.0, 10000.0]);    
    
    iter_list = list(itertools.product(np.array([underlying_price]), strike_percentile_array, strike_price_array, volatility_array, interest_rate_array, dividend_rate_array, option_type_array, exercise_type_array, option_style_array, Nsample_array, Nstep_array) )
    df= pd.DataFrame(iter_list, columns = ['underlying_price', 'strike_percentile', 'strike_price', 'volatility', 'interest_rate','dividend_rate','option_type', 'exercise_type', 'option_style', 'Nsample', 'Nstep'])
    
    days_remaining_2d_array = [[1.0, 1.0], [1.0, 10.0], [10.0, 1.0], [10.0, 10.0], [10.0, 30.0],
                               [30.0, 10.0], [30.0, 30.0], [30.0, 90.0], [90.0, 30.0], [90.0, 90.0], [90.0, 180.0]];
    df_expiry = pd.DataFrame(days_remaining_2d_array, columns = ['valueday_to_maturity','fixingday_to_maturity'])                               
    df_expiry = pd.concat([df_expiry, pd.DataFrame(np.array([underlying_price for i in range(df_expiry.shape[0])]), columns = ['underlying_price'])], axis = 1)
    df_merge = pd.merge(df, df_expiry, how = 'outer', on = 'underlying_price')
    return df_merge
    
    
if __name__ == '__main__':
    underlying_price = 2500.0
    df_merge = createTestCase(underlying_price)
    df_merge.to_csv('optionTestCase.csv')