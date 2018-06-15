# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 14:37:35 2018

@author: Harrison
"""
from WindPy import w
import pandas as pd
w.start();
import GetFutureIndexCode
#%%
def MothStat(startyear):
    startday=startyear+'-01-01'
    Timetoday=str(pd.datetime.now().date())
    codelist=GetFutureIndexCode.GetFutureIndexCode(Timetoday,'Index')
    Outall=[]
    for a in range(codelist.shape[0]):
        Eachdata=w.wsd(codelist.Windcode[a], "pct_chg", startday, Timetoday, "Period=M")
        ChangeP=Eachdata.Data[0]
        ChangeT=Eachdata.Times
        statdata=pd.DataFrame([ChangeP,ChangeT],index=['change','time']).T
        statdata=statdata.dropna(axis=0, how='any')
        statdata.reset_index(inplace=True,drop=True)
        statdata['month']=statdata['time'].apply(lambda x:x.month)
        Outputdata = statdata.month.drop_duplicates().sort_values().tolist()
        Outputdata=pd.DataFrame([Outputdata],index=['month']).T
        Outputdata['Gain']=0
        Outputdata['Loss']=0
        Outputdata['Stay']=0
        for i in range(len(Outputdata)):
            for ii in range(statdata.shape[0]):
                if statdata.loc[ii,'month']==Outputdata.loc[i,'month']:
                    if statdata.loc[ii,'change']>0:
                        Outputdata.Gain[i]=Outputdata.Gain[i]+1
                    elif statdata.loc[ii,'change']<0:
                        Outputdata.Loss[i]=Outputdata.Loss[i]-1
                    else:
                        Outputdata.Stay[i]=Outputdata.Stay[i]+0.5
        Outall.append([codelist.loc[a],Outputdata,statdata])
    return Outall