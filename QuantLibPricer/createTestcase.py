# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 13:17:31 2018

@author: gxjy-003
"""
import pandas as pd
import numpy as np

def createTestCase(underlying_price):   
    '''外生变量underlying_price可以改'''
    
    strike_percentile_array = np.array([80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0]);
    #2d array
    days_remaining_2d_array = np.array([[1.0, 1.0], [1.0, 8.0],
                                        [8.0, 1.0], [8.0, 8.0], [8.0, 15.0],
                                        [15.0, 8.0], [15.0, 15.0], [15.0, 30.0],
                                        [30.0, 15.0], [30.0, 30.0], [30.0, 90.0],
                                        [90.0, 30.0], [90.0, 90.0], [90.0, 180.0]]); 
                          
    volatility_array = 0.01 * np.array([1.0, 5.0, 10.0, 15.0, 20.0, 40.0, 60.0, 100.0, 150.0]);
    interest_rate_array = 0.01 * np.array([0.0, 2.0, 4.0]);
    dividend_rate_array = 0.01 * np.array([0.0, 2.0]);
    option_type_array = np.array(['call', 'put']);
    exercise_type_array = np.array(['A', 'E']);
    option_style_array = np.array(['Vanilla','Asian']);
    Nsample_array = np.array([100.0, 1000.0]);
    Nstep_array = np.array([100.0, 1000.0, 10000.0]);    
    
    
    '''
    strike_percentile_array = np.array([80.0, 85.0, 87.5, 90.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0,100.0, 102.0, 104.0, 106.0, 108.0, 110.0, 112.5, 115.0, 120.0]);
    #days_remaining_array = np.array([1.0, 8.0, 15.0, 30.0, 90.0, 180.0, 360.0]);
    #fix_days_remaining_array = np.array([1.0, 8.0, 15.0, 30.0, 90.0, 180.0, 360.0]);
    days_remaining_2d_array = np.array([[1.0, 1.0], [1.0, 8.0],
                                        [8.0, 1.0], [8.0, 8.0], [8.0, 15.0],
                                        [15.0, 8.0], [15.0, 15.0], [15.0, 30.0],
                                        [30.0, 15.0], [30.0, 30.0], [30.0, 90.0],
                                        [90.0, 30.0], [90.0, 90.0], [90.0, 180.0],
                                        [180.0, 90.0], [180.0, 180.0], [180.0, 360.0],
                                        [360.0, 180.0], [360.0, 360.0]]);                           
    volatility_array = 0.01 * np.array([1.0, 5.0, 10.0, 15.0, 20.0, 40.0, 60.0, 80.0, 100.0, 125.0, 150.0, 200.0, 250.0]);
    interest_rate_array = 0.01 * np.array([0.1, 0.5, 1.0, 2.0, 4.0]);
    dividend_rate_array = 0.01 * np.array([0.0, 1.0, 2.0, 5.0]);
    option_type_array = np.array(['call', 'put']);
    exercise_type_array = np.array(['A', 'E']);
    option_style_array = np.array(['Vanilla','Asian']);
    Nsample_array = np.array([100.0, 500.0, 1000.0]);
    Nstep_array = np.array([100.0, 500.0, 1000.0, 10000.0, 100000.0]);
    '''

    strike_price_array = 0.01 * strike_percentile_array * underlying_price;
    df_price = pd.DataFrame({'strike_percentile':strike_percentile_array, 'strike_price':strike_price_array, 'underlying_price':np.array([underlying_price for i in range(len(strike_percentile_array))])});
    df_expiry = pd.DataFrame(days_remaining_2d_array, columns = ['valueday_to_maturity','fixingday_to_maturity'])
    df_expiry = pd.concat([df_expiry, pd.DataFrame(np.array([underlying_price for i in range(df_expiry.shape[0])]), columns = ['underlying_price'])], axis = 1)
    df_vol = pd.DataFrame({'volatility':volatility_array, 'underlying_price':np.array([underlying_price for i in range(len(volatility_array))])});
    df_r = pd.DataFrame({'interest_rate':interest_rate_array, 'underlying_price':np.array([underlying_price for i in range(len(interest_rate_array))])});
    df_d = pd.DataFrame({'dividend_rate':dividend_rate_array, 'underlying_price':np.array([underlying_price for i in range(len(dividend_rate_array))])});
    df_option_type = pd.DataFrame({'option_type':option_type_array, 'underlying_price':np.array([underlying_price for i in range(len(option_type_array))])});
    df_exercise_type = pd.DataFrame({'option_type':exercise_type_array, 'underlying_price':np.array([underlying_price for i in range(len(exercise_type_array))])});    
    df_option_style = pd.DataFrame({'option_style':option_style_array, 'underlying_price':np.array([underlying_price for i in range(len(option_style_array))])});   
    df_option_Nsample = pd.DataFrame({'Nsample':Nsample_array, 'underlying_price':np.array([underlying_price for i in range(len(Nsample_array))])});
    df_option_Nstep = pd.DataFrame({'Nstep':Nstep_array, 'underlying_price':np.array([underlying_price for i in range(len(Nstep_array))])});
        
    df_merge = pd.merge(df_price, df_expiry, how = 'outer', on = 'underlying_price')
    df_merge = pd.merge(df_merge, df_vol, how = 'outer', on = 'underlying_price')
    df_merge = pd.merge(df_merge, df_r, how = 'outer', on = 'underlying_price')
    df_merge = pd.merge(df_merge, df_d, how = 'outer', on = 'underlying_price')
    df_merge = pd.merge(df_merge, df_option_type, how = 'outer', on = 'underlying_price')
    df_merge = pd.merge(df_merge, df_exercise_type, how = 'outer', on = 'underlying_price')
    df_merge = pd.merge(df_merge, df_option_style, how = 'outer', on = 'underlying_price')
    df_merge = pd.merge(df_merge, df_option_Nsample, how = 'outer', on = 'underlying_price')
    df_merge = pd.merge(df_merge, df_option_Nstep, how = 'outer', on = 'underlying_price')
    
    return df_merge
    
    
if __name__ == '__main__':
    underlying_price = 2500.0
    df_merge = generateTestCase(underlying_price)
    df_merge.to_csv('optionTestCase.csv')