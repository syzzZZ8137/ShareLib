# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:21:26 2018

@author: Harrison
"""
import GetDataMySQL
import CreateNewcontract
import Newparamdata
#%% 建立新合约，并根据旧合约数据复制参数。新合约必须是usermodels表里没有的。
def Copyparam(newcontract,oldcontract):
    CreateNewcontract.Newcontract(newcontract.split('-')[0],newcontract.split('-')[1],newcontract.split('-')[2])
    old1=GetDataMySQL.getparamdata(oldcontract.split('-')[0],oldcontract.split('-')[1],oldcontract.split('-')[2])
    aa=old1[0]['data']
    sizaa=aa.shape[1]-1
    for i in range(sizaa):
        itemname=aa.columns[i]
        itemvalue=str(aa.iloc[0,i])
        Newparamdata.Newparamdata(itemname,itemvalue,newcontract.split('-')[0],newcontract.split('-')[1],newcontract.split('-')[2])
    print('复制'+oldcontract+'值至'+newcontract)
#%% 使用方法
    #Copyparam('DCE-I-1','DCE-C-1') #建立新合约DCE-I-1把DCE-C-1参数数据复制复制过去