# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:15:39 2018

@author: Harrison
"""
import PyMySQLwrite
#%% 在usermodels表里建立新合约
def Newcontract(exchange,index,days):  #输入需要建立的新合约代码：交易所、品种、日期
    modelinstance=exchange+'-'+index+'-'+days
    strall="INSERT INTO `futurexdb`.`usermodels` (`accountid`, `modelinstance`, `model`) VALUES ('20', '"+modelinstance+"', 'wing');"
    data=PyMySQLwrite.MySQLexecute1(strall)  
    return data