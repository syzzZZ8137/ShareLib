# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 13:39:37 2018

@author: Harrison
"""
import PyMySQLwrite
#%% 删除合约全部参数值
def Delparamdata(contractname):
    strall="DELETE FROM `futurexdb`.`model_params` WHERE `accountid`='20' and`modelinstance`='"+contractname+"';"
    data=PyMySQLwrite.MySQLexecute1(strall)  
    return data