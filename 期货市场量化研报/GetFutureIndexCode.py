# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 10:31:06 2018

@author: Harrison
"""
from WindPy import w
import pandas as pd
#import datetime as dt

def GetFutureIndexCode(date,futureorindex):
    w.start()
    if futureorindex=='Index':
        string="date="+date+";sectorid=1000016325000000"
    elif futureorindex=='MainContract':
        string="date="+date+";sectorid=1000015510000000"
    a=w.wset("sectorconstituent",string)
    b=a.Data[1:3]
    c=pd.DataFrame(b,index=['Windcode','ZH']).T
    #c['aaa']=1
    c['contract']=c['Windcode'].apply(lambda x:x.split('.')[0])
    c['exchange']=c['Windcode'].apply(lambda x:x.split('.')[1])
    return c