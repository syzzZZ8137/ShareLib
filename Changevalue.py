# -*- coding: utf-8 -*-
"""
Created on Wed May 30 10:25:34 2018

@author: Harrison
"""

import pymysql

def Writeparamdata(changeitem,changevalue,exchange='',index='',days=''):        #获取exchange-index的参数数据
    
    if exchange==''and index=='' and days=='':  #判断是否有合约限制 输出可执行MySQL语句
        strall="UPDATE futurexdb.model_params SET paramvalue='"+ changevalue + "' where accountid=20 and paramname="+"'"\
        +changeitem+"'"
    else:                           
        modelinstance=exchange+'-'+index+'-'+days
        strall="UPDATE futurexdb.model_params SET paramvalue='"+ changevalue + "' where accountid=20 and modelinstance ='"\
        +modelinstance +"' and " +'paramname='+"'"+changeitem+"'"
    
    data=MySQLexecute1(strall)                  #调用函数执行MySQL语句
    
    if exchange==''and index=='' and days=='':  #输出结果整合
        outputstr='本次更改全部时间：'+changeitem+' 值至：'+changevalue+' 受到影响的行数: '+str(data)
    else:
        outputstr='本次更改：'+modelinstance+' '+changeitem+' 值至：'+changevalue+' 受到影响的行数: '+str(data)
    print(outputstr)                            #print结果 
    return outputstr                            #返回结果

def MySQLexecute1(inputstr):                    #替换保存
    connection = pymysql.connect(host='47.100.2.112', port=33306, user='gxqh', passwd='R{Zppc7r0Lxd')
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    influencenum=cursor.execute(inputstr)       #受影响条数
    connection.commit()                         #替换保存
    cursor.close()
    connection.close
    return influencenum                         #返回受影响条数

#%%使用方法
#a=Writeparamdata('alpha','0')
#b=Writeparamdata('alpha','0','DCE','C','1')                        