# -*- coding: utf-8 -*-
"""
Created on Fri May 25 10:54:50 2018

@author: Harrison
"""
import pymysqlread
def getparamdata(exchange='DCE',index='C',model='wing'):        #获取exchange-index的参数数据
    #%% 获取数据库数据
    modelinstance=exchange+'-'+index
    strall='SELECT * FROM futurexdb.model_params where accountid=20 and model= '+"'wing' " +'and modelinstance like'+"'%"+modelinstance+"%'"
    data=pymysqlread.dbconn(strall)                             #读取函数pymysqlread
    #%%整理数据表
    days = data.modelinstance.drop_duplicates().tolist()
    Totaltable=[]
    for i in range(len(days)):
        b=data[data['modelinstance']==days[i]]                  #按时间分割
        b.reset_index(inplace=True,drop=True)                   #重置index
        bb=b.pivot('modelinstance','paramname','paramvalue')    #转换数据表头
        bb['day']=int(days[i].split('-')[2])                    #加入日期列
        Totaltable.append({'days':days[i],'data':bb})
    return Totaltable
#%%使用方法
if __name__ == '__main__':
    a=getparamdata(exchange='DCE',index='C',model='wing')
    alpha=list(a[0]['data'].alpha)                              #获取第一个表的alpha值
    day=list(a[0]['data'].day)                                  #获取第一个表的day值
    print(alpha,day)