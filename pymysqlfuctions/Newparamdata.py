# -*- coding: utf-8 -*-
"""
Created on Thu May 31 13:42:04 2018

@author: Harrison
"""
import pymysql
#%% 向model_params表，为选定合约代码输入参数
def Newparamdata(itemname,itemvalue,exchange='',index='',days=''):
    modelinstance=exchange+'-'+index+'-'+days    
    strall="INSERT INTO `futurexdb`.`model_params` (`accountid`, `modelinstance`, `model`, `paramname`, `paramvalue`) VALUES ('20',"+ "'"+modelinstance+"'"+", 'wing', '"+itemname+"', '"+itemvalue+"')"
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