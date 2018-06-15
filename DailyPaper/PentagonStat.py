# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 14:48:48 2018

@author: Harrison
"""
from WindPy import w
import pandas as pd
w.start();
import GetFutureIndexCode
def normrize(aaa,column1):
    for i in range(len(column1)):
        aaa['Z'+column1[i]]=(aaa[column1[i]]-min(aaa[column1[i]]))/(max(aaa[column1[i]])-min(aaa[column1[i]]))*9+1
    return aaa

def PentagonStat(day):
    Timetoday=str(pd.datetime.now().date())
    codelist=GetFutureIndexCode.GetFutureIndexCode(Timetoday,'MainContract')

    strall=''
    for i in range(codelist.shape[0]):
        strall=strall+codelist.Windcode[i]+','
    strall=strall[:-1]

    dataraw=w.wss(strall, "volume,vol_ratio,oi,oi_chg,pct_chg,swing,contractmultiplier,pre_close,close,exch_eng","tradeDate="+day+";cycle=D;VolumeRatio_N=1;priceAdj=U")
    volume=dataraw.Data[0]
    vol_ratio=dataraw.Data[1]
    oi=dataraw.Data[2]
    oi_chg=dataraw.Data[3]
    pct_chg=dataraw.Data[4]
    swing=dataraw.Data[5]
    contractmultiplier=dataraw.Data[6]
    pre_close=dataraw.Data[7]
    close=dataraw.Data[8]
    exch_eng=dataraw.Data[9]


    Outdata=pd.DataFrame([dataraw.Codes,volume,vol_ratio,oi,oi_chg,pct_chg,swing,contractmultiplier,pre_close,close,exch_eng],index=['code','volume','vol_ratio','oi','oi_chg','pct_chg','swing','contractmultiplier','pre_close','close','exch_eng']).T 
    Outdata=Outdata[Outdata['oi']*Outdata['volume']!=0]
    Outdata['oi_ratio']=Outdata['oi']/(Outdata['oi']-Outdata['oi_chg'])
    Outdata['turnvolume']=Outdata['volume']*Outdata['close']*Outdata['contractmultiplier']
    Outdata['pre_turnvolume']=Outdata['volume']/Outdata['vol_ratio']*Outdata['pre_close'] *Outdata['contractmultiplier']
    Outdata['turnvolume_ratio']=Outdata['turnvolume']/Outdata['pre_turnvolume']
    Outdata['pct_chg_abs']=abs(Outdata['pct_chg'])
    Outdata['Z_color']= Outdata['pct_chg'].apply(lambda x:1 if x>=0 else 0)
    Outdata=Outdata[Outdata['turnvolume']>100000000]
    Outdata=normrize(Outdata,['oi_ratio','vol_ratio','turnvolume_ratio','pct_chg_abs','swing'])
    
    Outdata=Outdata.sort_index(axis=1, level=None)
    Outdata=Outdata.sort_values('exch_eng',axis = 0,ascending = False)  
    Outdata.reset_index(inplace=True,drop=True)
    return Outdata