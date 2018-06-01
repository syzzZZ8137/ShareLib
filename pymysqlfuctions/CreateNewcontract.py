# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:15:39 2018

@author: Harrison
"""
import pymysql
#%% 在usermodels表里建立新合约
def Newcontract(exchange='',index='',days=''):  #输入需要建立的新合约代码：交易所、品种、日期
    modelinstance=exchange+'-'+index+'-'+days
    strall="INSERT INTO `futurexdb`.`usermodels` (`accountid`, `modelinstance`, `model`) VALUES ('20', '"+modelinstance+"', 'wing');"
    data=MySQLexecute1(strall)  
    return data
#%% MySQL连接函数
def MySQLexecute1(inputstr):                    #替换保存
    connection = pymysql.connect(host='47.100.2.112', port=33306, user='gxqh', passwd='R{Zppc7r0Lxd')
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    influencenum=cursor.execute(inputstr)       #受影响条数
    connection.commit()                         #替换保存
    cursor.close()
    connection.close
    return influencenum                         #返回受影响条数