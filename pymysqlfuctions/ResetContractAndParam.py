# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:18:17 2018

@author: Harrison
"""
import Delparamdata
import ReadParamData
import NewParamData
#%%重置，复制另一份合约的数据
def ResetContractAndParam(needresetcontract,copyfromcontract='DCE-C-1'):
    old1=ReadParamData.getparamdata(copyfromcontract.split('-')[0],copyfromcontract.split('-')[1],copyfromcontract.split('-')[2])
    Delparamdata.Delparamdata(needresetcontract)
    aa=old1[0]['data']
    sizaa=aa.shape[1]-1
    for i in range(sizaa):
        itemname=aa.columns[i]
        itemvalue=str(aa.iloc[0,i])
        NewParamData.Newparamdata(itemname,itemvalue,needresetcontract.split('-')[0],needresetcontract.split('-')[1],needresetcontract.split('-')[2])
    print('复制'+copyfromcontract+'值至'+needresetcontract)
    return
#%%
    #ResetContractAndParam('DCE-C-360') #按照默认的'DCE-C-1'合约基准值重置'DCE-C-360'所有参数
        
        