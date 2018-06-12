# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 11:03:25 2018

@author: Harrison
"""
from WindPy import w
import GetUnderling
import ChangeParamData
w.start();
#%%根据wind数据库更新f_ref价格数据（使用时间：最好是交易时间，开盘前可能会有误差）
def refreshref():
    exchange,contract=GetUnderling.Getunderling()
    numex=exchange.shape[0]
    for i in range(numex):    
        numcon=len(contract[i]['contract']) 
        for ii in range(numcon):
            concode=contract[i]['contract'][ii]
            excode=exchange.exchange[i]
            combine=concode+'.'+excode[:3]
            winddata=w.wsq(combine, "rt_last")
            pricedata=str(winddata.Data[0][0])
            done=ChangeParamData.Writeparamdata('f_ref',pricedata,excode,concode)
            print(done)
    return