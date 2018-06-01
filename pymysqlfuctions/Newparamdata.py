# -*- coding: utf-8 -*-
"""
Created on Thu May 31 13:42:04 2018

@author: Harrison
"""
import PyMySQLwrite
#%% 向model_params表，为选定合约代码输入参数
def Newparamdata(itemname,itemvalue,exchange,index,days):
    modelinstance=exchange+'-'+index+'-'+days    
    strall="INSERT INTO `futurexdb`.`model_params` (`accountid`, `modelinstance`, `model`, `paramname`, `paramvalue`) VALUES ('20',"\
    + "'"+modelinstance+"'"+", 'wing', '"+itemname+"', '"+itemvalue+"')"
    data=PyMySQLwrite.MySQLexecute1(strall)  
    return data